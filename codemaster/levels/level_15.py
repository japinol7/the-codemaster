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
    SquirrelA,
    )
from codemaster.models.actors.items import (
    AppleGreen,
    AppleRed,
    AppleYellow,
    BatteryA,
    DoorLeftYellow,
    DoorRightBlue,
    FilesDiskA,
    )
from codemaster.levels.level_base import Level


class Level15(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(11)).convert()
        self.player_start_pos_left = 220, 520
        self.player_start_pos_right = 300, 520
        self.player_start_pos_rtop = 250, -440
        self.player_start_pos_ltop = 80, 100
        
        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [
            [3, 300, 460, platforms.PLAT_TYPE_01],
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
            [10, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
            [14, 2700, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
            ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(platform[0], platform[1], platform[2], platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add water blocks
        Water.create_water(0, SCREEN_NEAR_EARTH + 216, self.game, qty=19, qty_depth=3)

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
            SquirrelA(2700, -42, self.game, border_left=2610, border_right=2960, change_x=2),
            SquirrelA(2930, -42, self.game, border_left=2610, border_right=2960, change_x=2),
            ])

        # Add doors
        self.doors.add([
            DoorLeftYellow(2, 550, self.game, level_dest=13, door_dest_pos=DOOR_DEST_NL),
            DoorRightBlue(3500, 550, self.game, level_dest=15, door_dest_pos=DOOR_DEST_NL),
            ])
