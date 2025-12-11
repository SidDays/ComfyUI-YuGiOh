from abc import ABC, abstractmethod
from PIL import Image, ImageDraw

class CardElement(ABC):
    @abstractmethod
    def draw(self, image: Image.Image, draw: ImageDraw.ImageDraw):
        """
        Draws this element onto the provided image.
        :param image: The PIL Image object (canvas)
        :param draw: The ImageDraw object for the canvas
        """
        pass
