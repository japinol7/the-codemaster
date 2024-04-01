"""Module level 8."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    )
from codemaster.models.actors.items import platforms
from codemaster.models.actors.decorations import Water
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.actors import DropItem
from codemaster.models.actors.npcs import (
    BatBlack,
    BatBlue,
    RobotA,
    RobotB,
    SkullGreen,
    SkullYellow,
    WolfManMale,
    )
from codemaster.models.actors.items import (
    CartridgeGreen,
    CartridgeBlue,
    BatteryA,
    DoorRightWhite,
    DoorLeftYellow,
    FilesDiskB,
    PotionHealth,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level8(Level):

    def __init__(self, game):
        super().__init__(game)
        self.id = 7
        self.name = '08'
        self.next_level_left = 6
        self.next_level_right = 8
        self.next_level_top = False
        self.next_level_bottom = False
        self.background = pg.image.load(self.file_name_im_get(8)).convert()
        self.level_limit = -3000
        self.level_limit_top = -1000
        self.player_start_pos_left = (250, 520)
        self.player_start_pos_right = (520, 520)
        self.player_start_pos_rtop = (250, -440)
        self.player_start_pos_ltop = (80, 100)
        self.player_start_pos_bottom = (300, 800)
        self.world_start_pos_left = (0, -758)
        self.world_start_pos_right = (self.level_limit + self.SCROLL_LV_NEAR_RIGHT_SIDE, -758)
        self.world_start_pos_rtop = (self.level_limit + 500 + self.SCROLL_LV_NEAR_RIGHT_SIDE, -900)
        self.world_start_pos_ltop = (0, -900)

        self._add_actors()
        self._sprites_all_add()

    def _add_actors(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [[11, 2000, -16, platforms.PLAT_TYPE_01],
                       [12, 2600, 160, platforms.PLAT_TYPE_01],
                       [6, 20, 160, platforms.PLAT_TYPE_01],
                       [7, 740, 84, platforms.PLAT_TYPE_01],
                       [7, 1400, 84, platforms.PLAT_TYPE_01],
                       [5, 600, 280, platforms.PLAT_TYPE_01],
                       [13, 1200, 280, platforms.PLAT_TYPE_01],
                       [7, 740, 476, platforms.PLAT_TYPE_01],
                       [8, 1660, 476, platforms.PLAT_TYPE_01],
                       [7, 2400, 476, platforms.PLAT_TYPE_01],
                       [2, 1380, 585, platforms.PLAT_TYPE_01],
                       [56, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],  # earth
                       ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(platform[0], platform[1], platform[2], platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add water blocks
        Water.create_water(0, SCREEN_NEAR_EARTH + 216, self.game, qty=20, qty_depth=3, add_to_list=self.decors)

        # Add batteries
        self.batteries.add([
            BatteryA(26, 124, self.game),
            BatteryA(3340, 124, self.game),
            BatteryA(3380, 124, self.game),
            ])

        # Add files_disks
        self.files_disks.add([
            FilesDiskB(3290, 124, self.game),
            ])

        # Add potions
        self.potions.add([
            PotionPower(2630, -54, self.game),
            PotionHealth(2670, -54, self.game),
            PotionPower(2630, -92, self.game),
            PotionHealth(2670, -92, self.game),
            ])

        # Add NPCs
        self.npcs.add([
            BatBlue(634, -26, self.game, border_left=610, border_right=1300, change_x=3),
            BatBlue(780, 16, self.game, border_left=610, border_right=1300, change_x=3),
            BatBlue(2220, -86, self.game, border_left=2140, border_right=2660, change_x=3),
            BatBlack(2320, 356, self.game, border_left=1670, border_right=2850, change_x=3),
            BatBlack(1994, 379, self.game, border_left=1670, border_right=2850, change_x=3),
            SkullGreen(20, 90, self.game, border_left=10, border_right=380, change_x=3),
            SkullGreen(90, 90, self.game, border_left=10, border_right=380, change_x=3),
            SkullYellow(240, 90, self.game, border_left=10, border_right=380, change_x=2),
            WolfManMale(1700, 207, self.game, border_left=1490, border_right=2010, change_x=2),
            WolfManMale(1780, 207, self.game, border_left=1500, border_right=2004, change_x=2),
            ])

        items_to_drop = [
            DropItem(CartridgeGreen, ActorType.CARTRIDGE_BLUE, probability_to_drop=100,
                     add_to_list=self.cartridges, x_delta=16),
            ]

        self.npcs.add(RobotB(
            3020, 86, self.game, border_left=2620, border_right=3380, change_x=2,
            items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionPower, ActorType.POTION_POWER, probability_to_drop=100, add_to_list=self.potions,
                     x_delta=16, **{'random_min': 70, 'random_max': 80}),
            DropItem(CartridgeBlue, ActorType.CARTRIDGE_GREEN, probability_to_drop=100,
                     add_to_list=self.cartridges, x_delta=60),
            ]
        self.npcs.add(RobotA(
            2940, 86, self.game, border_left=2590, border_right=3400, change_x=3,
            items_to_drop=items_to_drop))

        # Add doors
        self.doors.add([
            DoorLeftYellow(2, 550, self.game, level_dest=6, door_dest_pos=DOOR_DEST_NL),
            DoorRightWhite(3640, 550, self.game, level_dest=8, door_dest_pos=DOOR_DEST_NL),
            ])
