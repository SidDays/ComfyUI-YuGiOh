import os
import zlib
from PIL import Image
import UnityPy

from .utils import tensor_to_pil

DEFAULT_STEAM_LOCALDATA_DIR = (
    r"C:\Program Files (x86)\Steam\steamapps\common\Yu-Gi-Oh! Master Duel\LocalData"
)


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
