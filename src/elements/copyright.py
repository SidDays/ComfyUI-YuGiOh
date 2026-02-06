from PIL import Image, ImageDraw
from .base_element import CardElement
from ..utils import get_font
from ..config import get_layout_config, EXPECTED_WIDTH, EXPECTED_HEIGHT

class CopyrightElement(CardElement):
    def __init__(self, text):
        self.text = text

    def draw(self, image: Image.Image, draw: ImageDraw.ImageDraw):
        if not self.text:
            return
            
        W, H = image.size
        config = get_layout_config("series_10", "copyright")
        
        ratio = min(W / EXPECTED_WIDTH, H / EXPECTED_HEIGHT)
        font_size = int(config["font_size"] * ratio)
        font = get_font(font_size, "Stone Serif Regular.ttf")
        
        x = int(W * config["x"] / EXPECTED_WIDTH)
        y = int(H * config["y"] / EXPECTED_HEIGHT)
        
        max_width = int(W * config["w"] / EXPECTED_WIDTH)
        
        left, top, right, bottom = draw.textbbox((0, 0), self.text, font=font)
        text_w = right - left
        text_h = bottom - top
        
        title_layer = Image.new('RGBA', (text_w, text_h), (0,0,0,0))
        title_draw = ImageDraw.Draw(title_layer)
        title_draw.text((-left, -top), self.text, font=font, fill=(0, 0, 0))
        
        # Squish it to the width if it is larger than the max width
        #
        # TODO: If the text contains a copyright symbol, do not squish
        # the symbol, just the rest of the text
        if text_w > max_width:
            title_layer = title_layer.resize((max_width, text_h), Image.Resampling.LANCZOS)
            
        paste_x, paste_y = x, y
        anchor = config["anchor"]
        
        # TODO: Simplify anchor logic?
        if 'r' in anchor:
            paste_x -= title_layer.width
        elif anchor.startswith('m'):
            paste_x -= title_layer.width // 2
        if 'b' in anchor:
            paste_y -= title_layer.height
        elif anchor.endswith('m'):
            paste_y -= title_layer.height // 2
            
        image.paste(title_layer, (paste_x, paste_y), title_layer)
        