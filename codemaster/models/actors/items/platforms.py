"""Module platforms."""
__author__ = 'Joan A. Pinol  (japinol)'

from collections import Counter
from os import path

import pygame as pg

from codemaster.config.constants import BITMAPS_FOLDER, FILE_NAMES
from codemaster.config.constants import VELOCITY_DEFAULT
from codemaster.utils.utils_graphics import SpriteSheet
from codemaster.models.actors.actor_types import ActorType, ActorBaseType, ActorCategoryType

PLAT_STD_WIDTH = 70
PLAT_STD_HEIGHT = 60
PLAT_STD_HEIGHT_2 = 40

# platform types  (X, Y, width, height, id) of sprite
PLAT_TYPE_01 = 1
PLAT_TYPE_02_STONE = 2
PLAT_TYPE_03_SLIDING = 3
PLAT_TYPE_05_EARTH = 5
PLAT_TYPE_05_EARTH_2SIZE = 6

PLAT_TYPE_01_LEFT = (0, 0, PLAT_STD_WIDTH, PLAT_STD_HEIGHT, 1)
PLAT_TYPE_01_MIDDLE = (72, 0, PLAT_STD_WIDTH, PLAT_STD_HEIGHT, 2)
PLAT_TYPE_01_RIGHT = (144, 0, PLAT_STD_WIDTH, PLAT_STD_HEIGHT, 3)
PLAT_TYPE_02_STONE_LEFT = (0, 129, PLAT_STD_WIDTH, PLAT_STD_HEIGHT_2, 4)
PLAT_TYPE_02_STONE_MIDDLE = (72, 129, PLAT_STD_WIDTH, PLAT_STD_HEIGHT_2, 5)
PLAT_TYPE_02_STONE_RIGHT = (144, 129, PLAT_STD_WIDTH, PLAT_STD_HEIGHT_2, 6)
PLAT_TYPE_03_SLIDING_R_MID = (0, 206, PLAT_STD_WIDTH, PLAT_STD_HEIGHT_2, 7)
PLAT_TYPE_03_SLIDING_L_MID = (72, 206, PLAT_STD_WIDTH, PLAT_STD_HEIGHT_2, 8)
PLAT_TYPE_05_EARTH_LEFT = (0, 248, 70, 124, 9)
PLAT_TYPE_05_EARTH_MIDDLE = (72, 248, 70, 124, 10)
PLAT_TYPE_05_EARTH_RIGHT = (144, 248, 70, 124, 11)
PLAT_TYPE_05_EARTH_MIDDLE_2Z = (216, 248, 140, 124, 12)


class Platform(pg.sprite.Sprite):
    type_id_count = Counter()
    sprite_images = {}

    def file_name_im_get(self, id_):
        return path.join(BITMAPS_FOLDER,
                         f"{FILE_NAMES['im_tiles_spritesheet'][0]}_{id_:02d}"
                         f".{FILE_NAMES['im_tiles_spritesheet'][1]}")

    def __init__(self, sprite_sheet_data, x, y, game):
        super().__init__()
        self.game = game
        self.player = game.player
        self.base_type = ActorBaseType.PLATFORM
        if not getattr(self, 'type', None):
            self.type = ActorType.PLATFORM_A
        Platform.type_id_count[self.type] += 1
        if self.type == ActorType.PLATFORM_A:
            self.id = f"{self.type.name}_{Platform.type_id_count[self.type]:07d}"
        else:
            self.id = f"{self.type.name}_{Platform.type_id_count[self.type]:05d}"
        self.category_type = ActorCategoryType.PLATFORM

        sprite_sheet_data_id = sprite_sheet_data[4]
        if not Platform.sprite_images.get(sprite_sheet_data_id):
            sprite_sheet = SpriteSheet(self.file_name_im_get(1))
            self.image = sprite_sheet.get_image(
                sprite_sheet_data[0],
                sprite_sheet_data[1],
                sprite_sheet_data[2],
                sprite_sheet_data[3])
            Platform.sprite_images[sprite_sheet_data_id] = self.image
        else:
            self.image = Platform.sprite_images[sprite_sheet_data_id]
        self.rect = self.image.get_rect()
        self.rect.x = x
        # TODO: Add modifier constant to change the screen resolution easily
        self.rect.y = y

    @staticmethod
    def sprite_sheet_data_for_n_blocks(blocks_qty, x, y, type, velocity=None):
        res = []
        if type == PLAT_TYPE_01:
            type_left = PLAT_TYPE_01_LEFT
            type_middle = PLAT_TYPE_01_MIDDLE
            type_right = PLAT_TYPE_01_RIGHT
        elif type == PLAT_TYPE_02_STONE:
            type_left = PLAT_TYPE_02_STONE_LEFT
            type_middle = PLAT_TYPE_02_STONE_MIDDLE
            type_right = PLAT_TYPE_02_STONE_RIGHT
        elif type == PLAT_TYPE_05_EARTH:
            type_left = PLAT_TYPE_05_EARTH_LEFT
            type_middle = PLAT_TYPE_05_EARTH_MIDDLE
            type_right = PLAT_TYPE_05_EARTH_RIGHT
        elif type == PLAT_TYPE_03_SLIDING:
            velocity = velocity or VELOCITY_DEFAULT
            if velocity < 0:
                type_left = PLAT_TYPE_03_SLIDING_L_MID
                type_middle = PLAT_TYPE_03_SLIDING_L_MID
                type_right = PLAT_TYPE_03_SLIDING_L_MID
            else:
                type_left = PLAT_TYPE_03_SLIDING_R_MID
                type_middle = PLAT_TYPE_03_SLIDING_R_MID
                type_right = PLAT_TYPE_03_SLIDING_R_MID
        if blocks_qty == 1:
            res = [[type_middle, x, y, velocity]]
        elif blocks_qty == 2:
            res = [[type_left, x, y, velocity]]
            res.append([type_right, x + type_left[2], y, velocity])
        elif blocks_qty > 2:
            res = [[type_left, x, y, velocity]]
            for i in range(blocks_qty - 2):
                res.append([type_middle, x + type_left[2] * (i + 1), y, velocity])
            res.append([type_right, x + type_left[2] * (blocks_qty - 1), y, velocity])
        return res


class MovingPlatform(Platform):

    def __init__(self, sprite_sheet_data, x, y, game, border_left=0, border_right=0,
                 border_top=0, border_down=0, change_x=0, change_y=0, level=None):
        self.type = ActorType.PLAT_MOVING
        super().__init__(sprite_sheet_data, x, y, game)
        self.border_left = border_left
        self.border_right = border_right
        self.border_top = border_top - level.world_shift_top - self.rect.height
        self.border_down = border_down - level.world_shift_top - self.rect.height
        self.change_x = change_x
        self.change_y = change_y
        self.level = level

    def update(self):
        self.rect.x += self.change_x
        hit = pg.sprite.collide_rect(self, self.player)
        if hit:
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                self.player.rect.left = self.rect.right

        self.rect.y += self.change_y
        hit = pg.sprite.collide_rect(self, self.player)
        if hit:
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom

        # Check the boundaries and see if we need to reverse direction.
        if self.rect.bottom - self.level.world_shift_top > self.border_down \
                or self.rect.top - self.level.world_shift_top < self.border_top:
            self.change_y *= -1
        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.border_left or cur_pos > self.border_right:
            self.change_x *= -1


class SlidingBands(Platform):

    def __init__(self, sprite_sheet_data, x, y, game, velocity=None, level=None):
        self.type = ActorType.PLAT_SLIDING
        super().__init__(sprite_sheet_data, x, y, game)
        self.level = level
        self.velocity = velocity

    def update(self):
        hit = pg.sprite.collide_rect(self, self.player)
        if hit:
            if self.velocity > 0:
                self.player.rect.right = self.rect.left
            elif self.velocity < 0:
                self.player.rect.left = self.rect.right
