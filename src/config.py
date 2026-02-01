from typing import Literal, List

# Card Layout Configuration

SeriesName = Literal["series_10"]

LAYOUTS: List[SeriesName] = [
    "series_10",
]

# FONT_MAP = {
#     "Matrix Book": "asset/font/MatrixBook.ttf",
#     "ITC Stone Serif Bold Small Caps": "asset/font/YuGiOhITCStoneSerifBSc.ttf",
# }

# Main Configuration Dictionary
LAYOUT_CONFIG = {
    "series_10": {
        "art": {
            "x": 100,
            "y": 219,
            "w": 614,
            "h": 614
        },
        "title": {
            "x": 60,
            "y": 69,
            "w_attribute": 607,
            "w_full": 687,
            "h": 60,
            "font_size": 78,
        },
        "attribute": {
            "x": 680,
            "y": 57,
            "size": 72
        },
        "spell_trap_type": {
            "x": 733,
            "y": 146,
            "font_size": 43
        },
        "monster_type": {
            "x": 62,
            "y": 887,
            "font_size": 33
        },
        "level_rank": {
            "anchor_x": 729,
            "anchor_y": 145,
            "star_size": 49,
            "star_spacing": 5
        },
        "stats": {
            "atk_x": 515,
            "def_x": 686,
            "y": 1075,
            "font_size": 36
        }
    }
}

def getLayoutConfig(series_name: SeriesName, element_name):
    return LAYOUT_CONFIG[series_name][element_name]

# Image Maps
FRAME_MAP = {
    "darksynchro": "asset/image/frame/series-10/darksynchro.png",
    "effect": "asset/image/frame/series-10/effect.png",
    "fusion": "asset/image/frame/series-10/fusion.png",
    "link": "asset/image/frame/series-10/link.png",
    "normal": "asset/image/frame/series-10/normal.png",
    "ritual": "asset/image/frame/series-10/ritual.png",
    "spell": "asset/image/frame/series-10/spell.png",
    "synchro": "asset/image/frame/series-10/synchro.png",
    "token": "asset/image/frame/series-10/token.png",
    "trap": "asset/image/frame/series-10/trap.png",
    "xyz": "asset/image/frame/series-10/xyz.png"
}

ATTRIBUTE_MAP = {
    "none": "",
    "dark": "asset/image/attribute/cn/dark.png",
    "light": "asset/image/attribute/cn/light.png",
    "trap": "asset/image/attribute/cn/trap.png",
    "spell": "asset/image/attribute/cn/spell.png",
    "earth": "asset/image/attribute/cn/earth.png",
    "wind": "asset/image/attribute/cn/wind.png",
    "water": "asset/image/attribute/cn/water.png",
    "fire": "asset/image/attribute/cn/fire.png",
    "divine": "asset/image/attribute/cn/divine.png"
}

ICONS_MAP = {
    "none": "",
    "continuous": "asset/image/icon/continuous.png",
    "equip": "asset/image/icon/equip.png",
    "field": "asset/image/icon/field.png",
    "quick-play": "asset/image/icon/quick-play.png",
    "ritual": "asset/image/icon/ritual.png",
    "counter": "asset/image/icon/counter.png",
}

STAR_PATH = "asset/image/star/level.png"

# Dimensions and Ratios
EXPECTED_WIDTH = 813
EXPECTED_HEIGHT = 1185

# Normalized Coordinates (0.0 to 1.0 based on canvas size)

# Description / Effect
DESC_X = 0.065
DESC_Y = 0.825
DESC_W = 0.87
DESC_H = 0.14
DESC_FONT_SIZE_RATIO = 0.045
