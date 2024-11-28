"""Module level 27."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    )
from codemaster.models.actors.actors import DropItem
from codemaster.models.actors.items import platforms
from codemaster.models.actors.items.energy_shields import EnergyShield
from codemaster.models.actors.npcs import (
    EwlanMale,
    RobotA,
    RobotB,
    SquirrelA,
    )
from codemaster.models.actors.items import (
    AppleGreen,
    AppleRed,
    AppleYellow,
    BatteryA,
    CartridgeGreen,
    DoorLeftGreen,
    DoorRightYellow,
    PotionHealth,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level27(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(12)).convert()
        self.player_start_pos_left = 220, 408
        self.player_start_pos_right = 600, 408
        self.player_start_pos_rtop = 880, -292
        self.player_start_pos_ltop = 80, 100

        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [
            [2, 1520, 290, platforms.PLAT_TYPE_01],
            [3, 1760, 110, platforms.PLAT_TYPE_01],
            [2, 2200, 110, platforms.PLAT_TYPE_01],
            [8, 2500, 110, platforms.PLAT_TYPE_01],
            [7, 2530, 440, platforms.PLAT_TYPE_01],
            [6, 3190, 246, platforms.PLAT_TYPE_01],
            [1, 3090, 315, platforms.PLAT_TYPE_01],
            [1, 2395, 586, platforms.PLAT_TYPE_01],
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
            BatteryA(1532, 254, self.game),
            BatteryA(1570, 254, self.game),
            BatteryA(2710, 74, self.game),
            ])

        # Add apples
        self.apples.add([
            AppleGreen(3400, 222, self.game),
            AppleRed(3440, 222, self.game),
            AppleYellow(3490, 222, self.game),
            AppleYellow(3540, 222, self.game),
            ])

        # Add NPCs
        self.npcs.add([
            SquirrelA(700, 686, self.game, border_left=690, border_right=1210, change_x=2),
            SquirrelA(740, 686, self.game, border_left=690, border_right=1210, change_x=3),
            SquirrelA(820, 686, self.game, border_left=700, border_right=1210, change_x=2),
            SquirrelA(860, 686, self.game, border_left=690, border_right=1210, change_x=1),
            SquirrelA(900, 686, self.game, border_left=700, border_right=1210, change_x=2),
            ])

        robot_items_to_drop = [
            DropItem(PotionPower, y_delta=20, **{'random_min': 25, 'random_max': 25}),
            ]
        items_to_drop = [
            DropItem(PotionHealth, x_delta=-26, **{'random_min': 25, 'random_max': 25}),
            DropItem(RobotB, y_delta=-20, items_to_drop=robot_items_to_drop,
                     **{'border_left': 800, 'border_right': 1200, 'change_x': 2}),
            ]
        self.npcs.add([
            SquirrelA(1100, 686, self.game, border_left=800, border_right=1200, change_x=2,
                      items_to_drop=items_to_drop),
            ])

        items_to_drop = [
            DropItem(PotionPower, x_delta=16, **{'random_min': 45, 'random_max': 45}),
            ]
        self.npcs.add(RobotA(
            1820, 37, self.game, border_left=1764, border_right=1920, change_x=2,
            items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionHealth, x_delta=-22, **{'random_min': 58, 'random_max': 72}),
            DropItem(CartridgeGreen, x_delta=22),
            ]
        ewlan_male = EwlanMale(2600, 358, self.game, border_left=2550, border_right=2940,
                      change_x = 2, items_to_drop = items_to_drop)
        self.npcs.add(ewlan_male)
        EnergyShield.actor_acquire_energy_shield(ewlan_male, self.game, health_total=200)

        # Add doors
        self.doors.add([
            DoorLeftGreen(2, 550, self.game, level_dest=25, door_dest_pos=DOOR_DEST_NL),
            DoorRightYellow(3640, 550, self.game, level_dest=27, door_dest_pos=DOOR_DEST_NL),
            ])
