"""Module level 19."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    DOOR_DEST_TR,
    )
from codemaster.models.actors.items import platforms
from codemaster.models.actors.npcs import (
    SkullGreen,
    SkullYellow,
    SkullRed,
    )
from codemaster.models.actors.items import (
    BatteryA,
    ComputerA,
    DoorLeftBlue,
    DoorRightAqua,
    DoorRightMagenta,
    )
from codemaster.levels.level_base import Level


class Level19(Level):

    def __init__(self, id_, game):
        super().__init__(id_, game)
        self.background = pg.image.load(self.file_name_im_get(10)).convert()
        self.level_limit = -3000
        self.level_limit_top = -1000
        self.player_start_pos_left = 220, 520
        self.player_start_pos_right = 520, 520
        self.player_start_pos_rtop = 880, -292
        self.player_start_pos_ltop = 80, 100
        self.player_start_pos_bottom = 300, 800
        self.world_start_pos_left = 0, -758
        self.world_start_pos_right = self.level_limit + self.SCROLL_LV_NEAR_RIGHT_SIDE, -758
        self.world_start_pos_rtop = self.level_limit + 500 + self.SCROLL_LV_NEAR_RIGHT_SIDE, -900
        self.world_start_pos_ltop = 0, -900

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [[5, 3270, 240, platforms.PLAT_TYPE_01],
                       [1, 3200, 360, platforms.PLAT_TYPE_01],
                       [8, 1960, 130, platforms.PLAT_TYPE_01],
                       [2, 1780, 300, platforms.PLAT_TYPE_01],
                       [2, 1420, 575, platforms.PLAT_TYPE_01],
                       [21, 1640, 460, platforms.PLAT_TYPE_01],
                       [56, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
                       ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(platform[0], platform[1], platform[2],
                                                                       platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add batteries
        self.batteries.add([
            BatteryA(2160, 94, self.game),
            BatteryA(2200, 94, self.game),
            BatteryA(2240, 94, self.game),
            ])

        # Add computers
        self.computers.add([
            ComputerA(2800, 356, self.game),
            ])

        # Add NPCs
        self.npcs.add([
            SkullGreen(2000, 67, self.game, border_left=1950, border_right=2200, change_x=3),
            SkullGreen(2070, 67, self.game, border_left=1950, border_right=2200, change_x=3),
            SkullYellow(2360, 67, self.game, border_left=2080, border_right=2500, change_x=3),
            SkullRed(2410, 67, self.game, border_left=2170, border_right=2500, change_x=3),
            SkullRed(2460, 67, self.game, border_left=2170, border_right=2500, change_x=3),
            ])

        # Add doors
        self.doors.add([
            DoorLeftBlue(2, 550, self.game, level_dest=17, door_dest_pos=DOOR_DEST_NL),
            DoorRightAqua(3480, 52, self.game, level_dest=21, door_dest_pos=DOOR_DEST_TR),
            DoorRightMagenta(3640, 550, self.game, level_dest=19, door_dest_pos=DOOR_DEST_NL),
            ])
