import re
from PIL import Image, ImageDraw
from .base_element import CardElement
from ..utils import get_font
from ..config import DESC_X, DESC_Y, DESC_W, DESC_H, DESC_FONT_SIZE_RATIO

def parse_description(text):
    """Splits text into tokens: Justified, Compressed, NonBreaking, or Words."""
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
            if current_line:
                lines.append({'type': 'NORMAL', 'content': current_line})
                current_line = []
                current_width = 0
            lines.append({'type': t_type, 'content': text})
            
        else:
            token_w = font.getlength(text)
            added_w = token_w + (space_w if current_line else 0)
            
            if current_width + added_w <= max_width:
                current_line.append(token)
                current_width += added_w
            else:
                if current_line:
                    lines.append({'type': 'NORMAL', 'content': current_line})
                current_line = [token]
                current_width = token_w
    
    if current_line:
        lines.append({'type': 'NORMAL', 'content': current_line})
        
    return lines

class EffectElement(CardElement):
    def __init__(self, effect_text):
        self.effect = effect_text

    def draw(self, image: Image.Image, draw: ImageDraw.ImageDraw):
        W, H = image.size
        
        desc_x = int(W * DESC_X)
        desc_y = int(H * DESC_Y)
        max_desc_w = int(W * DESC_W)
        max_desc_h = int(H * DESC_H)
        
        # Determine Font Size
        current_font_size = int(H * DESC_FONT_SIZE_RATIO)
        min_font_size = 8
        final_layout = []
        final_font = None
        line_height_px = 0
        
        tokens = parse_description(self.effect)
        
        while current_font_size >= min_font_size:
            temp_font = get_font(current_font_size)
            calculated_lines = layout_text(tokens, temp_font, max_desc_w)
            
            _, _, _, char_h = draw.textbbox((0,0), "Ag", font=temp_font)
            line_height_px = char_h + 2 # Padding
            
            total_h = len(calculated_lines) * line_height_px
            
            if total_h <= max_desc_h:
                final_layout = calculated_lines
                final_font = temp_font
                break
            
            current_font_size -= 1
            
        if final_font is None:
            final_font = get_font(min_font_size)
            final_layout = layout_text(tokens, final_font, max_desc_w)
            _, _, _, char_h = draw.textbbox((0,0), "Ag", font=final_font)
            line_height_px = char_h + 2

        # Render
        y_cursor = desc_y
        
        for line in final_layout:
            l_type = line['type']
            content = line['content']
            
            if l_type == 'NORMAL':
                full_line_text = " ".join([t['text'] for t in content])
                draw.text((desc_x, y_cursor), full_line_text, font=final_font, fill=(0,0,0))
                
            elif l_type == 'COMPRESS':
                text_str = content
                l, t, r, b = draw.textbbox((0,0), text_str, font=final_font)
                w_needed = r - l
                h_needed = (b - t) + 5
                
                tmp = Image.new('RGBA', (int(w_needed), int(h_needed)), (0,0,0,0))
                d_tmp = ImageDraw.Draw(tmp)
                d_tmp.text((0,0), text_str, font=final_font, fill=(0,0,0))
                
                if w_needed > max_desc_w:
                    tmp = tmp.resize((max_desc_w, int(h_needed)), Image.Resampling.LANCZOS)
                
                image.paste(tmp, (desc_x, y_cursor), tmp)

            elif l_type == 'JUSTIFY':
                words = content.split(' ')
                total_word_w = sum(final_font.getlength(w) for w in words)
                space_avail = max_desc_w - total_word_w
                
                if space_avail < 0:
                    # Fallback to Compress
                    text_str = content
                    l, t, r, b = draw.textbbox((0,0), text_str, font=final_font)
                    w_needed = r - l
                    h_needed = (b - t) + 5
                    tmp = Image.new('RGBA', (int(w_needed), int(h_needed)), (0,0,0,0))
                    d_tmp = ImageDraw.Draw(tmp)
                    d_tmp.text((0,0), text_str, font=final_font, fill=(0,0,0))
                    tmp = tmp.resize((max_desc_w, int(h_needed)), Image.Resampling.LANCZOS)
                    image.paste(tmp, (desc_x, y_cursor), tmp)
                else:
                    if len(words) > 1:
                        gap = space_avail / (len(words) - 1)
                        curr_x = float(desc_x)
                        for w in words:
                            draw.text((int(curr_x), y_cursor), w, font=final_font, fill=(0,0,0))
                            curr_x += final_font.getlength(w) + gap
                    else:
                        draw.text((desc_x, y_cursor), words[0], font=final_font, fill=(0,0,0))

            y_cursor += line_height_px
