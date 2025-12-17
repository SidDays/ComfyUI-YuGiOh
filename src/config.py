
# Card Layout Configuration

# Main Configuration Dictionary
LAYOUT_CONFIG = {
    "series_9": {
        "art": {
            "x": 0.125,
            "y": 0.21,
            "w": 0.75,
            "h": 0.50
        },
        "title": {
            "x": 60,
            "y": 69,
            "w": 607,
            "h": 60,
            "font_size": 78
        },
        "spell_trap_type": {
            "x": 733,
            "y": 146,
            "font_size": 43
        },
        "monster_type": {
            "x": 49,
            "y": 962,
            "font_size": 41
        }
    }
}

# Image Maps
FRAME_MAP = {
    "effect": "asset/image/frame/effect-s9.png",
    "spell": "asset/image/frame/spell-s11.png"
}

ATTRIBUTE_MAP = {
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

STAR_PATH = "asset/image/star/level.png"

# Dimensions and Ratios
EXPECTED_WIDTH = 813
EXPECTED_HEIGHT = 1185

# Normalized Coordinates (0.0 to 1.0 based on canvas size)

# Art
ART_X = 0.125
ART_Y = 0.21
ART_W = 0.75 # Used for sizing
ART_H = 0.50 # Used for sizing

# Title
TITLE_X = 0.05
TITLE_Y = 0.035
TITLE_MAX_W = 0.78
TITLE_FONT_SIZE_RATIO = 0.08

# Attribute
ATTR_X = 0.84
ATTR_Y = 0.038
ATTR_SIZE_RATIO = 0.11

# Stars / Level
STAR_Y = 0.155
STAR_SIZE_RATIO = 0.065
STAR_SPACING = 0.065

# Description / Effect
DESC_X = 0.065
DESC_Y = 0.825
DESC_W = 0.87
DESC_H = 0.14
DESC_FONT_SIZE_RATIO = 0.045

# Stats
STATS_Y = 0.94
ATK_X = 0.65
DEF_X = 0.85
STATS_FONT_SIZE_RATIO = 0.035
