from PIL import Image, ImageDraw
from .base_element import CardElement
from ..utils import get_font
from ..config import EXPECTED_WIDTH, EXPECTED_HEIGHT, TITLE_MAX_W, LAYOUT_CONFIG

class TitleElement(CardElement):
    def __init__(self, name, title_color="#FFFFFF"):
        self.name = name
        self.title_color = title_color

    def draw(self, image: Image.Image, draw: ImageDraw.ImageDraw):
        W, H = image.size
        
        title_font_size = int(LAYOUT_CONFIG["series_9"]["title"]["font_size"])
        title_font = get_font(title_font_size, "MatrixSmallCaps.otf")

        left, top, right, bottom = draw.textbbox((0, 0), self.name, font=title_font)
        text_w = right - left
        text_h = bottom - top
        
        max_title_w = int(W * TITLE_MAX_W)
        
        # Draw onto a separate layer to allow resizing
        # Create a layer with the exact text dimensions.
        # The text is then drawn at an offset to account for glyphs that draw above or to the left of the origin.
        title_layer = Image.new('RGBA', (text_w, text_h), (0,0,0,0))
        title_draw = ImageDraw.Draw(title_layer)
        title_draw.text((-left, -top), self.name, font=title_font, fill=self.title_color)
        
        if text_w > max_title_w:
            title_layer = title_layer.resize((max_title_w, int(title_layer.height)), Image.Resampling.LANCZOS)
        
        title_x = int(LAYOUT_CONFIG["series_9"]["title"]["x"])
        title_y = int(LAYOUT_CONFIG["series_9"]["title"]["y"])
        
        image.paste(title_layer, (int(W * title_x / EXPECTED_WIDTH), int(H * title_y / EXPECTED_HEIGHT)), title_layer)
