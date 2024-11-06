"""Module level 6."""
__author__ = 'Joan A. Pinol  (japinol)'

from random import randint

import pygame as pg

from codemaster.models.actors.actors import DropItem
from codemaster.config.constants import (
    SCREEN_HEIGHT,
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    DOOR_DEST_TR,
    )
from codemaster.models.actors.items import platforms
from codemaster.models.actors.npcs import (
    BatBlack,
    SkullYellow,
    SkullRed,
    SnakeGreen,
    SnakeBlue,
    SnakeYellow,
    SnakeRed,
    VampireMale,
    )
from codemaster.models.actors.items import (
    BatteryA,
    CartridgeGreen,
    CartridgeBlue,
    CartridgeYellow,
    CartridgeRed,
    ComputerA,
    DoorLeftAqua,
    DoorRightGreen,
    DoorLeftRed,
    DoorKeyAqua,
    FilesDiskC,
    LifeRecoveryA,
    MineLilac,
    PotionHealth,
    PotionPower,
    )
from codemaster.models.actors.text_msgs import TextMsg
from codemaster.levels.level_base import Level


class Level6(Level):

    def __init__(self, id_, game):
        self.level_limit = -2700
        self.background = pg.image.load(self.file_name_im_get(6)).convert()
        self.player_start_pos_left = 220, 480
        self.player_start_pos_right = 600, 480
        self.player_start_pos_rtop = 900, -390
        self.player_start_pos_ltop = 80, 100
        
        super().__init__(id_, game)

    def update_pc_enter_level(self):
        super().update_pc_enter_level()
        TextMsg.create("Aargh!\nThese snakes\nare crazy!", self.game, time_in_secs=4)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [
            [5, 100, 460, platforms.PLAT_TYPE_01],
            [5, 300, 220, platforms.PLAT_TYPE_01],
            [4, 980, 570, platforms.PLAT_TYPE_01],
            [3, 800, 440, platforms.PLAT_TYPE_01],
            [3, 1100, 260, platforms.PLAT_TYPE_01],
            [9, 1900, 110, platforms.PLAT_TYPE_01],
            [8, 2580, 440, platforms.PLAT_TYPE_01],
            [4, 2780, 98, platforms.PLAT_TYPE_01],
            [2, 3340, 98, platforms.PLAT_TYPE_01],
            [2, 3200, 196, platforms.PLAT_TYPE_01],
            [2, 3060, 294, platforms.PLAT_TYPE_01],
            [4, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
            [14, 630, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
            [30, 1700, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
            ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(platform[0], platform[1], platform[2], platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)
    
        # Add moving platforms (type, x, y, ...)
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 1350, 510, self.game,
            border_left=1250, border_right=1650, change_x=2, level=self))
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 1600, 360, self.game,
            border_left=1350, border_right=2620, change_x=7, level=self))
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
            block = platforms.SlidingBands(
                platform[0], platform[1], platform[2], self.game, velocity=platform[3], level=self)
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

        # Add potions
        self.potions.add([
            PotionPower(400, 660, self.game),
            PotionHealth(480, 660, self.game),
            ])

        # Add files_disks
        self.files_disks.add([
            FilesDiskC(340, 184, self.game),
            FilesDiskC(2200, 74, self.game),
            ])

        # Add life_recs
        self.life_recs.add([
            LifeRecoveryA(511, 183, self.game),
            ])

        # Add cartridges
        self.cartridges.add([
            CartridgeBlue(2700, 405, self.game),
            CartridgeBlue(2700, 366, self.game),
            CartridgeYellow(2740, 405, self.game),
            CartridgeRed(2780, 405, self.game),
            ])

        # Add computers
        self.computers.add([
            ComputerA(2860, 336, self.game),
            ])

        # Add NPCs
        self.npcs.add([
            SkullYellow(2360, 47, self.game, border_left=2180, border_right=2500, change_x=3),
            VampireMale(1880, 14, self.game, border_left=1865, border_right=2245, change_x=2),
            BatBlack(1900, 560, self.game, border_left=1780, border_right=2600, change_x=4),
            BatBlack(2120, 620, self.game, border_left=1780, border_right=2600, change_x=5),
            ])

        x = 76
        for _ in range(2):
            self.npcs.add(SkullYellow(
                320 + x, 145, self.game,
                border_left=300, border_right=650, change_x=randint(3, 5)))
            x += 60
        x = 54
        for _ in range(2):
            self.npcs.add(SkullRed(
                320 + x, 145, self.game,
                border_left=310, border_right=600, change_x=randint(5, 7)))
            x += 75

        items_to_drop = [
            DropItem(PotionPower, x_delta=16, **{'random_min': 65, 'random_max': 75}),
            DropItem(PotionPower, x_delta=-52, **{'random_min': 65, 'random_max': 75}),
            DropItem(PotionHealth, x_delta=80, **{'random_min': 65, 'random_max': 75}),
            DropItem(LifeRecoveryA, x_delta=120),
            DropItem(CartridgeGreen, x_delta=170),
            DropItem(CartridgeBlue, x_delta=195),
            ]
        self.snakes.add(SnakeRed(1100, 560, self.game, border_left=395, border_right=1550,
                                 border_top=100, border_down=820, change_x=2, change_y=2,
                                 items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionPower, x_delta=16, **{'random_min': 65, 'random_max': 75}),
            DropItem(LifeRecoveryA, probability_to_drop=25, x_delta=120),
            DropItem(CartridgeGreen, x_delta=170),
            DropItem(CartridgeBlue, x_delta=195),
            ]
        self.snakes.add(SnakeBlue(300, 360, self.game, border_left=295, border_right=1450,
                                  border_top=100, border_down=810, change_x=1, change_y=2,
                                  items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionPower, probability_to_drop=30, x_delta=16,
                     **{'random_min': 65, 'random_max': 75}),
            ]
        self.snakes.add(SnakeGreen(800, 415, self.game, border_left=285, border_right=1750,
                                   border_top=100, border_down=810, change_x=1, change_y=1,
                                   items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionPower, x_delta=16,
                     **{'random_min': 65, 'random_max': 75}),
            DropItem(CartridgeGreen, x_delta=170),
            ]
        self.snakes.add(SnakeYellow(2050, 640, self.game, border_left=800, border_right=2350,
                                    border_top=100, border_down=810, change_x=4, change_y=4,
                                    items_to_drop=items_to_drop))

        # Add mines
        x = 1140
        for _ in range(5):
            y = 100
            for __ in range(28):
                self.mines.add(MineLilac(x, y, self.game))
                y += 22
            x += 25

        # Add doors
        self.doors.add([
            DoorLeftRed(2, 550, self.game, level_dest=4, door_dest_pos=DOOR_DEST_NL),
            DoorLeftAqua(2786, -90, self.game, level_dest=8, door_dest_pos=DOOR_DEST_TR, is_locked=True),
            DoorRightGreen(3400, 550, self.game, level_dest=6, door_dest_pos=DOOR_DEST_NL),
            ])

        # Add door keys
        self.door_keys.add([
            DoorKeyAqua(2740, 374, self.game, door=[door for door in self.doors if door.is_locked][0]),
            ])
