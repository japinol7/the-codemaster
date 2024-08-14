"""Module level 25."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    )
from codemaster.models.actors.actors import DropItem, ActorType
from codemaster.models.actors.items import platforms
from codemaster.models.actors.items.energy_shields import EnergyShield
from codemaster.models.actors.npcs import (
    KungFuFighterMale,
    RobotB,
    TethlorienYellow,
    )
from codemaster.models.actors.items import (
    BatteryA,
    CartridgeGreen,
    CartridgeBlue,
    CartridgeYellow,
    DoorLeftGreen,
    DoorRightYellow,
    FilesDiskB,
    PotionHealth,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level25(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(12)).convert()
        self.player_start_pos_left = 220, 520
        self.player_start_pos_right = 520, 520
        self.player_start_pos_rtop = 250, -440
        self.player_start_pos_ltop = 80, 100

        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [[5, 300, 220, platforms.PLAT_TYPE_01],
                       [1, 715, 292, platforms.PLAT_TYPE_01],
                       [1, 900, 426, platforms.PLAT_TYPE_01],
                       [1, 1076, 562, platforms.PLAT_TYPE_01],
                       [3, 1100, 260, platforms.PLAT_TYPE_01],
                       [9, 1900, 110, platforms.PLAT_TYPE_01],
                       [6, 2580, 440, platforms.PLAT_TYPE_01],
                       [5, 2680, 98, platforms.PLAT_TYPE_01],
                       [3, 3340, 98, platforms.PLAT_TYPE_01],
                       [1, 3240, 196, platforms.PLAT_TYPE_01],
                       [1, 3100, 294, platforms.PLAT_TYPE_01],
                       [1, 2395, 586, platforms.PLAT_TYPE_01],
                       [19, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
                       [28, 2000, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
                       ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(platform[0], platform[1], platform[2],
                                                                       platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add moving platforms (type, x, y, ...)
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 1600, 360, self.game,
            border_left=1430, border_right=2620, change_x=4, level=self))

        # Add batteries
        self.batteries.add([
            BatteryA(2280, 74, self.game),
            ])

        # Add potions
        self.potions.add([
            PotionPower(330, 184, self.game),
            ])

        # Add files_disks
        self.files_disks.add([
            FilesDiskB(2324, 72, self.game),
            ])

        # Add cartridges
        self.cartridges.add([
            CartridgeBlue(2170, 73, self.game),
            CartridgeYellow(2210, 73, self.game),
            ])

        # Add NPCs
        items_to_drop = [
            DropItem(PotionPower, ActorType.POTION_POWER, probability_to_drop=100, add_to_list=self.potions,
                     **{'random_min': 30, 'random_max': 30}),
            ]
        self.npcs.add(RobotB(
            1200, 186, self.game,
            border_left=1100, border_right=1280, change_x=2, items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(CartridgeGreen, ActorType.CARTRIDGE_GREEN, probability_to_drop=100, add_to_list=self.cartridges,
                     x_delta=120),
            DropItem(PotionHealth, ActorType.POTION_HEALTH, probability_to_drop=100, add_to_list=self.potions,
                     **{'random_min': 60, 'random_max': 60}),
            ]
        kung_fu_fighter = KungFuFighterMale(
            600, 138, self.game,
            border_left=300, border_right=600, change_x=2, items_to_drop=items_to_drop)
        self.npcs.add(kung_fu_fighter)
        EnergyShield.actor_acquire_energy_shield(kung_fu_fighter, self.game, health_total=200)

        items_to_drop = [
            DropItem(PotionPower, ActorType.POTION_POWER, probability_to_drop=100, add_to_list=self.potions,
                     **{'random_min': 27, 'random_max': 27}),
            ]
        self.npcs.add(TethlorienYellow(
            2200, 32, self.game,
            border_left=2080, border_right=2450, change_x=2, items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(CartridgeBlue, ActorType.CARTRIDGE_BLUE, probability_to_drop=100, add_to_list=self.cartridges,
                     x_delta=100),
            DropItem(PotionHealth, ActorType.POTION_HEALTH, probability_to_drop=100, add_to_list=self.potions,
                     **{'random_min': 45, 'random_max': 45}),
            ]
        kung_fu_fighter = KungFuFighterMale(
            3390, 16, self.game,
            border_left=3320, border_right=3460, change_x=2, items_to_drop=items_to_drop)
        self.npcs.add(kung_fu_fighter)
        EnergyShield.actor_acquire_energy_shield(kung_fu_fighter, self.game, health_total=200)

        # Add doors
        self.doors.add([
            DoorLeftGreen(2, 550, self.game, level_dest=23, door_dest_pos=DOOR_DEST_NL),
            DoorRightYellow(3640, 550, self.game, level_dest=25, door_dest_pos=DOOR_DEST_NL),
            ])
