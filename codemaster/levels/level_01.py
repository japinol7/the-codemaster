"""Module level 1."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_HEIGHT,
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    )
from codemaster.models.actors.items import platforms
from codemaster.models.actors.actors import DropItem
from codemaster.models.actors.npcs import (
    BatBlue,
    BatBlack,
    GhostGreen,
    SkullBlue,
    SkullYellow,
    SquirrelA,
    )
from codemaster.models.actors.items import (
    BatteryA,
    DoorLeftBlue,
    DoorRightYellow,
    MineCyan,
    )
from codemaster.models.actors.decorations import Water
from codemaster.levels.level_base import Level


class Level1(Level):

    def __init__(self, id_, game):
        self.level_limit = -1800
        self.background = pg.image.load(self.file_name_im_get(1)).convert()
        self.player_start_pos_left = 220, 480
        self.player_start_pos_right = 600, 480
        self.player_start_pos_rtop = 300, 100
        self.player_start_pos_ltop = 80, 100
        self.world_start_pos_left = 0, -658

        super().__init__(id_, game)

        # Special init attributes for first level
        self.door_previous_pos_player = self.player_start_pos_left
        self.door_previous_pos_world = self.world_start_pos_left

    def _add_actors_hook(self):
        # Add platforms (blocs, x, y, type)
        level_plats = [
            [5, 100, 360, platforms.PLAT_TYPE_01],
            [3, 200, 190, platforms.PLAT_TYPE_01],
            [4, 500, 380, platforms.PLAT_TYPE_01],
            [7, 800, 90, platforms.PLAT_TYPE_01],
            [4, 1360, 560, platforms.PLAT_TYPE_01],
            [3, 1250, 420, platforms.PLAT_TYPE_01],
            [10, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
            [15, 800, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
            [24, 1950, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
            [15, 400, SCREEN_HEIGHT + 190, platforms.PLAT_TYPE_01],
            ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(platform[0], platform[1], platform[2], platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add water blocks
        Water.create_water(0, SCREEN_NEAR_EARTH + 206, self.game, qty=16, qty_depth=3)

        # Add moving platforms (type, x, y, ...)
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 1700, 610, self.game,
            border_left=1660, border_right=2200, change_x=2, level=self))
        self.platforms.add(platforms.MovingPlatform(
            platforms.PLAT_TYPE_02_STONE_MIDDLE, 500, 260, self.game,
            border_left=500, border_right=2100, change_x=8, level=self))

        # Add batteries
        self.batteries.add([
            BatteryA(100, 324, self.game),
            BatteryA(300, 324, self.game),
            BatteryA(1200, 54, self.game),
            ])

        # Add mines
        self.mines.add([
            MineCyan(400, 330, self.game),
            MineCyan(425, 330, self.game),
            ])

        # Add NPCs
        self.npcs.add([
            GhostGreen(500, 312, self.game, border_left=480, border_right=750, change_x=3),
            SkullBlue(410, 314, self.game, border_left=410, border_right=800, change_x=2),
            SkullYellow(600, 314, self.game, border_left=410, border_right=800, change_x=2),
            SquirrelA(900, 38, self.game, border_left=805, border_right=1218, change_x=2),
            ])

        items_to_drop = [
            DropItem(BatBlack,
                     **{'border_left': 640, 'border_right': 1040, 'change_x': 2}),
            ]
        self.npcs.add(BatBlue(
            640, 510, self.game,
            border_left=640, border_right=1040, change_x=2, items_to_drop=items_to_drop))

        # Add doors
        self.doors.add([
            DoorLeftBlue(2, 550, self.game, level_dest=3, door_dest_pos=DOOR_DEST_NL),
            DoorRightYellow(2570, 550, self.game, level_dest=1, door_dest_pos=DOOR_DEST_NL),
            ])
