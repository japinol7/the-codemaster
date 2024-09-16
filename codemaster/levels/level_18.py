"""Module level 18."""
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
    DemonMale,
    GhostGreen,
    GhostYellow,
    SkullYellow,
    SkullRed,
    TethlorienLilac,
    TethlorienRed,
    )
from codemaster.models.actors.items import (
    BatteryA,
    CartridgeBlue,
    CartridgeYellow,
    CartridgeRed,
    DoorLeftYellow,
    DoorRightBlue,
    FilesDiskA,
    LifeRecoveryA,
    PotionHealth,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level18(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(3)).convert()
        self.player_start_pos_left = 220, 520
        self.player_start_pos_right = 520, 520
        self.player_start_pos_rtop = 250, -440
        self.player_start_pos_ltop = 80, 100
        
        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [[5, 300, 220, platforms.PLAT_TYPE_01],
                       [3, 800, 440, platforms.PLAT_TYPE_01],
                       [2, 670, 300, platforms.PLAT_TYPE_01],
                       [3, 1100, 260, platforms.PLAT_TYPE_01],
                       [9, 1900, 110, platforms.PLAT_TYPE_01],
                       [6, 2580, 440, platforms.PLAT_TYPE_01],
                       [5, 2680, 98, platforms.PLAT_TYPE_01],
                       [2, 3340, 98, platforms.PLAT_TYPE_01],
                       [2, 3200, 196, platforms.PLAT_TYPE_01],
                       [2, 3060, 294, platforms.PLAT_TYPE_01],
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
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 1350, 260, self.game,
            border_top=200, border_down=920, change_y=3, level=self))

        # Add sliding bands (n_blocs, x, y, type, velocity)
        level_plats = [
            [3, 1500, 120, platforms.PLAT_TYPE_03_SLIDING, 3]
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
            BatteryA(2160, 74, self.game),
            BatteryA(2200, 74, self.game),
            BatteryA(2240, 74, self.game),
            BatteryA(2280, 74, self.game),
            ])

        # Add potions
        self.potions.add([
            PotionPower(330, 184, self.game),
            PotionHealth(380, 184, self.game),
            ])

        # Add files_disks
        self.files_disks.add([
            FilesDiskA(2376, 72, self.game),
            ])

        # Add life_recs
        self.life_recs.add([
            LifeRecoveryA(2324, 68, self.game),
            ])

        # Add cartridges
        self.cartridges.add([
            CartridgeBlue(2800, 62, self.game),
            CartridgeBlue(2800, 24, self.game),
            CartridgeYellow(2840, 62, self.game),
            CartridgeRed(2880, 62, self.game),
            ])

        # Add NPCs
        self.npcs.add([
            GhostGreen(910, 180, self.game, border_left=800, border_right=1300, change_x=2),
            GhostYellow(960, 180, self.game, border_left=800, border_right=1700, change_x=3),
            SkullYellow(2360, 47, self.game, border_left=2080, border_right=2500, change_x=3),
            SkullRed(2410, 47, self.game, border_left=2170, border_right=2500, change_x=3),
            ])

        items_to_drop = [
            DropItem(PotionPower, **{'random_min': 65, 'random_max': 65}),
            DropItem(CartridgeBlue, x_delta=95),
            ]
        self.npcs.add(DemonMale(
            1200, 186, self.game,
            border_left=1100, border_right=1280, change_x=2, items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionHealth, **{'random_min': 60, 'random_max': 60}),
            ]
        self.npcs.add(DemonMale(
            600, 146, self.game,
            border_left=300, border_right=600, change_x=2, items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionPower, **{'random_min': 45, 'random_max': 45}),
            ]
        self.npcs.add(TethlorienRed(
            2200, 32, self.game,
            border_left=2080, border_right=2450, change_x=2, items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionHealth, **{'random_min': 25, 'random_max': 30}),
            ]
        tethlorien_lilac = TethlorienLilac(
            3390, 20, self.game,
            border_left=3320, border_right=3440, change_x=1, items_to_drop=items_to_drop)
        self.npcs.add(tethlorien_lilac)
        EnergyShield.actor_acquire_energy_shield(tethlorien_lilac, self.game, health_total=200)

        # Add doors
        self.doors.add([
            DoorLeftYellow(2, 550, self.game, level_dest=16, door_dest_pos=DOOR_DEST_NL),
            DoorRightBlue(3640, 550, self.game, level_dest=18, door_dest_pos=DOOR_DEST_NL),
            ])
