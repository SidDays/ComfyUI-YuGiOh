from PIL import Image
from .base_element import CardElement
from ..utils import tensor_to_pil, load_image
from ..config import ATTRIBUTE_MAP, EXPECTED_WIDTH, get_layout_config

class AttributeElement(CardElement):
    def __init__(self, attribute_input):
        self.attribute = attribute_input

    def draw(self, image: Image.Image, draw):
        W, H = image.size
        ratio = W / EXPECTED_WIDTH
        layout = get_layout_config("series_10", "attribute")
        ATTR_X = layout["x"] * ratio 
        ATTR_Y = layout["y"] * ratio
        ATTR_SIZE = layout["size"] * ratio

        # Resolve attribute image
        if isinstance(self.attribute, str):
            if self.attribute == "none":
                 attr_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
            else:
                rel_path = ATTRIBUTE_MAP.get(self.attribute)
                if rel_path:
                    attr_img = load_image(rel_path)
                else:
                    # Fallback or error?
                    attr_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
        else:
            if hasattr(self.attribute, 'ndim') and self.attribute.ndim > 3:
                attr_img = tensor_to_pil(self.attribute[0])
            else:
                attr_img = tensor_to_pil(self.attribute)

        target_attr_size = int(ATTR_SIZE)
        attr_resized = attr_img.resize((target_attr_size, target_attr_size), Image.Resampling.LANCZOS)
        
        mask = attr_resized if attr_resized.mode == 'RGBA' else None
        image.paste(attr_resized, (int(ATTR_X), int(ATTR_Y)), mask)
