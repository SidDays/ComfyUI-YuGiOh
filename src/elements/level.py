from PIL import Image
from .base_element import CardElement
from ..utils import load_image
from ..config import LAYOUT_CONFIG,STAR_PATH

class LevelElement(CardElement):
    def __init__(self, level_rank):
        self.level_rank = level_rank

    def draw(self, image: Image.Image, draw):
        if self.level_rank <= 0:
            return

        W, H = image.size
        
        STAR_CONFIG = LAYOUT_CONFIG["series_9"]["level_stars"]
        
        # Reuse global star loading or load per draw? 
        # Caching might be better but for now load per draw is safer/simpler
        star_img = load_image(STAR_PATH)

        target_star_size = int(STAR_CONFIG["star_size"])
        star_resized = star_img.resize((target_star_size, target_star_size), Image.Resampling.LANCZOS)
        star_mask = star_resized if star_resized.mode == 'RGBA' else None
        
        start_x = int(STAR_CONFIG["anchor_x"])
        start_y = int(STAR_CONFIG["anchor_y"])
        
        # Right-align stars from anchor point (top right)
        # Calculate spacing between stars
        star_spacing = int(STAR_CONFIG["star_spacing"])
        
        for i in range(self.level_rank):
            # Position stars right-to-left: rightmost star at anchor_x
            x_pos = int(start_x - (self.level_rank - i) * target_star_size - (self.level_rank - i - 1) * star_spacing)
            y_pos = int(start_y)
            image.paste(star_resized, (x_pos, y_pos), star_mask)
