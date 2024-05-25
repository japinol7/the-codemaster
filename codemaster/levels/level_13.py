"""Module level 13."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    DOOR_DEST_TR,
    )
from codemaster.models.actors.actors import DropItem, ActorType
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

    def __init__(self, game):
        super().__init__(game)
        self.id = 12
        self.name = str(self.id + 1)
        self.next_level_left = self.id - 1
        self.next_level_right = self.id + 1
        self.next_level_top = False
        self.next_level_bottom = False
        self.background = pg.image.load(self.file_name_im_get(4)).convert()
        self.level_limit = -3000
        self.level_limit_top = -1000
        self.player_start_pos_left = 220, 520
        self.player_start_pos_right = 520, 520
        self.player_start_pos_rtop = 958, -226
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
                       [10, 3090, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],  # earth
                       [10, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],  # earth
                       ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(platform[0], platform[1], platform[2], platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add water blocks
        Water.create_water(0, SCREEN_NEAR_EARTH + 216, self.game, qty=20, qty_depth=3, add_to_list=self.decors)

        # Add batteries
        self.batteries.add([
            BatteryA(1800, 340, self.game),
            BatteryA(1850, 340, self.game),
            ])

        # Add NPCs
        items_to_drop = [
            DropItem(CartridgeBlue, ActorType.CARTRIDGE_BLUE, probability_to_drop=100, add_to_list=self.cartridges),
            ]
        self.npcs.add([
            VampireFemale(1400, 8, self.game,
                          border_left=1320, border_right=1780, change_x=2, items_to_drop=items_to_drop),
            WolfManMale(1750, 8, self.game, border_left=1320, border_right=1780, change_x=2)
            ])

        items_to_drop = [
            DropItem(PotionPower, ActorType.POTION_POWER, probability_to_drop=100, add_to_list=self.potions,
                     **{'random_min': 25, 'random_max': 45}),
            ]
        self.npcs.add(TethlorienYellow(
            2000, 500, self.game,
            border_left=1550, border_right=2040, change_x=2, items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionPower, ActorType.POTION_POWER, probability_to_drop=100, add_to_list=self.potions,
                     **{'random_min': 50, 'random_max': 50}),
            ]
        self.npcs.add(TethlorienRed(
            2140, 500, self.game,
            border_left=1700, border_right=2200, change_x=3, items_to_drop=items_to_drop))

        # Add doors
        self.doors.add([
            DoorLeftAqua(2, 550, self.game, level_dest=11, door_dest_pos=DOOR_DEST_NL),
            DoorRightMagenta(3480, 52, self.game, level_dest=16, door_dest_pos=DOOR_DEST_TR),
            DoorRightGreen(3640, 550, self.game, level_dest=13, door_dest_pos=DOOR_DEST_NL),
            ])
