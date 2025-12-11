from PIL import Image
from .base_element import CardElement
from ..utils import load_image
from ..config import STAR_PATH, STAR_SIZE_RATIO, STAR_SPACING, STAR_Y

class LevelElement(CardElement):
    def __init__(self, level_rank):
        self.level_rank = level_rank

    def draw(self, image: Image.Image, draw):
        if self.level_rank <= 0:
            return

        W, H = image.size
        
        # Reuse global star loading or load per draw? 
        # Caching might be better but for now load per draw is safer/simpler
        star_img = load_image(STAR_PATH)

        target_star_size = int(W * STAR_SIZE_RATIO)
        star_resized = star_img.resize((target_star_size, target_star_size), Image.Resampling.LANCZOS)
        star_mask = star_resized if star_resized.mode == 'RGBA' else None
        
        total_star_width = (self.level_rank - 1) * (W * STAR_SPACING)
        start_x = (W / 2) - (total_star_width / 2) - (target_star_size / 2)
        
        for i in range(self.level_rank):
            x_pos = int(start_x + (i * W * STAR_SPACING))
            y_pos = int(H * STAR_Y)
            image.paste(star_resized, (x_pos, y_pos), star_mask)
