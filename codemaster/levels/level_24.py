"""Module level 24."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    )
from codemaster.models.actors.actors import DropItem
from codemaster.models.actors.items import platforms
from codemaster.models.actors.decorations import Water
from codemaster.models.actors.npcs import (
    PokoyoA,
    PokoyoB,
    RobotA,
    )
from codemaster.models.actors.items import (
    BatteryA,
    CartridgeBlue,
    DoorLeftRed,
    DoorRightGreen,
    FilesDiskD,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level24(Level):

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
            [5, 700, 480, platforms.PLAT_TYPE_01],
            [2, 550, 370, platforms.PLAT_TYPE_01],
            [5, 170, 260, platforms.PLAT_TYPE_01],
            [1, 1260, 570, platforms.PLAT_TYPE_01],
            [14, 1460, 440, platforms.PLAT_TYPE_01],
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

        # Add batteries
        self.batteries.add([
            BatteryA(1840, 405, self.game),
            BatteryA(2000, 405, self.game),
            ])

        # Add files_disks
        self.files_disks.add([
            FilesDiskD(1920, 403, self.game),
            ])

        # Add cartridges
        self.cartridges.add([
            CartridgeBlue(240, 226, self.game),
            ])

        # Add NPCs
        pokoyos = [
            PokoyoB(1630, 160, self.game, border_top=130, border_down=370, change_y=2),
            PokoyoA(1700, 160, self.game, border_top=130, border_down=370, change_y=3),
            PokoyoB(1770, 200, self.game, border_top=130, border_down=370, change_y=3),
            PokoyoA(1920, 270, self.game, border_top=130, border_down=370, change_y=3),
            PokoyoB(1990, 170, self.game, border_top=130, border_down=370, change_y=3),
            PokoyoA(2060, 300, self.game, border_top=130, border_down=370, change_y=3),
            PokoyoA(2130, 160, self.game, border_top=130, border_down=370, change_y=3),
            PokoyoB(2200, 200, self.game, border_top=130, border_down=370, change_y=3),
            ]
        self.npcs.add(pokoyos)

        items_to_drop = [
            DropItem(PotionPower, x_delta=16, **{'random_min': 40, 'random_max': 40}),
            ]
        self.npcs.add([
            RobotA(240, 188, self.game, border_left=180, border_right=480, change_x=2,
                   items_to_drop=items_to_drop),
            ])

        # Add doors
        self.doors.add([
            DoorLeftRed(2, 550, self.game, level_dest=22, door_dest_pos=DOOR_DEST_NL),
            DoorRightGreen(3640, 550, self.game, level_dest=24, door_dest_pos=DOOR_DEST_NL),
            ])
