"""Module level test 9."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    DOOR_DEST_TR,
    )
from codemaster.models.actors.actors import DropItem
from codemaster.models.actors.items import platforms
from codemaster.models.actors.decorations import (
    Grass,
    Water,
    )
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.npcs import (
    RobotB,
    SquirrelA,
    )
from codemaster.models.actors.items import (
    DoorLeftYellow,
    DoorRightAqua,
    DoorRightBlue,
    PotionHealth,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class LevelTest9(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(10)).convert()
        self.player_start_pos_left = 220, 520
        self.player_start_pos_right = 520, 520
        self.player_start_pos_rtop = 800, -292
        self.player_start_pos_ltop = 80, 100
        
        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [[5, 3160, 170, platforms.PLAT_TYPE_01],
                       [5, 2700, 240, platforms.PLAT_TYPE_01],
                       [4, 2400, 420, platforms.PLAT_TYPE_01],
                       [2, 2000, 150, platforms.PLAT_TYPE_01],
                       [3, 2180, 300, platforms.PLAT_TYPE_01],
                       [7, 1330, 80, platforms.PLAT_TYPE_01],
                       [2, 920, 130, platforms.PLAT_TYPE_01],
                       [5, 810, 270, platforms.PLAT_TYPE_01],
                       [8, 700, 410, platforms.PLAT_TYPE_01],
                       [12, 560, 550, platforms.PLAT_TYPE_01],
                       [2, 2900, 616, platforms.PLAT_TYPE_01],
                       [22, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
                       [10, 3090, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
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
        Grass.create_grass_sm(
            0, SCREEN_NEAR_EARTH , self.game, qty=11, qty_depth=4,
            actor_type=ActorType.PLAT_GRASS_S_SM)
        Grass.create_grass_sm(
            3090, SCREEN_NEAR_EARTH , self.game, qty=5, qty_depth=4,
            actor_type=ActorType.PLAT_GRASS_S_SM)

        # Add NPCs
        robot_items_to_drop = [
            DropItem(PotionHealth, y_delta=20, **{'random_min': 100, 'random_max': 100}),
            DropItem(PotionPower, y_delta=20, x_delta=-50,
                     **{'random_min': 100, 'random_max': 100}),
            ]
        item_to_drop = DropItem(
            RobotB, y_delta=-20, items_to_drop=robot_items_to_drop,
            **{'border_left': 530, 'border_right': 600, 'change_x': 1})
        self.npcs.add([
            SquirrelA(560, 685, self.game, change_x=0,items_to_drop=[item_to_drop]),
            ])

        # Add doors
        self.doors.add([
            DoorLeftYellow(2, 550, self.game, level_dest=7, door_dest_pos=DOOR_DEST_NL, is_locked=True),
            DoorRightAqua(3368, -18, self.game, level_dest=0, door_dest_pos=DOOR_DEST_TR, is_locked=True),
            DoorRightBlue(3640, 550, self.game, level_dest=0, door_dest_pos=DOOR_DEST_NL, is_locked=True),
            ])
