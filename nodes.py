from .src.generator import generate_yugioh_card_image
from .src.config import FRAME_MAP

class YuGiOhCardGenerator:
    """
    A custom node for ComfyUI to generate Yu-Gi-Oh style cards.
    Supports advanced formatting:
    - [Text]: Force line, compress if too long.
    - [[Text]]: Force line, justify (spread) to fill width.
    - {Text}: Non-breaking text (treat as one word).
    """
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "title_color": ("STRING", {"default": "#FFFFFF", "multiline": False}),
                "frame": (list(FRAME_MAP.keys()),),
                "art": ("IMAGE",),
                "attribute": (["none", "dark", "light", "earth", "wind", "water", "fire", "spell", "trap", "divine"],),
                "name": ("STRING", {"default": "Dark Magician", "multiline": False}),
                "level_rank": ("INT", {"default": 7, "min": 0, "max": 12}),
                "type": ("STRING", {"default": "[ Spellcaster / Normal ]", "multiline": False}),
                "effect": ("STRING", {"default": "The ultimate wizard in terms of attack and defense.", "multiline": True}),
                "atk_value": ("STRING", {"default": "2500"}),
                "def_value": ("STRING", {"default": "2100"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("card_image",)
    FUNCTION = "generate_card"
    CATEGORY = "Yu-Gi-Oh!"

    def generate_card(self, frame, art, attribute, name, level_rank, type, effect, atk_value, def_value, title_color="#FFFFFF"):
        return generate_yugioh_card_image(frame, art, attribute, name, level_rank, type, effect, atk_value, def_value, title_color)

NODE_CLASS_MAPPINGS = {
    "YuGiOhCardGenerator": YuGiOhCardGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "YuGiOhCardGenerator": "Yu-Gi-Oh! Card Generator"
}
