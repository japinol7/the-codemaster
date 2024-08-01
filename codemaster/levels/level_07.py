"""Module level 7."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    )
from codemaster.models.actors.items import platforms
from codemaster.models.actors.decorations import Water
from codemaster.models.actors.npcs import (
    PokoyoA,
    PokoyoB,
    )
from codemaster.models.actors.items import (
    AppleGreen,
    AppleRed,
    AppleYellow,
    BatteryA,
    CartridgeGreen,
    CartridgeBlue,
    CartridgeYellow,
    DoorRightYellow,
    DoorLeftGreen,
    FilesDiskB,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level7(Level):

    def __init__(self, id_, game):
        super().__init__(id_, game)
        self.background = pg.image.load(self.file_name_im_get(7)).convert()
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

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [[12, 620, 210, platforms.PLAT_TYPE_01],
                       [2, 1600, 335, platforms.PLAT_TYPE_01],
                       [2, 1780, 460, platforms.PLAT_TYPE_01],
                       [2, 1960, 585, platforms.PLAT_TYPE_01],
                       [12, 1890, 192, platforms.PLAT_TYPE_01],
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
            BatteryA(660, 174, self.game),
            BatteryA(2600, 156, self.game),
            BatteryA(2646, 156, self.game),
            ])

        # Add files_disks
        self.files_disks.add([
            FilesDiskB(700, 173, self.game),
            ])

        # Add apples
        self.apples.add([
            AppleGreen(800, 186, self.game),
            AppleGreen(800, 160, self.game),
            AppleYellow(830, 186, self.game),
            AppleRed(860, 186, self.game),
            ])

        # Add potions
        self.potions.add([
            PotionPower(1130, 172, self.game),
            PotionPower(1130, 132, self.game),
            ])

        # Add cartridges
        self.cartridges.add([
            CartridgeYellow(1180, 175, self.game),
            CartridgeBlue(1220, 175, self.game),
            CartridgeGreen(1180, 136, self.game),
            CartridgeGreen(1180, 98, self.game),
            ])

        # Add NPCs
        pokoyos = [
            PokoyoA(700, 340, self.game, border_top=270, border_down=665, change_y=3),
            PokoyoB(770, 600, self.game, border_top=270, border_down=665, change_y=3),
            PokoyoA(840, 340, self.game, border_top=270, border_down=665, change_y=4),
            PokoyoB(910, 600, self.game, border_top=270, border_down=665, change_y=4),
            PokoyoA(980, 300, self.game, border_top=270, border_down=665, change_y=3),
            PokoyoB(1050, 500, self.game, border_top=270, border_down=665, change_y=3),
            PokoyoA(1120, 310, self.game, border_top=270, border_down=665, change_y=2),
            PokoyoB(1190, 610, self.game, border_top=270, border_down=665, change_y=2),
            PokoyoA(1260, 440, self.game, border_top=270, border_down=665, change_y=2),
            PokoyoB(1330, 400, self.game, border_top=270, border_down=665, change_y=2),
            ]
        self.npcs.add(pokoyos)

        # Add doors
        self.doors.add([
            DoorLeftGreen(2, 550, self.game, level_dest=5, door_dest_pos=DOOR_DEST_NL),
            DoorRightYellow(3640, 550, self.game, level_dest=7, door_dest_pos=DOOR_DEST_NL),
            ])
