import json
import os
import threading
import time
import urllib.parse
import urllib.request
import zlib
from PIL import Image
import UnityPy

from .utils import get_root_dir, tensor_to_pil

DEFAULT_STEAM_LOCALDATA_DIR = (
    r"C:\Program Files (x86)\Steam\steamapps\common\Yu-Gi-Oh! Master Duel\LocalData"
)

LOOKUP_DB_REL_PATH = os.path.join("asset", "db", "konami_id_lookup.json")
YGOPRODECK_API_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
MIN_API_INTERVAL_SEC = 0.1  # Max 10 requests/sec (YGOPRODeck limit is 20 req/sec)

_LOOKUP_CACHE = None
_PW_TO_KONAMI_ID = None
_LOOKUP_LOCK = threading.Lock()
_LAST_API_CALL_TS = 0.0


def _get_lookup_db_path() -> str:
    return os.path.join(get_root_dir(), LOOKUP_DB_REL_PATH)


def _load_lookup_cache() -> tuple[dict, dict]:
    global _LOOKUP_CACHE, _PW_TO_KONAMI_ID
    if _LOOKUP_CACHE is not None and _PW_TO_KONAMI_ID is not None:
        return _LOOKUP_CACHE, _PW_TO_KONAMI_ID

    db_path = _get_lookup_db_path()
    _LOOKUP_CACHE = {}
    _PW_TO_KONAMI_ID = {}

    if os.path.isfile(db_path):
        try:
            with open(db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    _LOOKUP_CACHE = data
                    for kid_str, info in data.items():
                        if isinstance(info, dict):
                            pw = _normalize_password(str(info.get("password", "")))
                            if pw:
                                _PW_TO_KONAMI_ID[pw] = int(kid_str)
        except Exception:
            pass

    return _LOOKUP_CACHE, _PW_TO_KONAMI_ID


def _save_lookup_cache() -> None:
    if _LOOKUP_CACHE is None:
        return
    db_path = _get_lookup_db_path()
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    sorted_cache = {
        k: {"name": v.get("name", ""), "password": v.get("password", "")}
        for k, v in sorted(_LOOKUP_CACHE.items(), key=lambda item: int(item[0]))
    }
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(sorted_cache, f, indent=4, sort_keys=False, ensure_ascii=False)
        f.write("\n")


def _normalize_password(password: str) -> str:
    if not password:
        return ""
    cleaned = password.strip()
    if not cleaned.isdigit():
        return ""
    return cleaned.lstrip("0") or "0"


def _query_ygoprodeck(params: dict) -> dict | None:
    global _LAST_API_CALL_TS
    query = {"misc": "yes", **params}
    url = f"{YGOPRODECK_API_URL}?{urllib.parse.urlencode(query)}"
    req = urllib.request.Request(url, headers={"User-Agent": "ComfyUI-YuGiOh/1.0"})

    now = time.monotonic()
    elapsed = now - _LAST_API_CALL_TS
    if elapsed < MIN_API_INTERVAL_SEC:
        time.sleep(MIN_API_INTERVAL_SEC - elapsed)
    _LAST_API_CALL_TS = time.monotonic()

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def lookup_konami_id(
    password: str = "",
    use_ygoprodeck_api: bool = False,
) -> int:
    """
    Resolves a Yu-Gi-Oh! card password (8-digit passcode) to its Konami ID using
    the local lookup cache ('asset/db/konami_id_lookup.json'), optionally falling
    back to a rate-limited YGOPRODeck API query and caching the result.
    Returns 0 if no matching Konami ID is found.
    """
    norm_pw = _normalize_password(password)
    if not norm_pw:
        return 0

    with _LOOKUP_LOCK:
        cache, by_pw = _load_lookup_cache()

        if norm_pw in by_pw:
            return int(by_pw[norm_pw])

        if not use_ygoprodeck_api:
            return 0

        payload = _query_ygoprodeck({"id": norm_pw})
        if not payload:
            return 0

        cards = payload.get("data", [])
        if not cards:
            return 0

        target = cards[0]
        misc_list = target.get("misc_info", [])
        if not misc_list or "konami_id" not in misc_list[0]:
            return 0

        resolved_id = int(misc_list[0]["konami_id"])
        kid_key = str(resolved_id)
        card_name = str(target.get("name", "")).strip()

        cache[kid_key] = {
            "name": card_name or cache.get(kid_key, {}).get("name", ""),
            "password": norm_pw,
        }
        by_pw[norm_pw] = resolved_id

        try:
            _save_lookup_cache()
        except Exception:
            pass

        return resolved_id


def get_card_unity_path(konami_id: int = None, region: str = "tcg") -> str:
    """
    Computes the Yu-Gi-Oh! Master Duel 2-char prefix + 8-char CRC32 bundle path
    for a given Konami card ID (e.g., 10544 -> 'cd/cdcc181b').
    """
    if konami_id is None or not isinstance(konami_id, int) or konami_id <= 0:
        return ""

    logical_path = f"Card/Images/Illust/{region}/{konami_id}"
    crc = zlib.crc32(logical_path.encode("utf-8")) & 0xFFFFFFFF
    hex_name = f"{crc:08x}"
    return f"{hex_name[:2]}/{hex_name}"


def resolve_source_bundle_path(unity_path: str, localdata_dir: str = "") -> str:
    """
    Resolves the source AssetBundle file on disk given a unity_path (e.g., 'cd/cdcc181b')
    and a LocalData directory (which may point to LocalData, LocalData/<account_id>,
    or LocalData/<account_id>/0000).
    """
    clean_unity_path = unity_path.strip().replace("\\", "/").lstrip("/")
    if not clean_unity_path:
        raise ValueError("unity_path cannot be empty.")

    # Allow passing a direct file path in unity_path if it already exists on disk
    if os.path.isfile(unity_path):
        return os.path.abspath(unity_path)

    base_dir = localdata_dir.strip() if localdata_dir else DEFAULT_STEAM_LOCALDATA_DIR
    if not os.path.isdir(base_dir):
        raise FileNotFoundError(
            f"LocalData directory not found: '{base_dir}'. Please provide a valid localdata_dir."
        )

    rel_parts = clean_unity_path.split("/")
    if rel_parts[0] == "0000":
        rel_under_0000 = os.path.join(*rel_parts[1:])
    else:
        rel_under_0000 = os.path.join(*rel_parts)

    candidates = [
        os.path.join(base_dir, rel_under_0000),
        os.path.join(base_dir, "0000", rel_under_0000),
    ]

    # Also check account_id subdirectories inside LocalData (e.g., LocalData/<account_id>/0000/<xx>/<hash>)
    for entry in sorted(os.listdir(base_dir)):
        sub_dir = os.path.join(base_dir, entry)
        if os.path.isdir(sub_dir):
            candidates.append(os.path.join(sub_dir, "0000", rel_under_0000))
            candidates.append(os.path.join(sub_dir, rel_under_0000))

    for candidate in candidates:
        if os.path.isfile(candidate):
            return os.path.abspath(candidate)

    raise FileNotFoundError(
        f"Could not find bundle '{clean_unity_path}' inside LocalData directory '{base_dir}'."
    )


def get_default_output_root(output_dir: str = "") -> str:
    """
    Returns the custom output_dir if provided, otherwise ComfyUI's default output directory.
    """
    if output_dir and output_dir.strip():
        return os.path.abspath(output_dir.strip())

    try:
        import folder_paths  # type: ignore

        return os.path.abspath(folder_paths.get_output_directory())
    except Exception:
        return os.path.abspath("output")


def pack_master_duel_texture(
    image,
    unity_path: str,
    localdata_dir: str = "",
    output_dir: str = "",
    target_texture_name: str = "",
    resize_to_target: bool = True,
    compression: str = "lz4",
) -> str:
    """
    Injects a ComfyUI IMAGE tensor into a Master Duel Unity AssetBundle's Texture2D
    object and writes the patched bundle to <output_root>/0000/<xx>/<bundle_hash>.
    """
    if image is None:
        raise ValueError("An input image is required to pack a Master Duel Unity asset.")

    source_bundle_path = resolve_source_bundle_path(unity_path, localdata_dir)
    pil_img = tensor_to_pil(image).convert("RGBA")

    env = UnityPy.load(source_bundle_path)
    replaced = False
    target_name = target_texture_name.strip() if target_texture_name else ""

    for obj in env.objects:
        if obj.type.name == "Texture2D":
            data = obj.read()
            if not target_name or data.m_Name == target_name:
                if resize_to_target and pil_img.size != (data.m_Width, data.m_Height):
                    pil_img = pil_img.resize(
                        (data.m_Width, data.m_Height), Image.Resampling.LANCZOS
                    )
                else:
                    data.m_Width, data.m_Height = pil_img.size

                data.image = pil_img
                data.save()
                replaced = True
                if target_name:
                    break

    if not replaced:
        raise ValueError(
            f"No matching Texture2D ('{target_name}') found in bundle '{source_bundle_path}'."
        )

    bundle_hash = os.path.basename(source_bundle_path)
    hex_prefix = bundle_hash[:2]
    out_root = get_default_output_root(output_dir)

    if os.path.basename(out_root) == "0000":
        dest_dir = os.path.join(out_root, hex_prefix)
    else:
        dest_dir = os.path.join(out_root, "0000", hex_prefix)

    os.makedirs(dest_dir, exist_ok=True)
    out_path = os.path.join(dest_dir, bundle_hash)

    save_kwargs = {} if compression == "original" else {"packer": compression}
    with open(out_path, "wb") as f:
        f.write(env.file.save(**save_kwargs))

    return out_path
