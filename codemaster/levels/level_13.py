"""Module level 13."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    DOOR_DEST_TR,
    )
from codemaster.models.actors.actors import DropItem
from codemaster.models.actors.items import platforms
from codemaster.models.actors.decorations import Water
from codemaster.models.actors.npcs import (
    TethlorienYellow,
    TethlorienRed,
    VampireFemale,
    WolfManMale,
    )
from codemaster.models.actors.items import (
    BatteryA,
    CartridgeBlue,
    DoorLeftAqua,
    DoorRightMagenta,
    DoorRightGreen,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level13(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(4)).convert()
        self.player_start_pos_left = 220, 520
        self.player_start_pos_right = 520, 520
        self.player_start_pos_rtop = 958, -226
        self.player_start_pos_ltop = 80, 100
        
        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [[6, 2620, 170, platforms.PLAT_TYPE_01],
                       [5, 3270, 240, platforms.PLAT_TYPE_01],
                       [2, 3060, 384, platforms.PLAT_TYPE_01],
                       [2, 2000, 150, platforms.PLAT_TYPE_01],
                       [3, 2180, 300, platforms.PLAT_TYPE_01],
                       [7, 1330, 80, platforms.PLAT_TYPE_01],
                       [5, 810, 215, platforms.PLAT_TYPE_01],
                       [3, 700, 380, platforms.PLAT_TYPE_01],
                       [8, 560, 550, platforms.PLAT_TYPE_01],
                       [2, 1350, 380, platforms.PLAT_TYPE_01],
                       [2, 1750, 375, platforms.PLAT_TYPE_01],
                       [2, 2870, 550, platforms.PLAT_TYPE_01],
                       [10, 3090, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
                       [10, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
                       ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(platform[0], platform[1], platform[2], platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add water blocks
        Water.create_water(0, SCREEN_NEAR_EARTH + 216, self.game, qty=20, qty_depth=3)

        # Add batteries
        self.batteries.add([
            BatteryA(1800, 340, self.game),
            BatteryA(1850, 340, self.game),
            ])

        # Add NPCs
        item_to_drop = DropItem(CartridgeBlue)
        self.npcs.add([
            VampireFemale(1400, 8, self.game, border_left=1320, border_right=1780,
                          change_x=2, items_to_drop=[item_to_drop]),
            WolfManMale(1750, 8, self.game, border_left=1320, border_right=1780, change_x=2),
            ])

        item_to_drop = DropItem(PotionPower, **{'random_min': 25, 'random_max': 45})
        self.npcs.add(TethlorienYellow(
            2000, 500, self.game,
            border_left=1550, border_right=2040, change_x=2, items_to_drop=[item_to_drop]))

        item_to_drop = DropItem(PotionPower, **{'random_min': 50, 'random_max': 50})
        self.npcs.add(TethlorienRed(
            2140, 500, self.game,
            border_left=1700, border_right=2200, change_x=3, items_to_drop=[item_to_drop]))

        # Add doors
        self.doors.add([
            DoorLeftAqua(2, 550, self.game, level_dest=11, door_dest_pos=DOOR_DEST_NL),
            DoorRightMagenta(3480, 52, self.game, level_dest=16, door_dest_pos=DOOR_DEST_TR),
            DoorRightGreen(3640, 550, self.game, level_dest=13, door_dest_pos=DOOR_DEST_NL),
            ])
