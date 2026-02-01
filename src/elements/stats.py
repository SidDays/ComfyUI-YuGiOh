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
        W, H = image.size
        
        stats_config = getLayoutConfig("series_10", "stats")
        separator_config = getLayoutConfig("series_10", "effect_stats_separator")

        if (self.atk == "" and self.def_val == ""):
            return
        
        sep_x = int(W * separator_config["x"] / EXPECTED_WIDTH)
        sep_y = int(H * separator_config["y"] / EXPECTED_HEIGHT)
        sep_w = int(W * separator_config["width"] / EXPECTED_WIDTH)
        sep_h = int(H * separator_config["height"] / EXPECTED_HEIGHT)
        draw.rectangle((sep_x, sep_y, sep_x + sep_w, sep_y + sep_h), fill=(0,0,0))

        stats_font = get_font(int(stats_config["font_size"]), font_name="MatrixBoldFractions.otf")
        stats_label_font = get_font(int(stats_config["font_size"]), font_name="MatrixBoldSmallCaps.otf")
        
        stats_atk_label_x = int(W * stats_config["atk_label_x"] / EXPECTED_WIDTH)
        stats_atk_x = int(W * stats_config["atk_x"] / EXPECTED_WIDTH)
        stats_def_label_x = int(W * stats_config["def_label_x"] / EXPECTED_WIDTH)
        stats_def_x = int(W * stats_config["def_x"] / EXPECTED_WIDTH)
        stats_y = int(H * stats_config["y"] / EXPECTED_HEIGHT)
        
        atk_label_str = "ATK /"
        draw.text((stats_atk_label_x, stats_y), atk_label_str, font=stats_label_font, fill=(0,0,0))
        
        atk_str = str(self.atk)
        draw.text((stats_atk_x, stats_y), atk_str, font=stats_font, fill=(0,0,0), anchor="ra")
        
        def_label_str = "DEF /"
        draw.text((stats_def_label_x, stats_y), def_label_str, font=stats_label_font, fill=(0,0,0))
        
        def_str = str(self.def_val)
        draw.text((stats_def_x, stats_y), def_str, font=stats_font, fill=(0,0,0), anchor="ra")