"""Module utils_graphics."""
__author__ = 'Joan A. Pinol  (japinol)'

import os

import pygame as pg

from codemaster.utils.colors import Color
from codemaster.config import constants as consts
from codemaster.config.settings import Settings


FONT_DEFAULT_FIXED = False
chars_render = {}


class SpriteSheet:
    """ To grab images out of a sprite sheet. """
    sprite_sheet = None

    def __init__(self, file_name):
        self.sprite_sheet = pg.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger sprite sheet
            Pass in the x, y location of the sprite
            and its width and height.
        """
        image = pg.Surface([width, height]).convert()
        # Copy the sprite from the sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(Color.BLACK)
        return image


def full_screen_switch(game):
    Settings.is_full_screen = not Settings.is_full_screen
    game.screen = pg.display.set_mode(game.size,
                                      Settings.is_full_screen and game.full_screen_flags
                                      or game.normal_screen_flags)


def draw_text(text, x, y, screen, font_name=consts.FONT_DEFAULT_NAME, size=None,
              color=Color.YELLOW, align="topleft"):
    if not size:
        size = Settings.font_size1
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(**{align: (x, y)})
    screen.blit(text_surface, text_rect)


def draw_image(x, y, screen, surface_dic, surface_name, file_name, align="topleft",
               width=None, height=None, alpha_color=None):
    image = pg.image.load((os.path.join(consts.BITMAPS_FOLDER, file_name))).convert()
    if width and height:
        image = pg.transform.smoothscale(image, (width, height))
    if alpha_color:
        image.set_colorkey(alpha_color)
    rect = image.get_rect(**{align: (x, y)})
    surface_dic[surface_name] = (image, rect)
    screen.blit(image, rect)


def render_text(text, x, y, surface_dic, surface_name, font_name=consts.FONT_DEFAULT_NAME,
                size=None, color=Color.YELLOW, align="topleft"):
    if not size:
        size = Settings.font_size1
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(**{align: (x, y)})
    surface_dic[surface_name] = (text_surface, text_rect)


def render_text_tuple(text, x, y, surface_dic, surface_name, font_name=consts.FONT_DEFAULT_NAME,
                      size=None, color=Color.YELLOW, align="topleft"):
    if not size:
        size = Settings.font_size1
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(**{align: (x, y)})
    surface_dic[(surface_name, color)] = (text_surface, text_rect)


def chars_render_text_tuple():
    char_code_list = [x for x in range(32, 126)]
    for char_code in char_code_list:
        render_text_tuple(chr(char_code), 1, 1, chars_render, char_code, color=Color.GREEN)
    for char_code in char_code_list:
        render_text_tuple(chr(char_code), 1, 1, chars_render, char_code, color=Color.CYAN)
    for char_code in char_code_list:
        render_text_tuple(chr(char_code), 1, 1, chars_render, char_code, color=Color.YELLOW)
    for char_code in char_code_list:
        render_text_tuple(chr(char_code), 1, 1, chars_render, char_code, color=Color.RED)
    return


def draw_text_rendered(text, x, y, screen, color, space_btw_chars=None,
                       fixed_font=FONT_DEFAULT_FIXED):
    if not space_btw_chars:
        space_btw_chars = Settings.font_spc_btn_chars1
    xx = x
    for ch in text:
        if not chars_render.get((ord(ch), color)):
            ch = '-'
        screen.blit(chars_render[(ord(ch), color)][0], (xx, y))
        if not fixed_font:
            if ch != ' ':
                xx += space_btw_chars
            else:
                xx += space_btw_chars // 3


def draw_bar_graphic(surf, amount_pct, x, y, color_max=Color.GREEN,
                     color_med=Color.YELLOW, color_min=Color.RED,
                     bar_width=100, bar_height=15,
                     bar_outline=True, bar_up_line=False, bar_up_line_height=1):
    if amount_pct < 0:
        amount_pct = 0
    if bar_height < 5:
        bar_height = 5
    fill = amount_pct * bar_width
    fill_rect = pg.Rect(x, y, fill, bar_height)
    if amount_pct > 0.65:
        col = color_max
    elif amount_pct > 0.35:
        col = color_med
    else:
        col = color_min
    pg.draw.rect(surf, col, fill_rect)
    if bar_outline:
        outline_rect = pg.Rect(x, y, bar_width, bar_height)
        pg.draw.rect(surf, Color.WHITE, outline_rect, 2)
    elif bar_up_line:
        pg.draw.line(surf, Color.WHITE,
                     (int(x), int(y)),
                     (int(x + bar_width), int(y)),
                     int(bar_up_line_height))
