"""Module level 21."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    )
from codemaster.models.actors.actors import DropItem, ActorType
from codemaster.models.actors.items import platforms
from codemaster.models.actors.npcs import (
    PumpkinZombieA,
    PumpkinHeadA,
    RobotA,
    RobotB,
    )
from codemaster.models.actors.items import (
    AppleGreen,
    AppleYellow,
    AppleRed,
    BatteryA,
    CartridgeBlue,
    CartridgeGreen,
    DoorLeftGreen,
    DoorRightYellow,
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
        self.background = pg.image.load(self.file_name_im_get(11)).convert()
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
        level_plats = [[9, 620, 210, platforms.PLAT_TYPE_01],
                       [1, 1500, 240, platforms.PLAT_TYPE_01],
                       [1, 1780, 310, platforms.PLAT_TYPE_01],
                       [1, 1800, 575, platforms.PLAT_TYPE_01],
                       [7, 1960, 460, platforms.PLAT_TYPE_01],
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
            BatteryA(840, 174, self.game),
            BatteryA(880, 174, self.game),
            ])

        # Add apples
        self.apples.add([
            AppleGreen(2300, 436, self.game),
            AppleGreen(2300, 410, self.game),
            AppleYellow(2330, 436, self.game),
            AppleYellow(2330, 410, self.game),
            AppleYellow(2360, 436, self.game),
            AppleRed(2390, 436, self.game),
            ])

        # Add NPCs
        items_to_drop = [
            DropItem(CartridgeBlue, ActorType.CARTRIDGE_BLUE, probability_to_drop=100,
                     add_to_list=self.cartridges, x_delta=16),
            ]

        self.npcs.add(RobotB(
            1140, 138, self.game, border_left=660, border_right=1200, change_x=2,
            items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionPower, ActorType.POTION_POWER, probability_to_drop=100, add_to_list=self.potions,
                     x_delta=16, **{'random_min': 60, 'random_max': 60}),
            ]
        self.npcs.add(RobotA(
            710, 138, self.game, border_left=680, border_right=1200, change_x=3,
            items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionPower, ActorType.POTION_POWER, probability_to_drop=100, add_to_list=self.potions,
                     x_delta=26, y_delta=-28, **{'random_min': 60, 'random_max': 60}),
            DropItem(PumpkinHeadA, ActorType.PUMPKIN_HEAD_A, probability_to_drop=100,
                     add_to_list=self.npcs, y_delta=24),
            ]
        self.npcs.add(PumpkinZombieA(
            2050, 358, self.game, border_left=1980, border_right=2390, change_x=2,
            items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(CartridgeGreen, ActorType.CARTRIDGE_GREEN, probability_to_drop=100,
                     add_to_list=self.cartridges, x_delta=26, y_delta=-28),
            DropItem(PumpkinHeadA, ActorType.PUMPKIN_HEAD_A, probability_to_drop=100,
                     add_to_list=self.npcs, y_delta=24),
            ]
        self.npcs.add(PumpkinZombieA(
            2300, 358, self.game, border_left=1970, border_right=2370, change_x=2,
            items_to_drop=items_to_drop))

        # Add doors
        self.doors.add([
            DoorLeftGreen(2, 550, self.game, level_dest=19, door_dest_pos=DOOR_DEST_NL),
            DoorRightYellow(3640, 550, self.game, level_dest=21, door_dest_pos=DOOR_DEST_NL),
            ])
