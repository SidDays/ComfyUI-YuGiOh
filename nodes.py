from .src.generator import generate_yugioh_card_image
from .src.config import ATTRIBUTE_MAP, FRAME_MAP, ICONS_MAP, LAYOUTS
from .src.unity import (
    DEFAULT_STEAM_LOCALDATA_DIR,
    get_card_unity_path,
    pack_master_duel_texture,
)

class YuGiOhCardGenerator:
    """
    A custom node for ComfyUI to generate Yu-Gi-Oh style cards.
    """
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "series": (LAYOUTS, {"default": LAYOUTS[0]}),
                "frame": (list(FRAME_MAP.keys()), {"default": "effect"}),
                "name": ("STRING", {"default": "My Custom Card", "multiline": False}),
                "attribute": (list(ATTRIBUTE_MAP.keys()),),
                "type": ("STRING", {"default": "[ Spellcaster / Normal ]", "multiline": False}),
                "icon": (list(ICONS_MAP.keys()), {"default": list(ICONS_MAP.keys())[0]}),
                "level_rank": ("INT", {"default": 7, "min": 0, "max": 12}),
                "art": ("IMAGE",),
                "effect": ("STRING", {"default": "The ultimate wizard in terms of attack and defense.", "multiline": True}),
                "atk_value": ("STRING", {"default": "2500"}),
                "def_value": ("STRING", {"default": "2100"}),
                "link_rating": ("STRING", {"default": "auto"}),
                "link_markers": ("STRING", {"default": ""}),
                "is_pendulum": ("BOOLEAN", {"default": False}),
                "pendulum_scale_blue": ("STRING", {"default": ""}),
                "pendulum_scale_red": ("STRING", {"default": "auto"}), 
                "pendulum_effect": ("STRING", {"default": "", "multiline": True}),
                "corner_text": ("STRING", {"default": ""}),
                "set_id": ("STRING", {"default": ""}),
                "password": ("STRING", {"default": ""}),
                "edition": ("STRING", {"default": ""}),
                "copyright": ("STRING", {"default": "©2020 Studio Dice/SHUEISHA, TV TOKYO, KONAMI"}),
                "json_override": ("STRING", {"default": "{}"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("card_image",)
    FUNCTION = "generate_card"
    CATEGORY = "Yu-Gi-Oh!"

    def generate_card(self, series, frame, art, attribute, name, level_rank, type, icon, effect, atk_value, def_value, link_rating, link_markers, is_pendulum, pendulum_scale_blue, pendulum_scale_red, pendulum_effect, corner_text, set_id, password, edition, copyright, json_override):
        return generate_yugioh_card_image(series, frame, art, attribute, name, level_rank, type, icon, effect, atk_value, def_value, link_rating, link_markers, is_pendulum, pendulum_scale_blue, pendulum_scale_red, pendulum_effect, corner_text, set_id, password, edition, copyright, json_override)


class YuGiOhMasterDuelUnityPath:
    """
    A custom node for ComfyUI that converts a Konami Card ID into its
    Yu-Gi-Oh! Master Duel Unity bundle path (e.g., 10544 -> cd/cdcc181b).
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "optional": {
                "konami_id": ("INT", {"default": 4007, "min": 0, "max": 99999999, "step": 1}),
                "region": (["tcg", "ocg", "common"], {"default": "tcg"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("unity_path",)
    FUNCTION = "get_unity_path"
    CATEGORY = "Yu-Gi-Oh!"

    def get_unity_path(self, konami_id: int = None, region: str = "tcg"):
        return (get_card_unity_path(konami_id, region),)


class YuGiOhMasterDuelAssetPacker:
    """
    A custom node for ComfyUI that patches a Yu-Gi-Oh! Master Duel Unity
    AssetBundle's Texture2D with an input IMAGE tensor using UnityPy and saves
    the modified bundle to <output_dir>/0000/<xx>/<bundle_hash>.
    """

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "unity_path": ("STRING", {"default": "cd/cdcc181b", "multiline": False}),
            },
            "optional": {
                "localdata_dir": (
                    "STRING",
                    {"default": DEFAULT_STEAM_LOCALDATA_DIR, "multiline": False},
                ),
                "output_dir": ("STRING", {"default": "", "multiline": False}),
                "target_texture_name": ("STRING", {"default": "", "multiline": False}),
                "resize_to_target": ("BOOLEAN", {"default": True}),
                "compression": (["lz4", "none", "original"], {"default": "lz4"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("saved_bundle_path",)
    FUNCTION = "pack_asset"
    OUTPUT_NODE = True
    CATEGORY = "Yu-Gi-Oh!"

    def pack_asset(
        self,
        image,
        unity_path: str,
        localdata_dir: str = DEFAULT_STEAM_LOCALDATA_DIR,
        output_dir: str = "",
        target_texture_name: str = "",
        resize_to_target: bool = True,
        compression: str = "lz4",
    ):
        saved_path = pack_master_duel_texture(
            image=image,
            unity_path=unity_path,
            localdata_dir=localdata_dir,
            output_dir=output_dir,
            target_texture_name=target_texture_name,
            resize_to_target=resize_to_target,
            compression=compression,
        )
        return (saved_path,)


NODE_CLASS_MAPPINGS = {
    "YuGiOhCardGenerator": YuGiOhCardGenerator,
    "YuGiOhMasterDuelUnityPath": YuGiOhMasterDuelUnityPath,
    "YuGiOhMasterDuelAssetPacker": YuGiOhMasterDuelAssetPacker,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "YuGiOhCardGenerator": "Yu-Gi-Oh! Card Generator",
    "YuGiOhMasterDuelUnityPath": "Yu-Gi-Oh! Master Duel Unity Path",
    "YuGiOhMasterDuelAssetPacker": "Yu-Gi-Oh! Master Duel Asset Packer",
}
