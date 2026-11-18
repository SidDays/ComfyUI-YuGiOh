# ComfyUI-YuGiOh

A collection of custom nodes for [ComfyUI](https://www.comfy.org/) for generating Yu-Gi-Oh! cards and modding artwork for Yu-Gi-Oh! video games, such as [Yu-Gi-Oh! Master Duel](https://store.steampowered.com/app/1449850/YuGiOh_Master_Duel/).

## Features

- **Custom Card Generation**: Render Yu-Gi-Oh! cards from custom artwork, frames, attributes, stats, levels/ranks, and effect text.
- **Card Password → Konami ID Lookup**: Resolve 8-digit card passcodes to Konami Card IDs using a local lookup database (`asset/db/konami_id_lookup.json`), with an optional rate-limited YGOPRODeck API fallback.
- **Master Duel AssetBundle Path Resolution**: Compute the CRC32-hashed Unity AssetBundle path (`<xx>/<hash>`) for any Konami Card ID and region (`tcg`, `ocg`, `common`).
- **Master Duel Texture Packing**: Inject generated or custom `IMAGE` tensors directly into Yu-Gi-Oh! Master Duel Unity AssetBundles using `UnityPy`.

---

## Installation

### Manual Installation
1. Clone this repository into your `ComfyUI/custom_nodes` directory:
   ```bash
   cd ComfyUI/custom_nodes
   git clone https://github.com/SidDays/ComfyUI-YuGiOh.git
   ```
2. Install the package dependencies (specifically `UnityPy>=1.25.0`) using ComfyUI's Python environment:
   ```bash
   cd ComfyUI-YuGiOh
   pip install -e .
   ```
3. Restart ComfyUI.

---

## Nodes

### 1. Yu-Gi-Oh! Card Generator (`YuGiOhCardGenerator`)
Generates a Series 10 style Yu-Gi-Oh! card image (`IMAGE`) from user-supplied artwork and card metadata.

- **Key Inputs**:
  - `series`: Card layout series (currently `series_10`).
  - `frame`: Card frame template (`normal`, `effect`, `ritual`, `fusion`, `synchro`, `darksynchro`, `xyz`, `link`, `token`, `spell`, `trap`).
  - `name`: Card title.
  - `attribute`: Card attribute (`none`, `dark`, `light`, `earth`, `water`, `fire`, `wind`, `divine`, `spell`, `trap`).
  - `type`: Monster type/subtype line (e.g., `[ Spellcaster / Normal ]`) or Spell/Trap property text.
  - `level_rank`: Monster level/rank (`0`–`12`).
  - `art`: Input `IMAGE` tensor placed in the card artwork box.
  - `effect`: Card effect or flavor text.
  - `atk_value` / `def_value`: ATK and DEF values.
  - `corner_text`, `set_id`, `password`, `edition`, `copyright`: Additional card footer/header text fields.
  - *Note*: `icon`, `link_rating`, `link_markers`, `is_pendulum`, `pendulum_scale_blue`, `pendulum_scale_red`, `pendulum_effect`, and `json_override` are exposed on the node interface for upcoming layout features and are not yet rendered by the generator.
- **Output**: `card_image` (`IMAGE`)

---

### 2. Yu-Gi-Oh! Password to Konami ID (`YuGiOhPasswordToKonamiId`)
Resolves a card's 8-digit password (passcode) to its internal Konami Card ID.

- **Inputs**:
  - `password` (`STRING`): 8-digit card passcode (e.g., `46448938`).
  - `use_ygoprodeck_api` (`BOOLEAN`, default `False`): When enabled, falls back to a rate-limited query against the [YGOPRODeck API](https://db.ygoprodeck.com/api/v7/cardinfo.php) if the password is not found in `asset/db/konami_id_lookup.json`, and caches newly resolved entries locally.
- **Output**: `konami_id` (`INT`, returns `0` if no match is found).

---

### 3. Yu-Gi-Oh! Master Duel Unity Path (`YuGiOhMasterDuelUnityPath`)
Computes the Yu-Gi-Oh! Master Duel Unity AssetBundle relative path for a given Konami Card ID by hashing `Card/Images/Illust/{region}/{konami_id}` with CRC32.

- **Inputs**:
  - `konami_id` (`INT`): Konami Card ID (e.g., `4007`, `10544`).
  - `region` (`tcg` | `ocg` | `common`, default `tcg`): Asset region.
- **Output**: `unity_path` (`STRING`, e.g., `cd/cdcc181b`).

---

### 4. Yu-Gi-Oh! Master Duel Asset Packer (`YuGiOhMasterDuelAssetPacker`)
Patches a Yu-Gi-Oh! Master Duel Unity AssetBundle's `Texture2D` with an input `IMAGE` tensor using `UnityPy` and writes the modified bundle to disk.

- **Inputs**:
  - `image` (`IMAGE`): Replacement artwork image.
  - `unity_path` (`STRING`): Relative bundle path (e.g., `cd/cdcc181b`) or a direct path to a bundle file on disk.
  - `localdata_dir` (`STRING`): Path to Master Duel's `LocalData` directory (defaults to `C:\Program Files (x86)\Steam\steamapps\common\Yu-Gi-Oh! Master Duel\LocalData`). Automatically searches `0000/` and `<account_id>/0000/` subdirectories.
  - `output_dir` (`STRING`): Root directory for the patched bundle (defaults to ComfyUI's output directory).
  - `target_texture_name` (`STRING`): Optional `Texture2D` `m_Name` filter; if empty, replaces all `Texture2D` objects in the bundle.
  - `resize_to_target` (`BOOLEAN`, default `True`): Resizes the input image with Lanczos resampling to match the original texture dimensions.
  - `compression` (`lz4` | `none` | `original`, default `lz4`): AssetBundle compression mode.
- **Output**: `saved_bundle_path` (`STRING`) — written to `<output_dir>/0000/<xx>/<bundle_hash>`.

---

## Master Duel Modding Workflow

You can chain the nodes together in ComfyUI to replace in-game card art:

1. Pass a card's 8-digit passcode into **Yu-Gi-Oh! Password to Konami ID** to get `konami_id`.
2. Connect `konami_id` to **Yu-Gi-Oh! Master Duel Unity Path** to get `unity_path`.
3. Connect `unity_path` and your custom `IMAGE` to **Yu-Gi-Oh! Master Duel Asset Packer** to produce the patched bundle under `<output_dir>/0000/<xx>/<bundle_hash>`.
4. Copy the generated `0000/` folder contents into your Master Duel `LocalData/<account_id>/` directory (back up your original files first).

---

## Development

To install dev dependencies (`pytest`, `ruff`, `mypy`, `pre-commit`) in editable mode:

```bash
cd ComfyUI-YuGiOh
pip install -e .[dev]
pre-commit install
```

Run tests and linting:

```bash
pytest
ruff check .
mypy .
```

## TODO: Publishing to Registry

If you wish to share this custom node with others in the community, you can publish it to the registry. We've already auto-populated some fields in `pyproject.toml` under `tool.comfy`, but please double-check that they are correct.

You need to make an account on https://registry.comfy.org and create an API key token.

- [ ] Go to the [registry](https://registry.comfy.org). Login and create a publisher id (everything after the `@` sign on your registry profile).
- [ ] Add the publisher id into the pyproject.toml file.
- [ ] Create an api key on the Registry for publishing from Github. [Instructions](https://docs.comfy.org/registry/publishing#create-an-api-key-for-publishing).
- [ ] Add it to your Github Repository Secrets as `REGISTRY_ACCESS_TOKEN`.

A Github action will run on every git push. You can also run the Github action manually. Full instructions [here](https://docs.comfy.org/registry/publishing). Join our [discord](https://discord.com/invite/comfyorg) if you have any questions!

## License

MIT License — see [LICENSE](LICENSE) for details.

