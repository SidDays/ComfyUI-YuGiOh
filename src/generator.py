from PIL import ImageDraw
from .utils import pil_to_tensor
from .elements.frame import get_card_base_image
from .elements.artwork import ArtworkElement
from .elements.attribute import AttributeElement
from .elements.level import LevelElement
from .elements.title import TitleElement
from .elements.type_info import TypeInfoElement
from .elements.stats import StatsElement
from .elements.effect import EffectElement

def generate_yugioh_card_image(frame, art, attribute, name, level_rank, type, effect, atk_value, def_value, title_color):
    """
    Core logic to generate a Yu-Gi-Oh card image.
    Returns a Tensor as expected by ComfyUI.
    """
    # 1. Initialize Base Image (Frame)
    base_img = get_card_base_image(frame)
    
    # Create Draw Object
    draw = ImageDraw.Draw(base_img)
    
    # 2. Draw Elements sequentially
    elements = [
        TitleElement(name, title_color, attribute),
        AttributeElement(attribute),
        TypeInfoElement(type, frame),
        # IconElement(icon),
        LevelElement(level_rank),
        ArtworkElement(art),
        # PendulumScalesElement(pendulum_scale_blue, pendulum_scale_red, frame),
        # LinkMarkersElement(link_markers, frame),
        # CornerTextElement(corner_text)
        # SetIdElement(set_id)
        # EffectElement(effect)
        # StatsElement(atk_value, def_value, frame),
        # PasswordElement(password)
        # EditionElement(edition)
        # CopyrightElement(copyright)
        # StickerElement(sticker)
    ]
    
    for element in elements:
        element.draw(base_img, draw)
        
    return (pil_to_tensor(base_img),)
