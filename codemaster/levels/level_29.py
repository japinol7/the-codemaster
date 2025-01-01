"""Module level 29."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    )
from codemaster.models.actors.items import platforms
from codemaster.models.actors.items.energy_shields import EnergyShield
from codemaster.models.actors.actors import DropItem
from codemaster.models.actors.decorations import (
    Grass,
    Water,
    )
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.npcs import (
    BatBlack,
    KungFuFighterMale,
    SquirrelA,
    TethlorienLilac,
    TerminatorEyeRed,
    )
from codemaster.models.actors.items import (
    BatteryA,
    CartridgeGreen,
    CartridgeBlue,
    CartridgeYellow,
    CartridgeRed,
    DoorLeftBlue,
    DoorRightRed,
    PotionHealth,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level29(Level):

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
            [8, 2000, -16, platforms.PLAT_TYPE_01],
            [8, 2600, 84, platforms.PLAT_TYPE_01],
            [2, 20, 300, platforms.PLAT_TYPE_01],
            [1, 368, 350, platforms.PLAT_TYPE_01],
            [7, 740, 150, platforms.PLAT_TYPE_01],
            [6, 1400, 150, platforms.PLAT_TYPE_01],
            [1, 600, 400, platforms.PLAT_TYPE_01],
            [9, 1200, 440, platforms.PLAT_TYPE_01],
            [1, 1970, 280, platforms.PLAT_TYPE_01],
            [5, 1860, 586, platforms.PLAT_TYPE_01],
            [12, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
            [22, 2320, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
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
        Grass.create_grass_sm(
            0, SCREEN_NEAR_EARTH , self.game, qty=6, qty_depth=5,
            actor_type=ActorType.PLAT_GRASS_S_SM)
        Grass.create_grass_sm(
            2320, SCREEN_NEAR_EARTH , self.game, qty=12, qty_depth=5,
            actor_type=ActorType.PLAT_GRASS_S_SM)

        # Add moving platforms (type, x, y, ...)
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 1000, 586, self.game,
            border_left=790, border_right=1120, change_x=2, level=self))

        # Add batteries
        self.batteries.add([
            BatteryA(36, 263, self.game),
            BatteryA(3086, 49, self.game),
            ])

        # Add cartridges
        self.cartridges.add([
            CartridgeGreen(760, 115, self.game),
            CartridgeBlue(800, 115, self.game),
            CartridgeYellow(800, 78, self.game),
            ])

        # Add NPCs
        self.npcs.add([
            BatBlack(2650, -20, self.game, border_left=2600, border_right=3090, change_x=2),
            BatBlack(2850, 10, self.game, border_left=2600, border_right=3090, change_x=2),
            BatBlack(3050, -20, self.game, border_left=2600, border_right=3090, change_x=2),
            ])

        kff_items_to_drop = [
            DropItem(PotionHealth, **{'random_min': 20, 'random_max': 20}),
            DropItem(PotionPower, x_delta=50, **{'random_min': 25, 'random_max': 25}),
            ]
        items_to_drop = [
            DropItem(CartridgeRed, x_delta=16),
            DropItem(KungFuFighterMale, y_delta=-31, items_to_drop=kff_items_to_drop,
                     **{'border_left': 1200, 'border_right': 1800, 'change_x': 2}),
            ]
        self.npcs.add([
            SquirrelA(1300, 388, self.game, border_left=1200, border_right=1800, change_x=2),
            SquirrelA(1400, 388, self.game, border_left=1200, border_right=1800, change_x=1),
            SquirrelA(1500, 388, self.game, border_left=1200, border_right=1800, change_x=2,
                      items_to_drop=items_to_drop),
            SquirrelA(1600, 388, self.game, border_left=1200, border_right=1800, change_x=2),
            SquirrelA(1700, 388, self.game, border_left=1200, border_right=1800, change_x=1),
            ])

        items_to_drop = [
            DropItem(PotionPower, probability_to_drop=80, x_delta=16,
                     **{'random_min': 50, 'random_max': 75}),
            DropItem(CartridgeYellow, probability_to_drop=70, x_delta=60),
            ]
        self.npcs.add([
            TerminatorEyeRed(
                1500, 66, self.game, border_left=1400, border_right=1790, change_x=2,
                items_to_drop=items_to_drop),
            ])

        item_to_drop = DropItem(PotionHealth, **{'random_min': 25, 'random_max': 30})
        tethlorien_lilac = TethlorienLilac(
            1700, 72, self.game, border_left=1400, border_right=1790,
            change_x=2, items_to_drop=[item_to_drop])
        self.npcs.add(tethlorien_lilac)
        EnergyShield.actor_acquire_energy_shield(tethlorien_lilac, self.game, health_total=200)

        # Add doors
        self.doors.add([
            DoorLeftBlue(0, 550, self.game, level_dest=27, door_dest_pos=DOOR_DEST_NL),
            DoorRightRed(3640, 550, self.game, level_dest=29, door_dest_pos=DOOR_DEST_NL),
            ])
