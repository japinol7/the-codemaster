"""Module level 21."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    DOOR_DEST_TR,
    )
from codemaster.models.actors.actors import DropItem, ActorType
from codemaster.models.actors.items import platforms, DoorRightAqua
from codemaster.models.actors.npcs import (
    SkullGreen,
    SkullYellow,
    SkullRed,
    SamuraiMale,
    )
from codemaster.models.actors.items import (
    BatteryA,
    CartridgeBlue,
    ComputerA,
    DoorLeftGreen,
    DoorRightAqua,
    DoorRightYellow,
    PotionHealth,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level21(Level):

    def __init__(self, game):
        super().__init__(game)
        self.id = 20
        self.name = str(self.id + 1)
        self.next_level_left = self.id - 1
        self.next_level_right = 1
        self.next_level_top = False
        self.next_level_bottom = False
        self.background = pg.image.load(self.file_name_im_get(10)).convert()
        self.level_limit = -3000
        self.level_limit_top = -1000
        self.player_start_pos_left = 220, 520
        self.player_start_pos_right = 520, 520
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
        level_plats = [[12, 420, 210, platforms.PLAT_TYPE_01],
                       [5, 3270, 240, platforms.PLAT_TYPE_01],
                       [1, 3200, 360, platforms.PLAT_TYPE_01],
                       [8, 1960, 130, platforms.PLAT_TYPE_01],
                       [2, 1500, 210, platforms.PLAT_TYPE_01],
                       [2, 1680, 300, platforms.PLAT_TYPE_01],
                       [2, 1420, 575, platforms.PLAT_TYPE_01],
                       [21, 1640, 460, platforms.PLAT_TYPE_01],
                       [56, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],  # earth
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
            BatteryA(760, 174, self.game),
            BatteryA(800, 174, self.game),
            BatteryA(840, 174, self.game),
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

        items_to_drop = [
            DropItem(CartridgeBlue, ActorType.CARTRIDGE_BLUE, probability_to_drop=100,
                     add_to_list=self.cartridges, x_delta=50),
            ]
        self.npcs.add(SamuraiMale(
            620, 127, self.game,
            border_left=550, border_right=1130, change_x=2, items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionHealth, ActorType.POTION_POWER, probability_to_drop=100,
                     add_to_list=self.potions, **{'random_min': 30, 'random_max': 40}),
            ]
        self.npcs.add(SamuraiMale(
            1000, 127, self.game,
            border_left=440, border_right=1100, change_x=2, items_to_drop=items_to_drop))

        # Add doors
        self.doors.add([
            DoorLeftGreen(2, 550, self.game, level_dest=19, door_dest_pos=DOOR_DEST_NL),
            DoorRightAqua(3480, 52, self.game, level_dest=16, door_dest_pos=DOOR_DEST_TR),
            DoorRightYellow(3640, 550, self.game, level_dest=21, door_dest_pos=DOOR_DEST_NL),
            ])
