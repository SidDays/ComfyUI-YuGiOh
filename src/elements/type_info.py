from PIL import Image, ImageDraw
from .base_element import CardElement
from ..utils import get_font
from ..config import LAYOUT_CONFIG, EXPECTED_WIDTH, EXPECTED_HEIGHT

class TypeInfoElement(CardElement):
    def __init__(self, type_text, frame_type):
        self.type_text = type_text
        self.frame_type = frame_type

    def _draw_spell_trap_type(self, image: Image.Image, draw: ImageDraw.ImageDraw):
        W, H = image.size
        ratio = W / EXPECTED_WIDTH
        display_text = f"[ {self.type_text} ]"
        # Use specific font for spell format
        font_size = int(LAYOUT_CONFIG["series_9"]["spell_trap_type"]["font_size"] * ratio)
        type_font = get_font(font_size, "YuGiOhITCStoneSerifBSc.ttf")

        # Right align logic
        t_left, t_top, t_right, t_bottom = draw.textbbox((0, 0), display_text, font=type_font)
        t_width = t_right - t_left

        # SPELL_TYPE_X_REF is approx 0.88
        spell_type_x = int(ratio * LAYOUT_CONFIG["series_9"]["spell_trap_type"]["x"]) - t_width
        spell_type_y = int(ratio * LAYOUT_CONFIG["series_9"]["spell_trap_type"]["y"])

        draw.text((spell_type_x, spell_type_y), display_text, font=type_font, fill=(0,0,0))

    def _draw_monster_type(self, image: Image.Image, draw: ImageDraw.ImageDraw):
        W, H = image.size
        ratio_w = W / EXPECTED_WIDTH
        ratio_h = H / EXPECTED_HEIGHT
        
        conf = LAYOUT_CONFIG["series_9"]["monster_type"]
        font_size = int(conf["font_size"] * ratio_w)
        type_font = get_font(font_size)
        
        x = int(conf["x"] * ratio_w)
        y = int(conf["y"] * ratio_h)
        draw.text((x, y), self.type_text, font=type_font, fill=(0,0,0))

    def draw(self, image: Image.Image, draw: ImageDraw.ImageDraw):
        if self.frame_type == "spell" or self.frame_type == "trap":
            self._draw_spell_trap_type(image, draw)
        else:
            self._draw_monster_type(image, draw)
