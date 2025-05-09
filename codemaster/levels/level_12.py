"""Module level 12."""
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
    PokoyoA,
    PokoyoB,
    SnakeBlue,
    SnakeYellow,
    )
from codemaster.models.actors.items import (
    BatteryA,
    ComputerA,
    DoorLeftMagenta,
    DoorRightAqua,
    FilesDiskA,
    FilesDiskC,
    LifeRecoveryA,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level12(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(3)).convert()
        self.player_start_pos_left = 220, 408
        self.player_start_pos_right = 600, 408
        self.player_start_pos_rtop = 250, -440
        self.player_start_pos_ltop = 80, 100

        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [
            [7, 620, 380, platforms.PLAT_TYPE_01],
            [7, 1460, 440, platforms.PLAT_TYPE_01],
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
            actor_type=ActorType.PLAT_GRASS_Q)

        # Add moving platforms (type, x, y, ...)
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 1220, 600, self.game,
            border_top=470, border_down=700, change_y=2, level=self))

        # Add batteries
        self.batteries.add([
            BatteryA(1640, 405, self.game),
            ])

        # Add files_disks
        self.files_disks.add([
            FilesDiskC(1680, 403, self.game),
            FilesDiskA(1720, 403, self.game),
            ])

        # Add computers
        self.computers.add([
            ComputerA(1780, 336, self.game),
            ])

        # Add NPCs
        pokoyos = [
            PokoyoA(700, 460, self.game, border_top=440, border_down=665, change_y=3),
            PokoyoB(770, 600, self.game, border_top=440, border_down=665, change_y=3),
            PokoyoA(920, 570, self.game, border_top=440, border_down=665, change_y=3),
            PokoyoB(990, 470, self.game, border_top=440, border_down=665, change_y=3),
            ]
        self.npcs.add(pokoyos)
        items_to_drop = [
            DropItem(PotionPower, probability_to_drop=60, x_delta=16,
                     **{'random_min': 40, 'random_max': 60}),
            ]
        self.snakes.add(SnakeBlue(1500, 415, self.game, border_left=1210, border_right=2940,
                                  border_top=90, border_down=810, change_x=1, change_y=1,
                                  items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionPower, probability_to_drop=80, x_delta=16,
                     **{'random_min': 60, 'random_max': 75}),
            DropItem(LifeRecoveryA, x_delta=70),
            ]
        self.snakes.add(SnakeYellow(2100, 500, self.game, border_left=1200, border_right=2900,
                                    border_top=100, border_down=806, change_x=3, change_y=3,
                                    items_to_drop=items_to_drop))

        # Add doors
        self.doors.add([
            DoorLeftMagenta(0, 550, self.game, level_dest=10, door_dest_pos=DOOR_DEST_NL),
            DoorRightAqua(3640, 550, self.game, level_dest=12, door_dest_pos=DOOR_DEST_NL, is_locked=False),
            ])
