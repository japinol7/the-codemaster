"""Module colors."""
__author__ = 'Joan A. Pinol  (japinol)'

from enum import Enum


class ColorName(Enum):
    """Defines some color names."""
    NONE = 0
    BLACK = 1
    WHITE = 255
    RED = 2
    GREEN = 3
    BLUE = 4
    YELLOW = 5
    CYAN = 6
    BLUE_VIOLET = 7
    BRICK = 8
    BROWN = 9
    PINK = 10
    AQUA = 11
    AZURE = 12
    GOLD = 13
    GOLDEN_ROD = 14
    GRAY = 15
    GRAY10 = 16
    GRAY15 = 17
    GRAY30 = 18


class Color:
    """Defines some colors."""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 238, 238)
    BLUE_VIOLET = (138, 43, 226)
    BRICK = (156, 102, 31)
    BROWN = (165, 42, 42)
    PINK = (255, 192, 203)
    AQUA = (0, 255, 255)
    AZURE = (240, 255, 255)
    GOLD = (255, 215, 0)
    GOLDEN_ROD = (218, 165, 32)
    GRAY = (128, 128, 128)
    GRAY10 = (28, 28, 28)
    GRAY15 = (38, 38, 38)
    GRAY30 = (77, 77, 77)
