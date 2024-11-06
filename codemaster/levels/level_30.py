"""Module level 28."""
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
    GhostGreen,
    GhostYellow,
    GhostRed,
    SnakeGreen,
    SnakeRed,
    VampireFemale,
    )
from codemaster.models.actors.items import (
    BatteryA,
    CartridgeBlue,
    CartridgeYellow,
    DoorLeftRed,
    DoorRightAqua,
    FilesDiskA,
    LifeRecoveryA,
    PotionHealth,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level30(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(3)).convert()
        self.player_start_pos_left = 220, 520
        self.player_start_pos_right = 520, 520
        self.player_start_pos_rtop = 880, -292
        self.player_start_pos_ltop = 80, 100
        
        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [
            [5, 300, 220, platforms.PLAT_TYPE_01],
            [3, 800, 440, platforms.PLAT_TYPE_01],
            [1, 1080, 586, platforms.PLAT_TYPE_01],
            [2, 670, 300, platforms.PLAT_TYPE_01],
            [8, 2500, 110, platforms.PLAT_TYPE_01],
            [6, 2580, 440, platforms.PLAT_TYPE_01],
            [5, 3260, 240, platforms.PLAT_TYPE_01],
            [2, 3086, 310, platforms.PLAT_TYPE_01],
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
            BatteryA(2710, 74, self.game),
            BatteryA(2750, 74, self.game),
            ])

        # Add potions
        self.potions.add([
            PotionPower(330, 184, self.game),
            PotionPower(2670, 75, self.game),
            PotionPower(2970, 75, self.game),
            PotionHealth(380, 184, self.game),
            ])

        # Add files_disks
        self.files_disks.add([
            FilesDiskA(2800, 72, self.game),
            ])

        # Add life_recs
        self.life_recs.add([
            LifeRecoveryA(2844, 68, self.game),
            ])

        # Add cartridges
        self.cartridges.add([
            CartridgeBlue(2890, 75, self.game),
            CartridgeBlue(2890, 38, self.game),
            CartridgeYellow(2930, 75, self.game),
            ])

        # Add NPCs
        self.npcs.add([
            GhostGreen(310, 158, self.game, border_left=260, border_right=780, change_x=2),
            GhostYellow(360, 158, self.game, border_left=260, border_right=720, change_x=3),
            GhostRed(670, 158, self.game, border_left=300, border_right=800, change_x=2),
            ])

        item_to_drop = DropItem(CartridgeYellow)
        self.npcs.add(VampireFemale(
            2800, 38, self.game, border_left=2680, border_right=2980,
            change_x=2, items_to_drop=[item_to_drop]))

        items_to_drop = [
            DropItem(PotionPower, probability_to_drop=60, x_delta=16,
                     **{'random_min': 30, 'random_max': 40}),
            ]
        self.snakes.add(SnakeGreen(1500, 415, self.game, border_left=1210, border_right=2940,
                                   border_top=90, border_down=810, change_x=1, change_y=1,
                                   items_to_drop=items_to_drop))

        items_to_drop = [
            DropItem(PotionPower, probability_to_drop=80, x_delta=16,
                     **{'random_min': 60, 'random_max': 65}),
            DropItem(LifeRecoveryA, x_delta=70),
            ]
        self.snakes.add(SnakeRed(2100, 500, self.game, border_left=1300, border_right=2980,
                                 border_top=100, border_down=806, change_x=3, change_y=3,
                                 items_to_drop=items_to_drop))

        # Add doors
        self.doors.add([
            DoorLeftRed(2, 550, self.game, level_dest=28, door_dest_pos=DOOR_DEST_NL),
            DoorRightAqua(3472, 52, self.game, level_dest=22, door_dest_pos=DOOR_DEST_TR),
            ])
