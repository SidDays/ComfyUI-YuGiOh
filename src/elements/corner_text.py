from PIL import Image, ImageDraw
from .base_element import CardElement
from ..utils import get_font
from ..config import get_layout_config, EXPECTED_WIDTH, EXPECTED_HEIGHT

class CornerTextElement(CardElement):
    def __init__(self, text):
        self.text = text

    def draw(self, image: Image.Image, draw: ImageDraw.ImageDraw):
        if not self.text:
            return
            
        W, H = image.size
        config = get_layout_config("series_10", "corner_text")
        
        ratio = min(W / EXPECTED_WIDTH, H / EXPECTED_HEIGHT)
        font_size = int(config["font_size"] * ratio)
        font = get_font(font_size, "MatrixBoldSmallCaps.otf")
        
        x = int(W * config["x"] / EXPECTED_WIDTH)
        y = int(H * config["y"] / EXPECTED_HEIGHT)
        
        draw.text((x, y), self.text, font=font, fill=(0, 0, 0))