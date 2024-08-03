"""Module level test 3."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    DOOR_DEST_TR,
    )
from codemaster.models.actors.items import platforms
from codemaster.models.actors.decorations import Water
from codemaster.models.actors.npcs import (
    SnakeGreen,
    SnakeYellow,
    )
from codemaster.models.actors.items import (
    BatteryA,
    DoorLeftGreen,
    DoorRightAqua,
    DoorRightYellow,
    LifeRecoveryA,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class LevelTest3(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(9)).convert()
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
        Water.create_water(0, SCREEN_NEAR_EARTH + 216, self.game, qty=20, qty_depth=3, add_to_list=self.decors)

        # Add batteries
        self.batteries.add([
            BatteryA(2610, 380, self.game),
            ])

        # Add life_recs
        self.life_recs.add([
            LifeRecoveryA(2940, 194, self.game),
            ])

        # Add cartridges
        self.potions.add([
            PotionPower(2800, 204, self.game),
            PotionPower(2840, 204, self.game),
            PotionPower(2880, 204, self.game),
            PotionPower(2800, 164, self.game),
            PotionPower(2840, 164, self.game),
            PotionPower(2880, 164, self.game),
            ])

        # Add NPCs
        self.snakes.add(SnakeGreen(1700, 415, self.game, border_left=1100, border_right=3400,
                                   border_top=80, border_down=810, change_x=1, change_y=1))

        self.snakes.add(SnakeYellow(2400, 500, self.game, border_left=2000, border_right=3380,
                                    border_top=100, border_down=810, change_x=3, change_y=3))

        # Add doors
        self.doors.add([
            DoorLeftGreen(2, 550, self.game, level_dest=0, door_dest_pos=DOOR_DEST_NL, is_locked=True),
            DoorRightAqua(3368, -18, self.game, level_dest=0, door_dest_pos=DOOR_DEST_TR, is_locked=True),
            DoorRightYellow(3640, 550, self.game, level_dest=0, door_dest_pos=DOOR_DEST_NL, is_locked=True),
            ])
