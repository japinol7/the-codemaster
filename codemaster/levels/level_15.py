"""Module level 15."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    )
from codemaster.models.actors.items import platforms
from codemaster.models.actors.decorations import Water
from codemaster.models.actors.npcs import (
    BatBlack,
    )
from codemaster.models.actors.items import (
    AppleGreen,
    AppleRed,
    AppleYellow,
    BatteryA,
    DoorLeftYellow,
    DoorRightBlue,
    FilesDiskA,
    PotionHealth,
    )
from codemaster.levels.level_base import Level


class Level15(Level):

    def __init__(self, game):
        super().__init__(game)
        self.id = 14
        self.name = str(self.id + 1)
        self.next_level_left = self.id - 1
        self.next_level_right = self.id + 1
        self.next_level_top = False
        self.next_level_bottom = False
        self.background = pg.image.load(self.file_name_im_get(11)).convert()
        self.level_limit = -3000
        self.level_limit_top = -1000
        self.player_start_pos_left = 220, 520
        self.player_start_pos_right = 300, 520
        self.player_start_pos_rtop = 250, -440
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
        level_plats = [[3, 300, 460, platforms.PLAT_TYPE_01],
                       [6, 300, 220, platforms.PLAT_TYPE_01],
                       [2, 680, 580, platforms.PLAT_TYPE_01],
                       [6, 1300, 120, platforms.PLAT_TYPE_01],
                       [2, 2360, 130, platforms.PLAT_TYPE_01],
                       [2, 8, 90, platforms.PLAT_TYPE_01],
                       [2, 30, 300, platforms.PLAT_TYPE_01],
                       [4, 900, 110, platforms.PLAT_TYPE_01],
                       [6, 2600, 10, platforms.PLAT_TYPE_01],
                       [9, 1350, 460, platforms.PLAT_TYPE_01],
                       [4, 2560, 400, platforms.PLAT_TYPE_01],
                       [2, 2860, 560, platforms.PLAT_TYPE_01],
                       [10, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],  # earth
                       [14, 2700, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],  # earth
                       ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(platform[0], platform[1], platform[2], platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add water blocks
        Water.create_water(0, SCREEN_NEAR_EARTH + 216, self.game, qty=19, qty_depth=3, add_to_list=self.decors)

        # Add moving platforms (type, x, y, ...)
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 1800, 310, self.game,
            border_left=1600, border_right=2600, change_x=6, level=self))

        # Add batteries
        self.batteries.add([
            BatteryA(60, 54, self.game),
            ])

        # Add files_disks
        self.files_disks.add([
            FilesDiskA(2920, -27, self.game),
            ])

        # Add apples
        self.apples.add([
            AppleGreen(950, 85, self.game),
            AppleGreen(950, 59, self.game),
            AppleYellow(980, 85, self.game),
            AppleYellow(980, 59, self.game),
            AppleYellow(1010, 85, self.game),
            AppleRed(1040, 85, self.game),
            AppleRed(1070, 85, self.game),
            ])

        # Add NPCs
        self.npcs.add([
            BatBlack(1000, 40, self.game, border_left=700, border_right=1650, change_x=3),
            BatBlack(1190, 40, self.game, border_left=700, border_right=1650, change_x=3),
            BatBlack(1380, 40, self.game, border_left=700, border_right=1650, change_x=3),
            ])

        # Add doors
        self.doors.add([
            DoorLeftYellow(2, 550, self.game, level_dest=13, door_dest_pos=DOOR_DEST_NL),
            DoorRightBlue(3500, 550, self.game, level_dest=15, door_dest_pos=DOOR_DEST_NL),
            ])
