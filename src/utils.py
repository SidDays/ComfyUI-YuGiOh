import torch
import numpy as np
from PIL import Image, ImageFont
import os

def tensor_to_pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

def pil_to_tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

def get_root_dir():
    # current file is in src/utils.py, so root is two levels up
    return os.path.dirname(os.path.dirname(__file__))

def get_font(size, font_name="MatrixBook.ttf"):
    font_path = os.path.join(get_root_dir(), f"asset/font/{font_name}")
    try:
        return ImageFont.truetype(font_path, size=int(size))
    except IOError:
        print(f"Warning: Could not load font at {font_path}. Using default.")
        return ImageFont.load_default()

def load_image(relative_path):
    full_path = os.path.join(get_root_dir(), relative_path)
    return Image.open(full_path).convert("RGBA")
