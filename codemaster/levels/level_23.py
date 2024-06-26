"""Module level 23."""
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
    DemonMale,
    SkullYellow,
    SkullRed,
    TethlorienLilac,
    )
from codemaster.models.actors.items import (
    BatteryA,
    DoorLeftBlue,
    DoorRightRed,
    PotionHealth,
    )
from codemaster.levels.level_base import Level


class Level23(Level):

    def __init__(self, game):
        super().__init__(game)
        self.id = 22
        self.name = str(self.id + 1)
        self.next_level_left = self.id - 1
        self.next_level_right = 1
        self.next_level_top = False
        self.next_level_bottom = False
        self.background = pg.image.load(self.file_name_im_get(4)).convert()
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

        self._add_actors()
        self._sprites_all_add()

    def _add_actors(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [[5, 300, 220, platforms.PLAT_TYPE_01],
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
                       [1, 3200, 196, platforms.PLAT_TYPE_01],
                       [1, 3060, 294, platforms.PLAT_TYPE_01],
                       [1, 2395, 586, platforms.PLAT_TYPE_01],
                       [19, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],  # earth
                       [24, 2140, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],  # earth
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
            BatteryA(2160, 74, self.game),
            BatteryA(2200, 74, self.game),
            ])

        # Add NPCs
        self.npcs.add([
            SkullYellow(2360, 47, self.game, border_left=2080, border_right=2500, change_x=3),
            SkullRed(2410, 47, self.game, border_left=2170, border_right=2500, change_x=3),
            ])

        items_to_drop = [
            DropItem(PotionHealth, ActorType.POTION_POWER, probability_to_drop=100, add_to_list=self.potions,
                     **{'random_min': 60, 'random_max': 60}),
            ]
        self.npcs.add(DemonMale(
            600, 146, self.game,
            border_left=300, border_right=600, change_x=2, items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionHealth, ActorType.POTION_POWER, probability_to_drop=100, add_to_list=self.potions,
                     **{'random_min': 25, 'random_max': 30}),
            ]
        tethlorien_lilac = TethlorienLilac(
            1500, 240, self.game,
            border_left=1320, border_right=1680, change_x=2, items_to_drop=items_to_drop)
        self.npcs.add(tethlorien_lilac)
        EnergyShield.actor_acquire_energy_shield(tethlorien_lilac, self.game, health_total=200)
        tethlorien_lilac.stats.energy_shield.activate()

        # Add doors
        self.doors.add([
            DoorLeftBlue(2, 550, self.game, level_dest=21, door_dest_pos=DOOR_DEST_NL),
            DoorRightRed(3640, 550, self.game, level_dest=23, door_dest_pos=DOOR_DEST_NL),
            ])
