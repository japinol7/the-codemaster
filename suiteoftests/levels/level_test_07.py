"""Module level test 7."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_HEIGHT,
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    )
from codemaster.models.actors.items import platforms
from codemaster.models.actors.decorations import Water
from codemaster.models.actors.items import (
    DoorLeftGreen,
    DoorRightRed,
    )
from codemaster.levels.level_base import Level


class LevelTest7(Level):

    def __init__(self, id_, game):
        self.level_limit = -2700
        self.background = pg.image.load(self.file_name_im_get(2)).convert()
        self.player_start_pos_left = 250, 480
        self.player_start_pos_right = 600, 470
        self.player_start_pos_rtop = 300, 100
        self.player_start_pos_ltop = 80, 100

        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [[5, 100, 460, platforms.PLAT_TYPE_01],
                       [5, 300, 220, platforms.PLAT_TYPE_01],
                       [4, 980, 562, platforms.PLAT_TYPE_01],
                       [3, 1100, 260, platforms.PLAT_TYPE_01],
                       [9, 1906, 110, platforms.PLAT_TYPE_01],
                       [3, 1300, 120, platforms.PLAT_TYPE_01],
                       [8, 2580, 440, platforms.PLAT_TYPE_01],
                       [4, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
                       [44, 630, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
                       ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(
                platform[0], platform[1], platform[2], platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add water blocks
        Water.create_water(0, SCREEN_NEAR_EARTH + 206, self.game, qty=19, qty_depth=3)

        # Add moving platforms (type, x, y, ...)
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 1350, 510, self.game,
            border_left=1250, border_right=1650, change_x=2, level=self))
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 1600, 360, self.game,
            border_left=1350, border_right=2650, change_x=7, level=self))
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 950, 260, self.game,
            border_top=200, border_down=450, change_y=3, level=self))

        # Add sliding bands (n_blocs, x, y, type, velocity)
        level_plats = [[5, 280, SCREEN_HEIGHT - platforms.PLAT_TYPE_03_SLIDING_R_MID[3], platforms.PLAT_TYPE_03_SLIDING, 2],
                       ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(
                platform[0], platform[1], platform[2], platform[3], velocity=platform[4])
        for platform in plats:
            block = platforms.SlidingBands(platform[0], platform[1], platform[2],
                                           self.game, velocity=platform[3], level=self)
            self.platforms.add(block)

        # Add doors
        self.doors.add([
            DoorRightRed(3400, 550, self.game, level_dest=5, door_dest_pos=DOOR_DEST_NL, is_locked=True),
            DoorLeftGreen(2, 550, self.game, level_dest=7, door_dest_pos=DOOR_DEST_NL, is_locked=True),
            ])
