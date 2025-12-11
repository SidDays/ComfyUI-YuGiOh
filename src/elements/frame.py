from PIL import Image
from ..utils import load_image, tensor_to_pil
from ..config import FRAME_MAP

def get_card_base_image(frame_input):
    """
    Resolves the frame input to a PIL Image.
    :param frame_input: Either a string key (e.g. 'effect', 'spell') or a Tensor/Image
    :return: PIL.Image
    """
    if isinstance(frame_input, str):
        # Use existing map or default
        rel_path = FRAME_MAP.get(frame_input, FRAME_MAP["effect"])
        return load_image(rel_path)
    else:
        # Assume tensor
        base = frame_input
        # If batch dimension > 1, take first? The original code did frame[0] if ndim > 3
        if hasattr(base, 'ndim') and base.ndim > 3:
             base = base[0]
        return tensor_to_pil(base)
