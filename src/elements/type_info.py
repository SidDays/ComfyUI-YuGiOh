from PIL import Image, ImageDraw
from .base_element import CardElement
from ..utils import get_font
from ..config import get_layout_config, EXPECTED_WIDTH, EXPECTED_HEIGHT

class TypeInfoElement(CardElement):
    def __init__(self, type_text, frame_type):
        self.type_text = type_text
        self.frame_type = frame_type

    def _draw_spell_trap_type(self, image: Image.Image, draw: ImageDraw.ImageDraw):
        W, H = image.size
        ratio = W / EXPECTED_WIDTH
        display_text = f"[ {self.type_text} ]"
        # Use specific font for spell format
        spell_trap_type_config = get_layout_config("series_10", "spell_trap_type")
        font_size = int(spell_trap_type_config["font_size"] * ratio)
        type_font = get_font(font_size, "YuGiOhITCStoneSerifBSc.ttf")

        # Right align logic
        t_left, t_top, t_right, t_bottom = draw.textbbox((0, 0), display_text, font=type_font)
        t_width = t_right - t_left

        # SPELL_TYPE_X_REF is approx 0.88
        spell_type_x = int(ratio * spell_trap_type_config["x"]) - t_width
        spell_type_y = int(ratio * spell_trap_type_config["y"])

        draw.text((spell_type_x, spell_type_y), display_text, font=type_font, fill=(0,0,0))

    def draw(self, image: Image.Image, draw: ImageDraw.ImageDraw):
        self._draw_spell_trap_type(image, draw)
