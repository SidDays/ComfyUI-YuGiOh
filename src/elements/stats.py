from PIL import Image, ImageDraw
from .base_element import CardElement
from ..utils import get_font
from ..config import getLayoutConfig, EXPECTED_WIDTH, EXPECTED_HEIGHT

class StatsElement(CardElement):
    def __init__(self, atk_value, def_value, frame_type):
        self.atk = atk_value
        self.def_val = def_value
        self.frame_type = frame_type

    def draw(self, image: Image.Image, draw: ImageDraw.ImageDraw):
        if self.frame_type == "spell":
            return
            
        W, H = image.size
        
        
        stats_config = getLayoutConfig("series_10", "stats")

        if self.atk is not None or self.def_val is not None:
            sep_x = int(W * stats_config["separator_x"] / EXPECTED_WIDTH)
            sep_y = int(H * stats_config["separator_y"] / EXPECTED_HEIGHT)
            sep_w = int(W * stats_config["separator_width"] / EXPECTED_WIDTH)
            sep_h = int(H * stats_config["separator_height"] / EXPECTED_HEIGHT)
            draw.rectangle((sep_x, sep_y, sep_x + sep_w, sep_y + sep_h), fill=(0,0,0))

        stats_font = get_font(int(stats_config["font_size"]), font_name="MatrixBoldFractions.otf")
        stats_label_font = get_font(int(stats_config["font_size"]), font_name="MatrixBoldSmallCaps.otf")
        
        stats_atk_label_x = int(W * stats_config["atk_label_x"] / EXPECTED_WIDTH)
        stats_atk_x = int(W * stats_config["atk_x"] / EXPECTED_WIDTH)
        stats_def_label_x = int(W * stats_config["def_label_x"] / EXPECTED_WIDTH)
        stats_def_x = int(W * stats_config["def_x"] / EXPECTED_WIDTH)
        stats_y = int(H * stats_config["y"] / EXPECTED_HEIGHT)
        
        atk_label_str = "ATK /"
        atk_str = str(self.atk)
        
        def_label_str = "DEF /"
        def_str = str(self.def_val)
        

        l, t, r, b = draw.textbbox((0, 0), atk_str, font=stats_font)
        atk_w = r - l
        l, t, r, b = draw.textbbox((0, 0), def_str, font=stats_font)
        def_w = r - l
        
        draw.text((stats_atk_label_x, stats_y), atk_label_str, font=stats_label_font, fill=(0,0,0))
        draw.text((stats_atk_x - atk_w, stats_y), atk_str, font=stats_font, fill=(0,0,0))
        draw.text((stats_def_label_x, stats_y), def_label_str, font=stats_label_font, fill=(0,0,0))
        draw.text((stats_def_x - def_w, stats_y), def_str, font=stats_font, fill=(0,0,0))