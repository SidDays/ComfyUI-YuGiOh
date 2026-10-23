from .src.generator import generate_yugioh_card_image
from .src.config import ATTRIBUTE_MAP, FRAME_MAP, ICONS_MAP, LAYOUTS

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

NODE_CLASS_MAPPINGS = {
    "YuGiOhCardGenerator": YuGiOhCardGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "YuGiOhCardGenerator": "Yu-Gi-Oh! Card Generator"
}
