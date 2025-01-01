"""Module level 20."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    )
from codemaster.models.actors.items import platforms
from codemaster.models.actors.decorations import (
    Grass,
    Water,
    )
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.npcs import (
    PokoyoA,
    PokoyoB,
    )
from codemaster.models.actors.items import (
    BatteryA,
    DoorLeftMagenta,
    DoorRightGreen,
    FilesDiskB,
    FilesDiskD,
    )
from codemaster.levels.level_base import Level


class Level20(Level):

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
            [8, 620, 440, platforms.PLAT_TYPE_01],
            [1, 1260, 570, platforms.PLAT_TYPE_01],
            [14, 1460, 440, platforms.PLAT_TYPE_01],
            [1, 2580, 350, platforms.PLAT_TYPE_01],
            [3, 2700, 250, platforms.PLAT_TYPE_01],
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
            actor_type=ActorType.PLAT_GRASS_U)

        # Add batteries
        self.batteries.add([
            BatteryA(880, 405, self.game),
            BatteryA(2840, 215, self.game),
            ])

        # Add files_disks
        self.files_disks.add([
            FilesDiskD(800, 403, self.game),
            FilesDiskB(960, 403, self.game),
            ])

        # Add NPCs
        pokoyos = [
            PokoyoA(700, 160, self.game, border_top=130, border_down=370, change_y=3),
            PokoyoB(770, 200, self.game, border_top=130, border_down=370, change_y=3),
            PokoyoA(920, 270, self.game, border_top=130, border_down=370, change_y=3),
            PokoyoB(990, 170, self.game, border_top=130, border_down=370, change_y=3),
            PokoyoA(1060, 300, self.game, border_top=130, border_down=370, change_y=3),
            ]
        self.npcs.add(pokoyos)

        # Add doors
        self.doors.add([
            DoorLeftMagenta(0, 550, self.game, level_dest=18, door_dest_pos=DOOR_DEST_NL),
            DoorRightGreen(3640, 550, self.game, level_dest=20, door_dest_pos=DOOR_DEST_NL),
            ])
