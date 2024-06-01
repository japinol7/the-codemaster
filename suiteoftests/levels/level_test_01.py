"""Module level test 1."""
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
    ComputerA,
    DoorLeftGreen,
    DoorRightYellow,
    FilesDiskB,
    FilesDiskC,
    )
from codemaster.levels.level_base import Level


class LevelTest1(Level):

    def __init__(self, game):
        super().__init__(game)
        self.id = 0
        self.name = str(self.id + 1)
        self.next_level_left = False
        self.next_level_right = False
        self.next_level_top = False
        self.next_level_bottom = False
        self.background = pg.image.load(self.file_name_im_get(11)).convert()
        self.level_limit = -2700
        self.level_limit_top = -1000
        self.player_start_pos_left = 250, 480
        self.player_start_pos_right = 600, 470
        self.player_start_pos_rtop = 300, 100
        self.player_start_pos_ltop = 80, 100
        self.player_start_pos_bottom = 300, 800
        self.world_start_pos_left = 0, -758
        self.world_start_pos_right = self.level_limit + self.SCROLL_LV_NEAR_RIGHT_SIDE, -758
        self.world_start_pos_rtop = self.level_limit + 500 + self.SCROLL_LV_NEAR_RIGHT_SIDE, -900
        self.world_start_pos_ltop = 0, -900

        self._add_actors()
        self._sprites_all_add()

    def _add_actors(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [[6, 100, 460, platforms.PLAT_TYPE_01],
                       [5, 300, 258, platforms.PLAT_TYPE_01],
                       [4, 980, 562, platforms.PLAT_TYPE_01],
                       [3, 1100, 260, platforms.PLAT_TYPE_01],
                       [9, 1906, 110, platforms.PLAT_TYPE_01],
                       [3, 1300, 120, platforms.PLAT_TYPE_01],
                       [8, 2580, 440, platforms.PLAT_TYPE_01],
                       [4, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],  # earth
                       [44, 630, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],  # earth
                       ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(
                platform[0], platform[1], platform[2], platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add water blocks
        Water.create_water(0, SCREEN_NEAR_EARTH + 206, self.game, qty=19, qty_depth=3, add_to_list=self.decors)

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
        level_plats = [[5, 280, SCREEN_HEIGHT - platforms.PLAT_TYPE_03_SLIDING_R_MID[3], platforms.PLAT_TYPE_03_SLIDING, -2],
                       ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(
                platform[0], platform[1], platform[2], platform[3], velocity=platform[4])
        for platform in plats:
            block = platforms.SlidingBands(platform[0], platform[1], platform[2],
                                           self.game, velocity=platform[3], level=self)
            self.platforms.add(block)

        # Add computers
        self.computers.add([
            ComputerA(2960, 336, self.game),
            ])

        # Add files_disks
        self.files_disks.add([
            FilesDiskB(480, 222, self.game),
            FilesDiskC(530, 222, self.game),
            ])

        # Add doors
        self.doors.add([
            DoorRightYellow(3400, 550, self.game, level_dest=0, door_dest_pos=DOOR_DEST_NL, is_locked=True),
            DoorLeftGreen(2, 550, self.game, level_dest=0, door_dest_pos=DOOR_DEST_NL, is_locked=True),
            ])
