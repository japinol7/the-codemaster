"""Module level 3."""
__author__ = 'Joan A. Pinol  (japinol)'

from random import randint

import pygame as pg

from codemaster.config.constants import (
    SCREEN_HEIGHT,
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    )
from codemaster.models.actors.actors import DropItem, ActorType
from codemaster.models.actors.items import platforms
from codemaster.models.actors.decorations import Water
from codemaster.models.actors.npcs import (
    BatBlack,
    BatLilac,
    DemonMale,
    SkullBlue,
    SkullYellow,
    TerminatorEyeGreen,
    TerminatorEyeYellow,
    VampireMale,
    )
from codemaster.models.actors.items import (
    AppleGreen,
    AppleYellow,
    AppleRed,
    BatteryA,
    CartridgeGreen,
    CartridgeBlue,
    CartridgeYellow,
    CartridgeRed,
    ComputerA,
    DoorLeftGreen,
    DoorRightYellow,
    FilesDiskD,
    PotionPower,
    PotionHealth,
    )
from codemaster.levels.level_base import Level


class Level3(Level):

    def __init__(self, id_, game):
        super().__init__(id_, game)
        self.background = pg.image.load(self.file_name_im_get(3)).convert()
        self.level_limit = -2700
        self.level_limit_top = -1000
        self.player_start_pos_left = 220, 480
        self.player_start_pos_right = 600, 470
        self.player_start_pos_rtop = 300, 100
        self.player_start_pos_ltop = 80, 100
        self.player_start_pos_bottom = 300, 800
        self.world_start_pos_left = 0, -758
        self.world_start_pos_right = self.level_limit + self.SCROLL_LV_NEAR_RIGHT_SIDE, -758
        self.world_start_pos_rtop = self.level_limit + 500 + self.SCROLL_LV_NEAR_RIGHT_SIDE, -900
        self.world_start_pos_ltop = 0, -900

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [[5, 100, 460, platforms.PLAT_TYPE_01],
                       [5, 300, 220, platforms.PLAT_TYPE_01],
                       [4, 980, 570, platforms.PLAT_TYPE_01],
                       [3, 800, 440, platforms.PLAT_TYPE_01],
                       [3, 1100, 260, platforms.PLAT_TYPE_01],
                       [9, 1900, 110, platforms.PLAT_TYPE_01],
                       [8, 2580, 440, platforms.PLAT_TYPE_01],
                       [4, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
                       [14, 630, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
                       [30, 1700, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
                       ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(
                platform[0], platform[1], platform[2], platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add water blocks
        Water.create_water(0, SCREEN_NEAR_EARTH + 206, self.game, qty=19, qty_depth=3, add_to_list=self.decors)

        # Add moving platforms (type, x, y, ...)
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 1350, 510, self.game,
            border_left=1250, border_right=1650, change_x=2, level=self))
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 1600, 360, self.game,
            border_left=1350, border_right=2650, change_x=7, level=self))
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 950, 260, self.game,
            border_top=200, border_down=450, change_y=3, level=self))

        # Add sliding bands (n_blocs, x, y, type, velocity)
        level_plats = [[5, 280, SCREEN_HEIGHT - platforms.PLAT_TYPE_03_SLIDING_R_MID[3], platforms.PLAT_TYPE_03_SLIDING, -2],
                       [3, 1300, 120, platforms.PLAT_TYPE_03_SLIDING, 3]
                       ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(
                platform[0], platform[1], platform[2], platform[3], velocity=platform[4])
        for platform in plats:
            block = platforms.SlidingBands(platform[0], platform[1], platform[2],
                                           self.game, velocity=platform[3], level=self)
            self.platforms.add(block)

        # Add batteries
        self.batteries.add([
            BatteryA(410, 184, self.game),
            BatteryA(1400, 84, self.game),
            BatteryA(2200, 74, self.game),
            BatteryA(2300, 74, self.game),
            BatteryA(2380, 74, self.game),
            BatteryA(2390, 74, self.game),
            BatteryA(2400, 74, self.game),
            BatteryA(2410, 74, self.game),
            ])

        # Add files_disks
        self.files_disks.add([
            FilesDiskD(1300, 84, self.game),
            ])

        # Add cartridges
        self.cartridges.add([
            CartridgeGreen(2600, 405, self.game),
            CartridgeBlue(2700, 405, self.game),
            CartridgeYellow(2800, 405, self.game),
            CartridgeRed(2900, 405, self.game),
            ])

        # Add computers
        self.computers.add([
            ComputerA(2960, 336, self.game),
            ])

        # Add apples
        self.apples.add([
            AppleGreen(180, 435, self.game),
            AppleYellow(220, 435, self.game),
            AppleYellow(270, 435, self.game),
            AppleRed(320, 435, self.game),
            ])

        # Add NPCs
        self.npcs.add([
            SkullYellow(2360, 47, self.game, border_left=2180, border_right=2500, change_x=3),
            VampireMale(1880, 14, self.game, border_left=1865, border_right=2245, change_x=2),
            ])

        self.npcs.add([
            BatBlack(1900, 550, self.game, border_left=1780, border_right=2600, change_x=4),
            BatBlack(2120, 620, self.game, border_left=1780, border_right=2600, change_x=5),
            BatLilac(2250, 570, self.game, border_left=1780, border_right=2600, change_x=4),
            ])

        items_to_drop = [
            DropItem(PotionPower, ActorType.POTION_POWER, probability_to_drop=100, add_to_list=self.potions,
                     x_delta=16, **{'random_min': 58, 'random_max': 72}),
            DropItem(CartridgeGreen, ActorType.CARTRIDGE_GREEN, probability_to_drop=75, add_to_list=self.cartridges,
                     x_delta=170),
            DropItem(CartridgeBlue, ActorType.CARTRIDGE_BLUE, probability_to_drop=100, add_to_list=self.cartridges,
                     x_delta=195),
            ]
        self.npcs.add([
            TerminatorEyeYellow(1700, 650, self.game, border_left=1680, border_right=2370,
                                change_x=3, items_to_drop=items_to_drop),
            ])

        items_to_drop = [
            DropItem(PotionHealth, ActorType.POTION_POWER, probability_to_drop=100, add_to_list=self.potions,
                     x_delta=16, **{'random_min': 58, 'random_max': 72}),
            DropItem(CartridgeYellow, ActorType.CARTRIDGE_GREEN, probability_to_drop=75, add_to_list=self.cartridges,
                     x_delta=170),
            ]
        self.npcs.add([
            DemonMale(2280, 662, self.game, border_left=1680, border_right=2370,
                      change_x = 3, items_to_drop = items_to_drop),
            ])

        for _ in range(2):
            self.npcs.add(SkullYellow(
                320 + randint(7, 200), 155, self.game,
                border_left=300, border_right=650, change_x=randint(3, 6)))

        self.npcs.add(SkullBlue(
            320 + randint(15, 200), 155, self.game,
            border_left=310, border_right=600, change_x=randint(3, 7)))

        self.npcs.add([
            TerminatorEyeGreen(3000, 355, self.game, border_left=2660, border_right=3200, change_x=2),
            ])

        # Add doors
        self.doors.add([
            DoorRightYellow(3400, 550, self.game, level_dest=3, door_dest_pos=DOOR_DEST_NL),
            DoorLeftGreen(2, 550, self.game, level_dest=1, door_dest_pos=DOOR_DEST_NL),
            ])
