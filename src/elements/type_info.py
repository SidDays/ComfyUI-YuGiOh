from PIL import Image, ImageDraw
from .base_element import CardElement
from ..utils import get_font
from ..config import TYPE_X, TYPE_Y, TYPE_FONT_SIZE_RATIO, SPELL_TYPE_Y, SPELL_TYPE_X_REF

class TypeElement(CardElement):
    def __init__(self, type_text, frame_type):
        self.type_text = type_text
        self.frame_type = frame_type

    def draw(self, image: Image.Image, draw: ImageDraw.ImageDraw):
        W, H = image.size
        
        if self.frame_type == "spell":
            display_text = f"[ {self.type_text} ]"
            # Use specific font for spell format
            # Font size ratio * 1.5
            font_size = int(H * TYPE_FONT_SIZE_RATIO * 1.5)
            type_font = get_font(font_size, "YuGiOhITCStoneSerifBSc.ttf")
            
            # Right align logic
            t_left, t_top, t_right, t_bottom = draw.textbbox((0, 0), display_text, font=type_font)
            t_width = t_right - t_left
            
            # SPELL_TYPE_X_REF is approx 0.88
            spell_type_x = int(W * SPELL_TYPE_X_REF) - t_width
            spell_type_y = int(H * SPELL_TYPE_Y)
            
            draw.text((spell_type_x, spell_type_y), display_text, font=type_font, fill=(0,0,0))
        else:
            font_size = int(H * TYPE_FONT_SIZE_RATIO)
            type_font = get_font(font_size)
            draw.text((int(W * TYPE_X), int(H * TYPE_Y)), self.type_text, font=type_font, fill=(0,0,0))
