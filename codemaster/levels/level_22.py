"""Module level 22."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    DOOR_DEST_TR,
    )
from codemaster.models.actors.actors import DropItem
from codemaster.models.actors.items import platforms
from codemaster.models.actors.npcs import (
    SkullGreen,
    SkullYellow,
    SkullRed,
    SamuraiMale,
    TerminatorEyeYellow,
    )
from codemaster.models.actors.items import (
    BatteryA,
    CartridgeBlue,
    CartridgeGreen,
    ComputerA,
    DoorLeftYellow,
    DoorRightAqua,
    DoorRightBlue,
    PotionHealth,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level22(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(12)).convert()
        self.player_start_pos_left = 220, 520
        self.player_start_pos_right = 520, 520
        self.player_start_pos_rtop = 880, -292
        self.player_start_pos_ltop = 80, 100
        
        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [[12, 420, 210, platforms.PLAT_TYPE_01],
                       [5, 3270, 240, platforms.PLAT_TYPE_01],
                       [1, 3200, 360, platforms.PLAT_TYPE_01],
                       [10, 1960, 130, platforms.PLAT_TYPE_01],
                       [2, 1500, 210, platforms.PLAT_TYPE_01],
                       [2, 1680, 300, platforms.PLAT_TYPE_01],
                       [2, 1420, 575, platforms.PLAT_TYPE_01],
                       [21, 1640, 460, platforms.PLAT_TYPE_01],
                       [56, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
                       ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(platform[0], platform[1], platform[2],
                                                                       platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add batteries
        self.batteries.add([
            BatteryA(2180, 94, self.game),
            BatteryA(2220, 94, self.game),
            BatteryA(2260, 94, self.game),
            BatteryA(2300, 94, self.game),
            BatteryA(760, 174, self.game),
            BatteryA(800, 174, self.game),
            BatteryA(840, 174, self.game),
            ])

        # Add computers
        self.computers.add([
            ComputerA(2800, 356, self.game),
            ])

        # Add NPCs
        self.npcs.add([
            SkullGreen(2100, 67, self.game, border_left=1950, border_right=2200, change_x=3),
            SkullYellow(2360, 67, self.game, border_left=2080, border_right=2500, change_x=3),
            SkullRed(2460, 67, self.game, border_left=2170, border_right=2500, change_x=3),
            ])

        items_to_drop = [
            DropItem(PotionPower, x_delta=16, **{'random_min': 58, 'random_max': 72}),
            DropItem(CartridgeGreen, x_delta=170),
            DropItem(CartridgeBlue, probability_to_drop=80, x_delta=195),
                ]
        self.npcs.add([
            TerminatorEyeYellow(2300, 48, self.game, border_left=2000, border_right=2480, change_x=2,
                                items_to_drop=items_to_drop),
                ])

        items_to_drop = [
            DropItem(CartridgeBlue, x_delta=50),
            ]
        self.npcs.add(SamuraiMale(
            620, 127, self.game,
            border_left=550, border_right=1130, change_x=2, items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionHealth, **{'random_min': 30, 'random_max': 40}),
            ]
        self.npcs.add(SamuraiMale(
            1000, 127, self.game,
            border_left=440, border_right=1100, change_x=2, items_to_drop=items_to_drop))

        # Add doors
        self.doors.add([
            DoorLeftYellow(2, 550, self.game, level_dest=20, door_dest_pos=DOOR_DEST_NL),
            DoorRightAqua(3480, 52, self.game, level_dest=18, door_dest_pos=DOOR_DEST_TR),
            DoorRightBlue(3640, 550, self.game, level_dest=22, door_dest_pos=DOOR_DEST_NL),
            ])
