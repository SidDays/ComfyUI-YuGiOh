import torch
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
import textwrap
import re
import os

class YuGiOhCardGenerator:
    """
    A custom node for ComfyUI to generate Yu-Gi-Oh style cards.
    Supports advanced formatting:
    - [Text]: Force line, compress if too long.
    - [[Text]]: Force line, justify (spread) to fill width.
    - {Text}: Non-breaking text (treat as one word).
    """
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "title_color": ("STRING", {"default": "#FFFFFF", "multiline": False}),
                "frame": (["effect", "spell"],),
                "art": ("IMAGE",),
                "attribute": (["none", "dark", "light", "earth", "wind", "water", "fire", "spell", "trap", "divine"],),
                "name": ("STRING", {"default": "Dark Magician", "multiline": False}),
                "level_rank": ("INT", {"default": 7, "min": 0, "max": 12}),
                "type": ("STRING", {"default": "[ Spellcaster / Normal ]", "multiline": False}),
                "effect": ("STRING", {"default": "The ultimate wizard in terms of attack and defense.", "multiline": True}),
                "atk_value": ("STRING", {"default": "2500"}),
                "def_value": ("STRING", {"default": "2100"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("card_image",)
    FUNCTION = "generate_card"
    CATEGORY = "Yu-Gi-Oh!"

    def tensor_to_pil(self, image):
        return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

    def pil_to_tensor(self, image):
        return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

    def generate_card(self, frame, art, attribute, name, level_rank, type, effect, atk_value, def_value, title_color="#FFFFFF"):
        
        # 1. Convert Input Tensors to PIL Images
        if isinstance(frame, str):
            frame_map = {
                "effect": "asset/image/frame/effect-s9.png",
                "spell": "asset/image/frame/spell-s11.png"
            }
            img_path = os.path.join(os.path.dirname(__file__), frame_map.get(frame, "asset/image/frame/effect-s9.png"))
            base_img = Image.open(img_path).convert("RGBA")
        else:
            base_img = self.tensor_to_pil(frame[0]) if frame.ndim > 3 else self.tensor_to_pil(frame)
        art_img = self.tensor_to_pil(art[0]) if art.ndim > 3 else self.tensor_to_pil(art)
        if isinstance(attribute, str):
            if attribute == "none":
                 attr_img = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
            else:
                attr_map = {
                    "dark": "asset/image/attribute/dark-cn.png",
                    "light": "asset/image/attribute/light-cn.png",
                    "trap": "asset/image/attribute/trap-cn.png",
                    "spell": "asset/image/attribute/spell-cn.png",
                    "earth": "asset/image/attribute/earth-cn.png",
                    "wind": "asset/image/attribute/wind-cn.png",
                    "water": "asset/image/attribute/water-cn.png",
                    "fire": "asset/image/attribute/fire-cn.png",
                    "divine": "asset/image/attribute/divine-cn.png"
                }
                attr_path = os.path.join(os.path.dirname(__file__), attr_map.get(attribute))
                attr_img = Image.open(attr_path).convert("RGBA")
        else:
            attr_img = self.tensor_to_pil(attribute[0]) if attribute.ndim > 3 else self.tensor_to_pil(attribute)
        # Hardcoded star icon loading
        star_path = os.path.join(os.path.dirname(__file__), "asset/image/star/level.png")
        star_img = Image.open(star_path).convert("RGBA")

        W, H = base_img.size
        
        # --- CONFIGURATION ---
        ART_X, ART_Y = 0.125, 0.21
        ART_W, ART_H = 0.75, 0.50
        TITLE_X, TITLE_Y = 0.05, 0.035
        TITLE_MAX_W = 0.78
        TITLE_FONT_SIZE_RATIO = 0.08  # Increased from 0.07
        ATTR_X, ATTR_Y = 0.84, 0.038
        ATTR_SIZE_RATIO = 0.11
        STAR_Y = 0.155
        STAR_SIZE_RATIO = 0.065
        STAR_SPACING = 0.065
        TYPE_X, TYPE_Y = 0.06, 0.81
        TYPE_FONT_SIZE_RATIO = 0.035
        DESC_X, DESC_Y = 0.065, 0.825 # Moved up slightly to give more room if needed
        DESC_W, DESC_H = 0.87, 0.14  # Increased height from 0.11
        DESC_FONT_SIZE_RATIO = 0.045 # Increased from 0.03
        STATS_Y = 0.94
        ATK_X, DEF_X = 0.65, 0.85
        STATS_FONT_SIZE_RATIO = 0.035
        
        # Helper to load font
        def get_font(size, font_name="MatrixBook.ttf"):
            font_path = os.path.join(os.path.dirname(__file__), f"asset/font/{font_name}")
            try:
                return ImageFont.truetype(font_path, size=int(size))
            except IOError:
                print(f"Warning: Could not load font at {font_path}. Using default.")
                return ImageFont.load_default()

        draw = ImageDraw.Draw(base_img)

        # 2. Composite Main Art
        target_art_w = int(W * ART_W)
        target_art_h = int(H * ART_H)
        art_resized = art_img.resize((target_art_w, target_art_h), Image.Resampling.LANCZOS)
        base_img.paste(art_resized, (int(W * ART_X), int(H * ART_Y)))

        # 3. Composite Attribute Icon
        target_attr_size = int(W * ATTR_SIZE_RATIO)
        attr_resized = attr_img.resize((target_attr_size, target_attr_size), Image.Resampling.LANCZOS)
        mask = attr_resized if attr_resized.mode == 'RGBA' else None
        base_img.paste(attr_resized, (int(W * ATTR_X), int(H * ATTR_Y)), mask)

        # 4. Composite Stars
        if level_rank > 0:
            target_star_size = int(W * STAR_SIZE_RATIO)
            star_resized = star_img.resize((target_star_size, target_star_size), Image.Resampling.LANCZOS)
            star_mask = star_resized if star_resized.mode == 'RGBA' else None
            total_star_width = (level_rank - 1) * (W * STAR_SPACING)
            start_x = (W / 2) - (total_star_width / 2) - (target_star_size / 2)
            for i in range(level_rank):
                x_pos = int(start_x + (i * W * STAR_SPACING))
                y_pos = int(H * STAR_Y)
                base_img.paste(star_resized, (x_pos, y_pos), star_mask)

        # 5. Draw Title
        title_font_size = int(H * TITLE_FONT_SIZE_RATIO)
        title_font = get_font(title_font_size, "MatrixBoldSmallCaps.otf")
        left, top, right, bottom = draw.textbbox((0, 0), name, font=title_font)
        text_w = right - left
        text_h = bottom - top
        max_title_w = int(W * TITLE_MAX_W)
        title_layer = Image.new('RGBA', (text_w, int(text_h * 1.5)), (0,0,0,0))
        title_draw = ImageDraw.Draw(title_layer)
        title_draw.text((0, 0), name, font=title_font, fill=title_color)
        if text_w > max_title_w:
            title_layer = title_layer.resize((max_title_w, int(title_layer.height)), Image.Resampling.LANCZOS)
        base_img.paste(title_layer, (int(W * TITLE_X), int(H * TITLE_Y)), title_layer)

        # 6. Draw Race / Type
        if frame == "spell":
            type_text = f"[ {type} ]"
            # Use specific font for spell format
            type_font = get_font(int(H * TYPE_FONT_SIZE_RATIO * 1.5), "YuGiOhITCStoneSerifBSc.ttf") 
            # Right align at top right
            t_left, t_top, t_right, t_bottom = draw.textbbox((0, 0), type_text, font=type_font)
            t_width = t_right - t_left
            # Position: Right-aligned near Attribute (X approx 0.82 relative to canvas width?)
            # The reference shows it effectively right aligned with the title bar end roughly.
            # Let's place it at roughly X=0.88 - text_width
            # And Y position just below the top header or aligned with it?
            # In anime style, it is often just below the main header line.
            # Let's approximate Y = 0.125
            spell_type_x = int(W * 0.88) - t_width
            spell_type_y = int(H * 0.128)
            draw.text((spell_type_x, spell_type_y), type_text, font=type_font, fill=(0,0,0))
        else:
            type_font = get_font(int(H * TYPE_FONT_SIZE_RATIO))
            draw.text((int(W * TYPE_X), int(H * TYPE_Y)), type, font=type_font, fill=(0,0,0))

        # 7. Draw Stats
        if frame != "spell": # Spells don't have ATK/DEF typically
             stats_font = get_font(int(H * STATS_FONT_SIZE_RATIO))
             draw.text((int(W * ATK_X), int(H * STATS_Y)), str(atk_value), font=stats_font, fill=(0,0,0))
             draw.text((int(W * DEF_X), int(H * STATS_Y)), str(def_value), font=stats_font, fill=(0,0,0))

        # 8. Draw Description (Advanced Typesetting)
        desc_x = int(W * DESC_X)
        desc_y = int(H * DESC_Y)
        max_desc_w = int(W * DESC_W)
        max_desc_h = int(H * DESC_H)

        # --- Typesetting Logic Helper Functions ---
        
        def parse_description(text):
            """Splits text into tokens: Justified, Compressed, NonBreaking, or Words."""
            # Regex to find [[...]], [...], or {...}
            # Priority: [[ first, then [, then {
            pattern = r"(\[\[.*?\]\]|\[.*?\]|\{.*?\})"
            parts = re.split(pattern, text)
            tokens = []
            
            for part in parts:
                if not part: continue
                
                if part.startswith('[[') and part.endswith(']]'):
                    tokens.append({'type': 'JUSTIFY', 'text': part[2:-2]})
                elif part.startswith('[') and part.endswith(']'):
                    tokens.append({'type': 'COMPRESS', 'text': part[1:-1]})
                elif part.startswith('{') and part.endswith('}'):
                    tokens.append({'type': 'NO_BREAK', 'text': part[1:-1]})
                else:
                    # Standard text, split by spaces but keep newlines manually if needed (not supported yet, assuming single block)
                    words = part.split(' ')
                    for w in words:
                        if w: tokens.append({'type': 'WORD', 'text': w})
            return tokens

        def layout_text(tokens, font, max_width):
            """Calculates lines based on font size and box width."""
            lines = []
            current_line = []
            current_width = 0
            space_w = font.getlength(" ")
            
            for token in tokens:
                t_type = token['type']
                text = token['text']
                
                if t_type in ['JUSTIFY', 'COMPRESS']:
                    # These force their own lines.
                    # 1. Flush current line if exists
                    if current_line:
                        lines.append({'type': 'NORMAL', 'content': current_line})
                        current_line = []
                        current_width = 0
                    
                    # 2. Add this special line
                    lines.append({'type': t_type, 'content': text})
                    
                else:
                    # WORD or NO_BREAK
                    # Calculate width of this token
                    token_w = font.getlength(text)
                    
                    # Check fit
                    # If this is the first word, no space needed. Otherwise add space_w.
                    added_w = token_w + (space_w if current_line else 0)
                    
                    if current_width + added_w <= max_width:
                        current_line.append(token)
                        current_width += added_w
                    else:
                        # Wrap
                        if current_line:
                            lines.append({'type': 'NORMAL', 'content': current_line})
                        
                        current_line = [token]
                        current_width = token_w
            
            if current_line:
                lines.append({'type': 'NORMAL', 'content': current_line})
                
            return lines

        # --- Dynamic Sizing Loop ---
        current_font_size = int(H * DESC_FONT_SIZE_RATIO)
        min_font_size = 8
        final_layout = []
        final_font = None
        line_height_px = 0
        
        tokens = parse_description(effect)
        
        while current_font_size >= min_font_size:
            temp_font = get_font(current_font_size)
            
            # 1. Calculate Layout
            calculated_lines = layout_text(tokens, temp_font, max_desc_w)
            
            # 2. Check Height
            # Get height of a generic character (e.g., 'A') to determine line height
            _, _, _, char_h = draw.textbbox((0,0), "Ag", font=temp_font)
            line_height_px = char_h + 2 # Padding
            
            total_h = len(calculated_lines) * line_height_px
            
            if total_h <= max_desc_h:
                final_layout = calculated_lines
                final_font = temp_font
                break
            
            current_font_size -= 1
            
        if final_font is None:
            # Fallback to min size
            final_font = get_font(min_font_size)
            final_layout = layout_text(tokens, final_font, max_desc_w)
            _, _, _, char_h = draw.textbbox((0,0), "Ag", font=final_font)
            line_height_px = char_h + 2

        # --- Rendering ---
        
        y_cursor = desc_y
        
        for line in final_layout:
            l_type = line['type']
            content = line['content'] # List of tokens for NORMAL, string for SPECIAL
            
            if l_type == 'NORMAL':
                # content is list of tokens
                # Join with spaces
                full_line_text = " ".join([t['text'] for t in content])
                draw.text((desc_x, y_cursor), full_line_text, font=final_font, fill=(0,0,0))
                
            elif l_type == 'COMPRESS':
                # Render text to temp image then resize
                text_str = content
                l, t, r, b = draw.textbbox((0,0), text_str, font=final_font)
                w_needed = r - l
                h_needed = (b - t) + 5 # Buffer
                
                # Create temp surface
                tmp = Image.new('RGBA', (int(w_needed), int(h_needed)), (0,0,0,0))
                d_tmp = ImageDraw.Draw(tmp)
                d_tmp.text((0,0), text_str, font=final_font, fill=(0,0,0))
                
                # Resize if wider than box
                if w_needed > max_desc_w:
                    tmp = tmp.resize((max_desc_w, int(h_needed)), Image.Resampling.LANCZOS)
                
                base_img.paste(tmp, (desc_x, y_cursor), tmp)

            elif l_type == 'JUSTIFY':
                # Distribute words
                words = content.split(' ')
                # Measure total width of words
                total_word_w = sum(final_font.getlength(w) for w in words)
                space_avail = max_desc_w - total_word_w
                
                # If content is wider than box, default to COMPRESS behavior
                if space_avail < 0:
                     # Fallback to Compress logic
                    text_str = content
                    l, t, r, b = draw.textbbox((0,0), text_str, font=final_font)
                    w_needed = r - l
                    h_needed = (b - t) + 5
                    tmp = Image.new('RGBA', (int(w_needed), int(h_needed)), (0,0,0,0))
                    d_tmp = ImageDraw.Draw(tmp)
                    d_tmp.text((0,0), text_str, font=final_font, fill=(0,0,0))
                    tmp = tmp.resize((max_desc_w, int(h_needed)), Image.Resampling.LANCZOS)
                    base_img.paste(tmp, (desc_x, y_cursor), tmp)
                else:
                    # Distribute spacing
                    if len(words) > 1:
                        gap = space_avail / (len(words) - 1)
                        curr_x = float(desc_x)
                        for w in words:
                            draw.text((int(curr_x), y_cursor), w, font=final_font, fill=(0,0,0))
                            curr_x += final_font.getlength(w) + gap
                    else:
                        # Single word, just draw
                        draw.text((desc_x, y_cursor), words[0], font=final_font, fill=(0,0,0))

            y_cursor += line_height_px

        return (self.pil_to_tensor(base_img),)

NODE_CLASS_MAPPINGS = {
    "YuGiOhCardGenerator": YuGiOhCardGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "YuGiOhCardGenerator": "Yu-Gi-Oh! Card Generator"
}
