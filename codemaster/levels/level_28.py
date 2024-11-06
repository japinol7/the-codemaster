"""Module level 28."""
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
    AlienFelineMale,
    PokoyoA,
    PokoyoB,
    RobotA,
    SnakeYellow,
    )
from codemaster.models.actors.items import (
    BatteryA,
    CartridgeGreen,
    CartridgeYellow,
    DoorKeyBlue,
    DoorLeftYellow,
    DoorRightBlue,
    FilesDiskA,
    PotionHealth,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level28(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(13)).convert()
        self.player_start_pos_left = 220, 520
        self.player_start_pos_right = 520, 520
        self.player_start_pos_rtop = 880, -292
        self.player_start_pos_ltop = 80, 100

        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [
            [3, 456, 586, platforms.PLAT_TYPE_01],
            [2, 660, 424, platforms.PLAT_TYPE_01],
            [6, 900, 350, platforms.PLAT_TYPE_01],
            [6, 1450, 350, platforms.PLAT_TYPE_01],
            [6, 2000, 350, platforms.PLAT_TYPE_01],
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
            BatteryA(2290, 316, self.game),
            BatteryA(2325, 316, self.game),
            ])

        # Add files_disks
        self.files_disks.add([
            FilesDiskA(2370, 314, self.game),
            ])

        # Add rec_potions
        self.potions.add([
            PotionHealth(1180, 315, self.game),
            PotionPower(1240, 315, self.game),
            ])

        # Add NPCs
        pokoyos = [
            PokoyoA(1520, 140, self.game, border_top=80, border_down=280, change_y=3),
            PokoyoB(1590, 200, self.game, border_top=80, border_down=280, change_y=3),
            PokoyoA(1660, 110, self.game, border_top=80, border_down=280, change_y=3),
            PokoyoB(1730, 170, self.game, border_top=80, border_down=280, change_y=3),
            PokoyoA(1800, 260, self.game, border_top=80, border_down=280, change_y=3),
            ]
        self.npcs.add(pokoyos)

        item_to_drop = DropItem(CartridgeYellow, x_delta=50)
        self.npcs.add(RobotA(
            2130, 278, self.game, border_left=2000, border_right=2300, change_x=2,
            items_to_drop=[item_to_drop]))

        items_to_drop = [
            DropItem(PotionPower, y_delta=38, **{'random_min': 70, 'random_max': 75}),
            DropItem(PotionHealth, x_delta=44, y_delta=38, **{'random_min': 50, 'random_max': 75}),
            DropItem(CartridgeYellow, x_delta=90),
            ]
        alien_feline = AlienFelineMale(
            700, 660, self.game, border_left=690, border_right=1210, change_x=2,
            items_to_drop=items_to_drop)
        self.npcs.add([alien_feline])
        EnergyShield.actor_acquire_energy_shield(alien_feline, self.game, health_total=300)

        items_to_drop = [
            DropItem(PotionPower, probability_to_drop=60, **{'random_min': 45, 'random_max': 60}),
            DropItem(CartridgeGreen, x_delta=90),
            ]
        self.snakes.add(SnakeYellow(
            1500, 415, self.game, border_left=1000, border_right=2800,
            border_top=90, border_down=810, change_x=1, change_y=1,
            items_to_drop=items_to_drop))

        # Add doors
        self.doors.add([
            DoorLeftYellow(2, 550, self.game, level_dest=26, door_dest_pos=DOOR_DEST_NL),
            DoorRightBlue(3640, 550, self.game, level_dest=28, door_dest_pos=DOOR_DEST_NL, is_locked=True),
            ])

        # Add door keys
        self.door_keys.add([
            DoorKeyBlue(2220, 320, self.game, door=[door for door in self.doors if door.is_locked][0]),
            ])
