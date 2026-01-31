from PIL import Image
from .base_element import CardElement
from ..utils import tensor_to_pil
from ..config import getLayoutConfig, EXPECTED_WIDTH

class ArtworkElement(CardElement):
    def __init__(self, art_input):
        self.art_input = art_input

    def draw(self, image: Image.Image, draw):
        W, H = image.size
        ratio = W / EXPECTED_WIDTH
        
        # Resolve art input to PIL
        if hasattr(self.art_input, 'ndim') and self.art_input.ndim > 3:
            art_img = tensor_to_pil(self.art_input[0])
        else:
            art_img = tensor_to_pil(self.art_input)

        art_config = getLayoutConfig("series_10", "art")
        target_art_w = int(ratio * art_config["w"])
        target_art_h = int(ratio * art_config["h"])
        
        # Resize
        art_resized = art_img.resize((target_art_w, target_art_h), Image.Resampling.LANCZOS)
        
        # Paste
        image.paste(art_resized, (int(ratio * art_config["x"]), int(ratio * art_config["y"])))