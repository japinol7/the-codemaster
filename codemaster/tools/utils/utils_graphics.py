"""Module utils_graphics."""
__author__ = 'Joan A. Pinol  (japinol)'

import os

import pygame as pg

from codemaster.tools.utils.colors import Color
from codemaster.config import constants as consts
from codemaster.config.settings import Settings


FONT_DEFAULT_FIXED = False
chars_render = {}
chars_fixed_render = {}


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


def image_change_scale_smooth(image):
    return pg.transform.smoothscale(
        image,
        (int(image.get_rect().width * Settings.screen_scale),
         int(image.get_rect().height * Settings.screen_scale)))


def image_change_scale(image):
    return pg.transform.scale(
        image,
        (int(image.get_rect().width * Settings.screen_scale),
         int(image.get_rect().height * Settings.screen_scale)))


def screen_change_scale(game):
    game.screen.blit(pg.transform.scale(
        game.screen,
        (int(Settings.screen_width * Settings.screen_scale),
         int(Settings.screen_height * Settings.screen_scale))
         ),
        (0, 0))


def full_screen_switch(game):
    Settings.is_full_screen = not Settings.is_full_screen
    game.screen = pg.display.set_mode(
        game.size,
        Settings.is_full_screen and game.full_screen_flags or game.normal_screen_flags)


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


def render_text_tuple(text, x, y, surface_dic, surface_name, font_name=consts.FONT_FIXED_DEFAULT_NAME,
                      size=None, color=Color.YELLOW, align="topleft"):
    if not size:
        size = Settings.font_size1
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(**{align: (x, y)})
    surface_dic[(surface_name, color)] = (text_surface, text_rect)


def chars_render_text_tuple(font_name=consts.FONT_FIXED_DEFAULT_NAME):
    ch_render = chars_render if font_name != consts.FONT_FIXED_DEFAULT_NAME else chars_fixed_render
    char_code_list = [x for x in range(32, 126)]
    for char_code in char_code_list:
        render_text_tuple(chr(char_code), 1, 1, ch_render, char_code, color=Color.GREEN, font_name=font_name)
    for char_code in char_code_list:
        render_text_tuple(chr(char_code), 1, 1, ch_render, char_code, color=Color.CYAN, font_name=font_name)
    for char_code in char_code_list:
        render_text_tuple(chr(char_code), 1, 1, ch_render, char_code, color=Color.YELLOW, font_name=font_name)
    for char_code in char_code_list:
        render_text_tuple(chr(char_code), 1, 1, ch_render, char_code, color=Color.RED, font_name=font_name)


def draw_text_rendered(text, x, y, screen, color, is_font_fixed=False,
                       space_btw_chars=None, space_btw_words=None):
    ch_render = chars_render if not is_font_fixed else chars_fixed_render
    if not space_btw_chars:
        space_btw_chars = Settings.font_spc_btn_chars1
    xx = x
    for ch in text:
        if not ch_render.get((ord(ch), color)):
            ch = '-'
        screen.blit(ch_render[(ord(ch), color)][0], (xx, y))
        if ch != ' ':
            xx += space_btw_chars
        else:
            if space_btw_words:
                xx += space_btw_words
            else:
                xx += space_btw_chars // 3


def draw_text_multi_lines_rendered(
        text, x, y, screen, color, is_font_fixed=False,
        space_btw_chars=None, space_btw_words=None, space_btw_lines=None):

    for i, txt in enumerate(text.splitlines()):
        ch_render = chars_render if not is_font_fixed else chars_fixed_render
        if not space_btw_chars:
            space_btw_chars = Settings.font_spc_btn_chars1
        xx = x
        for ch in txt:
            if not ch_render.get((ord(ch), color)):
                ch = '-'
            screen.blit(ch_render[(ord(ch), color)][0], (xx, y + (space_btw_lines * i)))
            if ch != ' ':
                xx += space_btw_chars
            else:
                if space_btw_words:
                    xx += space_btw_words
                else:
                    xx += space_btw_chars // 3


def draw_bar_graphic_outline(
        surf, amount_pct, x, y, color_max=Color.GREEN,
         color_med=Color.YELLOW, color_min=Color.RED,
         bar_width=100, bar_height=15):
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
    outline_rect = pg.Rect(x, y, bar_width, bar_height)
    pg.draw.rect(surf, Color.WHITE, outline_rect, 2)


def draw_bar_graphic(
        surf, amount_pct, x, y, color_max=Color.GREEN,
        color_med=Color.YELLOW, color_min=Color.RED,
        bar_width=100, bar_height=15,
        bar_up_line_height=1):
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
    pg.draw.line(
        surf, Color.WHITE,
         (int(x), int(y)),
         (int(x + bar_width), int(y)),
         int(bar_up_line_height))


def create_circle_surface(radius, color):
    surface = pg.Surface((radius * 2, radius * 2))
    pg.draw.circle(surface, color, (radius, radius), radius)
    surface.set_colorkey(Color.BLACK)
    return surface


def create_circle_in_surface(surface, color, center, radius):
    circle_surface = pg.Surface((radius * 2, radius * 2))
    pg.draw.circle(circle_surface, color, (radius, radius), radius)
    surface.blit(circle_surface, center)


def create_circle_surface_cached(radius, color, surface_renders):
    radius_rounded = int(radius)
    color_hash = hash(color)
    if surface_renders.get((radius_rounded, color_hash)):
        return surface_renders[(radius_rounded, color_hash)]

    surface = pg.Surface((radius * 2, radius * 2))
    pg.draw.circle(surface, color, (radius, radius), radius)
    surface.set_colorkey(Color.BLACK)
    surface_renders[(radius_rounded, color_hash)] = surface
    return surface


def create_circle_in_surface_cached(surface, color, position, radius, surface_renders):
    circle_surface = create_circle_surface_cached(radius, color, surface_renders)
    surface.blit(circle_surface, position)


def draw_circle(surface, color, center, radius):
    pg.draw.circle(surface, color, center, radius)
    return surface


def point_to_str(point):
    return f"{point[0]};{point[1]}"


def str_to_point(string):
    return [int(v) for v in string.split(";")[:2]]


def set_mask_alpha(surface, alpha_color):
    return multiply_color_on_surface(surface, alpha_color)


def multiply_color_on_surface(surface, color):
    base_surface = surface.copy()
    base_surface.fill(color)
    new_surface = surface.copy()
    new_surface.blit(base_surface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
    return new_surface


def get_chunk(point, chunk_size):
    return [point[0] // chunk_size, point[1] // chunk_size]


def draw_grid(screen, cell_size, screen_width, screen_height, screen_near_top, color):
    for x in range(0, screen_width, cell_size):
        pg.draw.line(screen, color, (x, screen_near_top), (x, screen_height))
    for y in range(screen_near_top, screen_height, cell_size):
        pg.draw.line(screen, color, (0, y), (screen_width, y))
