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

def generate_yugioh_card_image(series, frame, art, attribute, name, level_rank, type, icon, effect, atk_value, def_value, link_rating, link_markers, is_pendulum, pendulum_scale_blue, pendulum_scale_red, corner_text, set_id, password, edition, copyright,  json_input):
    """
    Core logic to generate a Yu-Gi-Oh card image.
    Returns a Tensor as expected by ComfyUI.
    """
    base_img = get_card_base_image(frame)
    
    draw = ImageDraw.Draw(base_img)
    
    elements = [
        TitleElement(name, attribute),
        AttributeElement(attribute),
        TypeInfoElement(type, frame),
        # IconElement(icon),
        LevelElement(level_rank),
        ArtworkElement(art),
        # PendulumScalesElement(pendulum_scale_blue, pendulum_scale_red, frame),
        # LinkMarkersElement(link_markers, frame),
        # CornerTextElement(corner_text),
        # SetIdElement(set_id),
        EffectElement(effect),
        StatsElement(atk_value, def_value, frame),
        # PasswordElement(password),
        # EditionElement(edition),
        # CopyrightElement(copyright),
        # StickerElement(sticker),
    ]
    
    for element in elements:
        element.draw(base_img, draw)
        
    return (pil_to_tensor(base_img),)
