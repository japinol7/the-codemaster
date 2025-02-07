"""Module level 23."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    DOOR_DEST_TR,
    )
from codemaster.models.actors.actors import DropItem
from codemaster.models.actors.items import platforms
from codemaster.models.actors.items.energy_shields import EnergyShield
from codemaster.models.actors.decorations import (
    Grass,
    Water,
    )
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.npcs import (
    DemonMale,
    SkullYellow,
    SkullRed,
    TethlorienLilac,
    )
from codemaster.models.actors.items import (
    BatteryA,
    DoorLeftBlue,
    DoorRightAqua,
    DoorRightRed,
    PotionHealth,
    )
from codemaster.levels.level_base import Level


class Level23(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(4)).convert()
        self.player_start_pos_left = 220, 408
        self.player_start_pos_right = 600, 408
        self.player_start_pos_rtop = 880, -292
        self.player_start_pos_ltop = 80, 100
        
        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [
            [5, 300, 220, platforms.PLAT_TYPE_01],
            [1, 1740, 250, platforms.PLAT_TYPE_01],
            [1, 1500, 320, platforms.PLAT_TYPE_01],
            [1, 1700, 470, platforms.PLAT_TYPE_01],
            [1, 1500, 586, platforms.PLAT_TYPE_01],
            [2, 800, 440, platforms.PLAT_TYPE_01],
            [1, 670, 300, platforms.PLAT_TYPE_01],
            [3, 1100, 260, platforms.PLAT_TYPE_01],
            [9, 1900, 110, platforms.PLAT_TYPE_01],
            [6, 2580, 440, platforms.PLAT_TYPE_01],
            [4, 2730, 98, platforms.PLAT_TYPE_01],
            [6, 3200, 240, platforms.PLAT_TYPE_01],
            [1, 3060, 310, platforms.PLAT_TYPE_01],
            [1, 2395, 586, platforms.PLAT_TYPE_01],
            [18, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
            [24, 2140, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
            ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(platform[0], platform[1], platform[2],
                                                                       platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add water blocks
        Water.create_water(0, SCREEN_NEAR_EARTH + 216, self.game, qty=20, qty_depth=3)

        # Add grass blocks
        Grass.create_grass_sm(
            0, SCREEN_NEAR_EARTH , self.game, qty=9, qty_depth=5,
            actor_type=ActorType.PLAT_GRASS_E_SM)
        Grass.create_grass_sm(
            2140, SCREEN_NEAR_EARTH , self.game, qty=12, qty_depth=5,
            actor_type=ActorType.PLAT_GRASS_E_SM)

        # Add batteries
        self.batteries.add([
            BatteryA(2160, 74, self.game),
            BatteryA(2200, 74, self.game),
            ])

        # Add NPCs
        self.npcs.add([
            SkullYellow(2360, 47, self.game, border_left=2080, border_right=2500, change_x=3),
            SkullRed(2410, 47, self.game, border_left=2170, border_right=2500, change_x=3),
            ])

        item_to_drop = DropItem(PotionHealth, **{'random_min': 60, 'random_max': 60})
        self.npcs.add(DemonMale(
            600, 146, self.game,
            border_left=300, border_right=600, change_x=2, items_to_drop=[item_to_drop]))

        item_to_drop = DropItem(PotionHealth, **{'random_min': 25, 'random_max': 30})
        tethlorien_lilac = TethlorienLilac(
            1500, 240, self.game, border_left=1320, border_right=1680,
            change_x=2, items_to_drop=[item_to_drop])
        self.npcs.add(tethlorien_lilac)
        EnergyShield.actor_acquire_energy_shield(tethlorien_lilac, self.game, health_total=200)

        # Add doors
        self.doors.add([
            DoorLeftBlue(0, 550, self.game, level_dest=21, door_dest_pos=DOOR_DEST_NL),
            DoorRightAqua(3480, 52, self.game, level_dest=29, door_dest_pos=DOOR_DEST_TR),
            DoorRightRed(3640, 550, self.game, level_dest=23, door_dest_pos=DOOR_DEST_NL),
            ])
