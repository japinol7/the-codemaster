"""Module level 4."""
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
    BatBlue,
    BatBlack,
    DemonMale,
    SnakeBlue,
    VampireMale,
    VampireFemale,
    WolfManMale,
    )
from codemaster.models.actors.items import (
    BatteryA,
    CartridgeGreen,
    CartridgeYellow,
    DoorRightBlue,
    DoorLeftYellow,
    DoorRightYellow,
    DoorKeyYellow,
    FilesDiskB,
    PotionHealth,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level4(Level):

    def __init__(self, id_, game):
        super().__init__(id_, game)
        self.background = pg.image.load(self.file_name_im_get(4)).convert()
        self.level_limit = -3000
        self.level_limit_top = -1000
        self.player_start_pos_left = 220, 520
        self.player_start_pos_right = 300, 520
        self.player_start_pos_rtop = 250, -440
        self.player_start_pos_ltop = 80, 100
        self.player_start_pos_bottom = 300, 800
        self.world_start_pos_left = 0, -758
        self.world_start_pos_right = self.level_limit + self.SCROLL_LV_NEAR_RIGHT_SIDE, -758
        self.world_start_pos_rtop = self.level_limit + 500 + self.SCROLL_LV_NEAR_RIGHT_SIDE, -900
        self.world_start_pos_ltop = 0, -900

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [[5, 100, 460, platforms.PLAT_TYPE_01],
                       [14, 300, 220, platforms.PLAT_TYPE_01],
                       [4, 980, 580, platforms.PLAT_TYPE_01],
                       [6, 1300, 120, platforms.PLAT_TYPE_01],
                       [7, 500, 450, platforms.PLAT_TYPE_01],
                       [2, 20, 340, platforms.PLAT_TYPE_01],
                       [9, 1900, 110, platforms.PLAT_TYPE_01],
                       [6, 2600, 10, platforms.PLAT_TYPE_01],
                       [22, 1350, 460, platforms.PLAT_TYPE_01],
                       [56, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
                       ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(platform[0], platform[1], platform[2], platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add water blocks
        Water.create_water(0, SCREEN_NEAR_EARTH + 216, self.game, qty=19, qty_depth=3, add_to_list=self.decors)

        # Add moving platforms (type, x, y, ...)
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 1600, 310, self.game,
            border_left=1350, border_right=2770, change_x=6, level=self))

        # Add batteries
        self.batteries.add([
            BatteryA(2410, 74, self.game),
            BatteryA(564, 415, self.game),
            BatteryA(614, 415, self.game),
            BatteryA(664, 415, self.game),
            ])

        # Add files_disks
        self.files_disks.add([
            FilesDiskB(2500, 74, self.game),
            ])

        # Add potions
        self.potions.add([
            PotionHealth(2350, 72, self.game),
            PotionPower(1000, 150, self.game),
            ])

        # Add NPCs
        items_to_drop = [
            DropItem(CartridgeYellow, ActorType.CARTRIDGE_YELLOW, probability_to_drop=100, add_to_list=self.cartridges),
            ]
        self.npcs.add(VampireFemale(
            1400, 46, self.game,
            border_left=1310, border_right=1680, change_x=2, items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionPower, ActorType.POTION_POWER, probability_to_drop=100, add_to_list=self.potions,
                     **{'random_min': 65, 'random_max': 75}),
            ]
        self.npcs.add(DemonMale(
            800, 146, self.game,
            border_left=690, border_right=1210, change_x=3, items_to_drop=items_to_drop))

        self.npcs.add([
            WolfManMale(2360, 37, self.game, border_left=2180, border_right=2500, change_x=3),
            VampireMale(1860, 14, self.game, border_left=1860, border_right=2240, change_x=2),
            BatBlack(510, 385, self.game, border_left=410, border_right=1100, change_x=3),
            BatBlack(760, 404, self.game, border_left=410, border_right=1100, change_x=3),
            WolfManMale(1900, 662, self.game, border_left=1900, border_right=2400, change_x=3),
            WolfManMale(2220, 662, self.game, border_left=1850, border_right=2250, change_x=2),
            BatBlue(2380, 346, self.game, border_left=1700, border_right=2450, change_x=3),
            BatBlue(2000, 365, self.game, border_left=1700, border_right=2450, change_x=3),
            ])

        items_to_drop = [
            DropItem(BatBlack, ActorType.BAT_BLACK, probability_to_drop=100, add_to_list=self.npcs,
                     **{'border_left': 1700, 'border_right': 2450, 'change_x': 3}),
            ]
        self.npcs.add(BatBlue(
            2190, 384, self.game,
            border_left=1700, border_right=2450, change_x=3, items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionPower, ActorType.POTION_POWER, probability_to_drop=100, add_to_list=self.potions,
                     x_delta=16, **{'random_min': 65, 'random_max': 75}),
            DropItem(CartridgeGreen, ActorType.CARTRIDGE_GREEN, probability_to_drop=100, add_to_list=self.cartridges,
                     x_delta=170),
            ]
        self.snakes.add(SnakeBlue(2250, 220, self.game, border_left=1800, border_right=2750,
                                  border_top=120, border_down=850, change_x=1, change_y=1,
                                  items_to_drop=items_to_drop))

        # Add doors
        self.doors.add([
            DoorRightBlue(3500, 550, self.game, level_dest=0, door_dest_pos=DOOR_DEST_NL),
            DoorLeftYellow(2, 550, self.game, level_dest=2, door_dest_pos=DOOR_DEST_NL),
            DoorRightYellow(2854, -179, self.game, level_dest=4, door_dest_pos=DOOR_DEST_NL, is_locked=True),
            ])

        # Add door keys
        self.door_keys.add([
            DoorKeyYellow(2800, 140, self.game, door=[door for door in self.doors if door.is_locked][0]),
            ])
