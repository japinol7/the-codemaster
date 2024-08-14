"""Module level 26."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    )
from codemaster.models.actors.actors import DropItem, ActorType
from codemaster.models.actors.items import platforms
from codemaster.models.actors.decorations import Water
from codemaster.models.actors.npcs import (
    SquirrelA,
    PumpkinHeadA,
    PumpkinZombieA,
    )
from codemaster.models.actors.items import (
    BatteryA,
    CartridgeGreen,
    DoorLeftYellow,
    DoorRightRed,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level26(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(6)).convert()
        self.player_start_pos_left = 220, 520
        self.player_start_pos_right = 520, 520
        self.player_start_pos_rtop = 250, -440
        self.player_start_pos_ltop = 80, 100
        
        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [[12, 1550, 440, platforms.PLAT_TYPE_01],
                       [1, 1360, 570, platforms.PLAT_TYPE_01],
                       [9, 1690, 98, platforms.PLAT_TYPE_01],
                       [1, 2580, 98, platforms.PLAT_TYPE_01],
                       [1, 2580, 350, platforms.PLAT_TYPE_01],
                       [1, 2780, 240, platforms.PLAT_TYPE_01],
                       [3, 3080, 200, platforms.PLAT_TYPE_01],
                       [1, 2490, 570, platforms.PLAT_TYPE_01],
                       [56, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
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
            BatteryA(3180, 167, self.game),
            BatteryA(3230, 167, self.game),
            ])

        # Add NPCs
        self.npcs.add([
            SquirrelA(1560, 388, self.game, border_left=1560, border_right=2350, change_x=2),
            SquirrelA(1610, 388, self.game, border_left=1560, border_right=2350, change_x=3),
            SquirrelA(1680, 388, self.game, border_left=1570, border_right=2340, change_x=2),
            SquirrelA(1740, 388, self.game, border_left=1560, border_right=2350, change_x=1),
            SquirrelA(1800, 388, self.game, border_left=1570, border_right=2340, change_x=2),
            SquirrelA(1870, 388, self.game, border_left=1570, border_right=2340, change_x=3),
            SquirrelA(1900, 388, self.game, border_left=1560, border_right=2350, change_x=1),
            SquirrelA(1950, 388, self.game, border_left=1570, border_right=2340, change_x=1),
            SquirrelA(1990, 388, self.game, border_left=1590, border_right=2340, change_x=3),
            SquirrelA(2010, 388, self.game, border_left=1570, border_right=2340, change_x=1),
            SquirrelA(2080, 388, self.game, border_left=1570, border_right=2340, change_x=3),
            SquirrelA(2130, 388, self.game, border_left=1570, border_right=2340, change_x=2),
            SquirrelA(2200, 388, self.game, border_left=1570, border_right=2340, change_x=1),
            SquirrelA(2280, 388, self.game, border_left=1570, border_right=2340, change_x=2),
            SquirrelA(2300, 388, self.game, border_left=1570, border_right=2340, change_x=1),
            SquirrelA(2320, 388, self.game, border_left=1570, border_right=2340, change_x=3),
            ])

        items_to_drop = [
            DropItem(PotionPower, ActorType.POTION_POWER, probability_to_drop=100, add_to_list=self.potions,
                     x_delta=26, y_delta=-35, **{'random_min': 40, 'random_max': 40}),
            DropItem(PumpkinHeadA, ActorType.PUMPKIN_HEAD_A, probability_to_drop=100,
                     add_to_list=self.npcs, y_delta=15),
            ]
        self.npcs.add(PumpkinZombieA(
            1770, 9, self.game, border_left=1730, border_right=2280, change_x=2,
            items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(CartridgeGreen, ActorType.CARTRIDGE_GREEN, probability_to_drop=100,
                     add_to_list=self.cartridges, x_delta=26, y_delta=-35),
            DropItem(PumpkinHeadA, ActorType.PUMPKIN_HEAD_A, probability_to_drop=100,
                     add_to_list=self.npcs, y_delta=15),
            ]
        self.npcs.add(PumpkinZombieA(
            2180, 9, self.game, border_left=1710, border_right=2280, change_x=2,
            items_to_drop=items_to_drop))

        # Add doors
        self.doors.add([
            DoorLeftYellow(2, 550, self.game, level_dest=24, door_dest_pos=DOOR_DEST_NL),
            DoorRightRed(3640, 550, self.game, level_dest=26, door_dest_pos=DOOR_DEST_NL),
            ])
