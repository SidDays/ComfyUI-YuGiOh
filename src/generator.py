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
from .elements.password import PasswordElement
from .elements.set_id import SetIdElement
from .elements.edition import EditionElement
from .elements.copyright import CopyrightElement
from .elements.corner_text import CornerTextElement

def generate_yugioh_card_image(series, frame, art, attribute, name, level_rank, type, icon, effect, atk_value, def_value, link_rating, link_markers, is_pendulum, pendulum_scale_blue, pendulum_scale_red, pendulum_effect, corner_text, set_id, password, edition, copyright, json_override):
    """
    Core logic to generate a Yu-Gi-Oh card image.
    Returns a Tensor as expected by ComfyUI.
    """
    base_img = get_card_base_image(frame)
    
    draw = ImageDraw.Draw(base_img)
    
    elements = [
        TitleElement(name, attribute),
        AttributeElement(attribute),
        # TypeInfoElement is now only for spell/trap here; Monster type is handled in EffectElement
        TypeInfoElement(type, frame) if frame in ["spell", "trap"] else None,
        # IconElement(icon),
        LevelElement(level_rank),
        ArtworkElement(art),
        # PendulumElement(pendulum_scale_blue, pendulum_scale_red, pendulum_effect, frame),
        # LinkMarkersElement(link_markers, frame),
        CornerTextElement(corner_text),
        SetIdElement(set_id),
        EffectElement(effect, type, frame),
        StatsElement(atk_value, def_value, frame),
        PasswordElement(password),
        EditionElement(edition),
        CopyrightElement(copyright),
        # StickerElement(sticker),
    ]
    
    # Filter out None elements
    elements = [e for e in elements if e is not None]
    
    for element in elements:
        element.draw(base_img, draw)
        
    return (pil_to_tensor(base_img),)
