"""Module level 11."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    DOOR_DEST_NL,
    DIRECTION_LEFT,
    SCREEN_NEAR_EARTH,
    )
from codemaster.models.actors.items import platforms
from codemaster.models.actors.actors import DropItem
from codemaster.models.actors.decorations import Water
from codemaster.models.actors.npcs import (
    MageFemaleA,
    MageFemaleAVanished,
    )
from codemaster.models.actors.items import (
    BatteryA,
    DoorKeyMagenta,
    DoorLeftBlue,
    DoorRightMagenta,
    PotionPower,
    )
from codemaster.levels.level_base import Level


class Level11(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(6)).convert()
        self.player_start_pos_left = 220, 520
        self.player_start_pos_right = 520, 520
        self.player_start_pos_rtop = 250, -440
        self.player_start_pos_ltop = 80, 100
        
        super().__init__(id_, game)

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [
            [12, 420, 210, platforms.PLAT_TYPE_01],
            [2, 1400, 200, platforms.PLAT_TYPE_01],
            [2, 1580, 300, platforms.PLAT_TYPE_01],
            [2, 1420, 575, platforms.PLAT_TYPE_01],
            [21, 1640, 460, platforms.PLAT_TYPE_01],
            [56, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
            ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(platform[0], platform[1], platform[2], platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add water blocks
        Water.create_water(0, SCREEN_NEAR_EARTH + 216, self.game, qty=20, qty_depth=3)

        # Add batteries
        self.batteries.add([
            BatteryA(460, 174, self.game),
            ])

        # Add potions
        self.potions.add([
            PotionPower(510, 174, self.game),
            ])

        # Add doors
        self.doors.add([
            DoorLeftBlue(2, 550, self.game, level_dest=9, door_dest_pos=DOOR_DEST_NL),
            DoorRightMagenta(3640, 550, self.game, level_dest=11, door_dest_pos=DOOR_DEST_NL, is_locked=True),
            ])

        # Add NPCs
        items_to_drop = [
            DropItem(PotionPower, x_delta=22, y_delta=38, **{'random_min': 68, 'random_max': 85}),
            DropItem(DoorKeyMagenta, x_delta=20, y_delta=58,
                     door=[door for door in self.doors if door.is_locked][0]),
            DropItem(MageFemaleAVanished, x_delta=0),
            ]
        mage = MageFemaleA(3570, 655, self.game, items_to_drop=items_to_drop)
        mage.direction = DIRECTION_LEFT
        self.npcs.add([mage])
