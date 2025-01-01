"""Module level test 6."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    )
from codemaster.models.actors.items import platforms
from codemaster.models.actors.actors import DropItem
from codemaster.models.actors.decorations import (
    Grass,
    Water,
    )
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.npcs import (
    BatBlue,
    RobotA,
    RobotB,
    )
from codemaster.models.actors.items import (
    CartridgeGreen,
    CartridgeBlue,
    BatteryA,
    DoorLeftYellow,
    DoorRightRed,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class LevelTest6(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(8)).convert()
        self.player_start_pos_left = 220, 520
        self.player_start_pos_right = 520, 520
        self.player_start_pos_rtop = 800, -292
        self.player_start_pos_ltop = 80, 100
        
        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [[11, 2000, -16, platforms.PLAT_TYPE_01],
                       [12, 2600, 160, platforms.PLAT_TYPE_01],
                       [6, 20, 160, platforms.PLAT_TYPE_01],
                       [7, 740, 84, platforms.PLAT_TYPE_01],
                       [7, 1400, 84, platforms.PLAT_TYPE_01],
                       [5, 600, 280, platforms.PLAT_TYPE_01],
                       [13, 1200, 280, platforms.PLAT_TYPE_01],
                       [7, 740, 476, platforms.PLAT_TYPE_01],
                       [8, 1660, 476, platforms.PLAT_TYPE_01],
                       [7, 2400, 476, platforms.PLAT_TYPE_01],
                       [2, 1380, 585, platforms.PLAT_TYPE_01],
                       [56, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
                       ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(platform[0], platform[1], platform[2], platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add water blocks
        Water.create_water(0, SCREEN_NEAR_EARTH + 216, self.game, qty=20, qty_depth=3)

        # Add grass blocks
        Grass.create_grass(0, SCREEN_NEAR_EARTH , self.game, qty=19, qty_depth=2,
            actor_type=ActorType.PLAT_GRASS_D)

        # Add batteries
        self.batteries.add([
            BatteryA(1250, 244, self.game),
            BatteryA(1300, 244, self.game),
            ])

        # Add NPCs
        self.npcs.add([
            BatBlue(634, -26, self.game, border_left=610, border_right=1300, change_x=3),
            BatBlue(780, 16, self.game, border_left=610, border_right=1300, change_x=3),
            ])

        items_to_drop = [
            DropItem(CartridgeGreen, x_delta=16),
            ]

        self.npcs.add(RobotB(
            3020, 86, self.game, border_left=2620, border_right=3380, change_x=2,
            items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionPower, x_delta=16, **{'random_min': 70, 'random_max': 80}),
            DropItem(CartridgeBlue, x_delta=60),
            ]
        self.npcs.add(RobotA(
            2940, 86, self.game, border_left=2590, border_right=3400, change_x=3,
            items_to_drop=items_to_drop))

        # Add doors
        self.doors.add([
            DoorLeftYellow(0, 550, self.game, level_dest=4, door_dest_pos=DOOR_DEST_NL, is_locked=True),
            DoorRightRed(3640, 550, self.game, level_dest=6, door_dest_pos=DOOR_DEST_NL, is_locked=True),
            ])
