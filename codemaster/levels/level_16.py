"""Module level 16."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    )
from codemaster.models.actors.items import platforms
from codemaster.models.actors.decorations import Water
from codemaster.models.actors.actors import DropItem, ActorType
from codemaster.models.actors.npcs import (
    SnakeGreen,
    SnakeYellow,
    )
from codemaster.models.actors.items import (
    BatteryA,
    ComputerA,
    DoorLeftBlue,
    DoorRightRed,
    FilesDiskC,
    LifeRecoveryA,
    MineCyan,
    MineLilac,
    PotionHealth,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level16(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(5)).convert()
        self.player_start_pos_left = 220, 520
        self.player_start_pos_right = 520, 520
        self.player_start_pos_rtop = 250, -440
        self.player_start_pos_ltop = 80, 100
        
        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [[6, 640, 380, platforms.PLAT_TYPE_01],
                       [4, 1100, 210, platforms.PLAT_TYPE_01],
                       [7, 1600, 440, platforms.PLAT_TYPE_01],
                       [55, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
                       ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(platform[0], platform[1], platform[2], platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add water blocks
        Water.create_water(0, SCREEN_NEAR_EARTH + 216, self.game, qty=20, qty_depth=3, add_to_list=self.decors)

        # Add moving platforms (type, x, y, ...)
        self.platforms.add([
            platforms.MovingPlatform(
                platforms.PLAT_TYPE_02_STONE_MIDDLE, 550, 600, self.game,
                border_top=400, border_down=700, change_y=2, level=self),
            platforms.MovingPlatform(
                platforms.PLAT_TYPE_02_STONE_MIDDLE, 1510, 500, self.game,
                border_top=260, border_down=640, change_y=2, level=self),
            ])

        # Add batteries
        self.batteries.add([
            BatteryA(1640, 405, self.game),
            ])

        # Add files_disks
        self.files_disks.add([
            FilesDiskC(1680, 403, self.game),
            ])

        # Add computers
        self.computers.add([
            ComputerA(1900, 336, self.game),
            ])

        # Add NPCs
        items_to_drop = [
            DropItem(PotionHealth, ActorType.POTION_HEALTH, probability_to_drop=60, add_to_list=self.potions,
                     x_delta=16, **{'random_min': 20, 'random_max': 20}),
            ]
        self.snakes.add(SnakeGreen(900, 315, self.game, border_left=160, border_right=1160,
                                   border_top=0, border_down=510, change_x=1, change_y=1,
                                   items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionHealth, ActorType.POTION_HEALTH, probability_to_drop=60, add_to_list=self.potions,
                     x_delta=16, **{'random_min': 20, 'random_max': 20}),
            ]
        self.snakes.add(SnakeGreen(2800, 415, self.game, border_left=1000, border_right=3000,
                                   border_top=90, border_down=810, change_x=1, change_y=1,
                                   items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionPower, ActorType.POTION_POWER, probability_to_drop=80, add_to_list=self.potions,
                     x_delta=16, **{'random_min': 60, 'random_max': 75}),
            DropItem(LifeRecoveryA, ActorType.LIFE_RECOVERY, probability_to_drop=100, add_to_list=self.cartridges,
                     x_delta=70),
            ]
        self.snakes.add(SnakeYellow(1800, 500, self.game, border_left=1100, border_right=2900,
                                    border_top=100, border_down=806, change_x=3, change_y=3,
                                    items_to_drop=items_to_drop))

        # Add mines
        x = 626
        for i in range(17):
            self.mines.add(MineCyan(x, 170, self.game))
            x += 28

        x = 626
        for i in range(17):
            self.mines.add(MineLilac(x, 140, self.game))
            x += 28

        x = 1400
        for i in range(20):
            self.mines.add(MineCyan(x, 170, self.game))
            x += 28

        x = 1400
        for i in range(20):
            self.mines.add(MineLilac(x, 140, self.game))
            x += 28

        # Add doors
        self.doors.add([
            DoorLeftBlue(2, 550, self.game, level_dest=14, door_dest_pos=DOOR_DEST_NL),
            DoorRightRed(3640, 550, self.game, level_dest=16, door_dest_pos=DOOR_DEST_NL),
            ])
