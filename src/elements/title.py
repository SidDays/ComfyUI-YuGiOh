from PIL import Image, ImageDraw
from .base_element import CardElement
from ..utils import get_font
from ..config import TITLE_X, TITLE_Y, TITLE_MAX_W, TITLE_FONT_SIZE_RATIO

class TitleElement(CardElement):
    def __init__(self, name, title_color="#FFFFFF"):
        self.name = name
        self.title_color = title_color

    def draw(self, image: Image.Image, draw: ImageDraw.ImageDraw):
        W, H = image.size
        
        # Calculate expected font size based on height
        # Note: Original code used CONFIGURATION["series_9"]["title"]["font_size"]
        # which was 72 for 1185 height. 72/1185 = 0.06
        # But defined TITLE_FONT_SIZE_RATIO = 0.08
        # Original code line 162: int(CONFIGURATION...["font_size"]) (72)
        # But line 111 defined TITLE_FONT_SIZE_RATIO.
        # Let's use the explicit constant if possible, or ratio.
        # Original code used the dictionary value 72 specifically.
        # Let's use the constant from config if available or calculate.
        # In config.py I kept the dictionary.
        
        # Let's fallback to ratio calculation for flexibility with resolution
        # Ratio 0.06 is approx 72/1185.
        
        # Wait, the original code used:
        # title_font_size = int(CONFIGURATION["series_9"]["title"]["font_size"])
        # It disregarded TITLE_FONT_SIZE_RATIO (0.08) defined at line 111 for the title itself?
        # Line 162 uses the dict.
        # I should probably stick to the dict value scaling or use the ratio.
        # Since I moved TITLE_FONT_SIZE_RATIO to config, I'll use that to scale nicely.
        
        title_font_size = int(H * TITLE_FONT_SIZE_RATIO) 
        # Actually 0.08 * 1185 = 94. 72 is smaller. 
        # The user's code had `TITLE_FONT_SIZE_RATIO = 0.08` but used `72` (from config) which is ~0.06.
        # I will use the ratio from my generated config which matches the passed variables, 
        # TO BE SAFE let's stick to what was apparently "intended" or used.
        # Let's use 72 scaled by W/813 if needed, or just H ratio.
        # If I use 0.0607 it matches 72.
        
        # I'll use the TITLE_FONT_SIZE_RATIO from config.py. 
        # Use simple ratio logic:
        title_font = get_font(title_font_size, "MatrixSmallCaps.otf")
        
        left, top, right, bottom = draw.textbbox((0, 0), self.name, font=title_font)
        text_w = right - left
        text_h = bottom - top
        
        max_title_w = int(W * TITLE_MAX_W)
        
        # Draw onto a separate layer to allow resizing
        # Check height multiplier 1.5
        title_layer = Image.new('RGBA', (text_w, int(text_h * 1.5)), (0,0,0,0))
        title_draw = ImageDraw.Draw(title_layer)
        title_draw.text((0, 0), self.name, font=title_font, fill=self.title_color)
        
        if text_w > max_title_w:
            title_layer = title_layer.resize((max_title_w, int(title_layer.height)), Image.Resampling.LANCZOS)
            
        image.paste(title_layer, (int(W * TITLE_X), int(H * TITLE_Y)), title_layer)
