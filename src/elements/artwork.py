from PIL import Image
from .base_element import CardElement
from ..utils import tensor_to_pil
from ..config import ART_X, ART_Y, ART_W, ART_H

class ArtworkElement(CardElement):
    def __init__(self, art_input):
        self.art_input = art_input

    def draw(self, image: Image.Image, draw):
        W, H = image.size
        
        # Resolve art input to PIL
        if hasattr(self.art_input, 'ndim') and self.art_input.ndim > 3:
            art_img = tensor_to_pil(self.art_input[0])
        else:
            art_img = tensor_to_pil(self.art_input)

        target_art_w = int(W * ART_W)
        target_art_h = int(H * ART_H)
        
        # Resize
        art_resized = art_img.resize((target_art_w, target_art_h), Image.Resampling.LANCZOS)
        
        # Paste
        image.paste(art_resized, (int(W * ART_X), int(H * ART_Y)))
