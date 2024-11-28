"""Module level 9."""
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
    SnakeGreen,
    SnakeYellow,
    SquirrelA,
    )
from codemaster.models.actors.items import (
    BatteryA,
    CartridgeGreen,
    CartridgeBlue,
    DoorRightAqua,
    DoorRightYellow,
    DoorLeftWhite,
    LifeRecoveryA,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level9(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(9)).convert()
        self.player_start_pos_left = 220, 408
        self.player_start_pos_right = 600, 408
        self.player_start_pos_rtop = 800, -292
        self.player_start_pos_ltop = 80, 100
        
        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [
            [5, 3160, 170, platforms.PLAT_TYPE_01],
            [5, 2700, 240, platforms.PLAT_TYPE_01],
            [4, 2400, 420, platforms.PLAT_TYPE_01],
            [2, 2000, 150, platforms.PLAT_TYPE_01],
            [3, 2180, 300, platforms.PLAT_TYPE_01],
            [7, 1330, 80, platforms.PLAT_TYPE_01],
            [2, 920, 130, platforms.PLAT_TYPE_01],
            [5, 810, 270, platforms.PLAT_TYPE_01],
            [8, 700, 410, platforms.PLAT_TYPE_01],
            [12, 560, 550, platforms.PLAT_TYPE_01],
            [2, 2900, 590, platforms.PLAT_TYPE_01],
            [10, 3090, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
            [22, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
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
            BatteryA(2610, 385, self.game),
            ])

        # Add life_recs
        self.life_recs.add([
            LifeRecoveryA(2960, 194, self.game),
            ])

        # Add cartridges
        self.cartridges.add([
            CartridgeGreen(2840, 205, self.game),
            CartridgeBlue(2880, 205, self.game),
            CartridgeGreen(2840, 165, self.game),
            ])

        # Add NPCs
        self.npcs.add([
            SquirrelA(700, 358, self.game, border_left=690, border_right=1210, change_x=2),
            SquirrelA(740, 358, self.game, border_left=690, border_right=1210, change_x=3),
            SquirrelA(820, 358, self.game, border_left=700, border_right=1210, change_x=2),
            SquirrelA(860, 358, self.game, border_left=690, border_right=1210, change_x=1),
            SquirrelA(900, 358, self.game, border_left=700, border_right=1210, change_x=2),
            SquirrelA(660, 498, self.game, border_left=590, border_right=1300, change_x=2),
            SquirrelA(700, 498, self.game, border_left=590, border_right=1270, change_x=3),
            SquirrelA(820, 498, self.game, border_left=600, border_right=1300, change_x=2),
            SquirrelA(860, 498, self.game, border_left=590, border_right=1200, change_x=1),
            SquirrelA(900, 498, self.game, border_left=600, border_right=1260, change_x=2),
            SquirrelA(970, 498, self.game, border_left=590, border_right=1300, change_x=1),
            SquirrelA(1100, 498, self.game, border_left=600, border_right=1290, change_x=1),
            ])

        items_to_drop = [
            DropItem(PotionPower, probability_to_drop=70, x_delta=16,
                     **{'random_min': 65, 'random_max': 75}),
            ]
        self.snakes.add(SnakeGreen(660, 415, self.game, border_left=285, border_right=2840,
                                   border_top=80, border_down=810, change_x=1, change_y=1,
                                   items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionPower, x_delta=16, **{'random_min': 65, 'random_max': 75}),
            DropItem(LifeRecoveryA, x_delta=70),
            ]
        self.snakes.add(SnakeYellow(800, 500, self.game, border_left=320, border_right=2700,
                                    border_top=100, border_down=810, change_x=3, change_y=3,
                                    items_to_drop=items_to_drop))

        # Add doors
        self.doors.add([
            DoorLeftWhite(2, 550, self.game, level_dest=7, door_dest_pos=DOOR_DEST_NL),
            DoorRightAqua(3368, -18, self.game, level_dest=5, door_dest_pos=DOOR_DEST_TR),
            DoorRightYellow(3640, 550, self.game, level_dest=9, door_dest_pos=DOOR_DEST_NL),
            ])
