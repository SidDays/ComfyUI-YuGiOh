from PIL import Image, ImageDraw
from .base_element import CardElement
from ..utils import get_font
from ..config import ATK_X, DEF_X, STATS_Y, STATS_FONT_SIZE_RATIO

class StatsElement(CardElement):
    def __init__(self, atk_value, def_value, frame_type):
        self.atk = atk_value
        self.def_val = def_value
        self.frame_type = frame_type

    def draw(self, image: Image.Image, draw: ImageDraw.ImageDraw):
        if self.frame_type == "spell":
            return
            
        W, H = image.size
        stats_font = get_font(int(H * STATS_FONT_SIZE_RATIO))
        
        draw.text((int(W * ATK_X), int(H * STATS_Y)), str(self.atk), font=stats_font, fill=(0,0,0))
        draw.text((int(W * DEF_X), int(H * STATS_Y)), str(self.def_val), font=stats_font, fill=(0,0,0))
