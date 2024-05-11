"""Module level test 3."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    DOOR_DEST_NL,
    SCREEN_NEAR_EARTH,
    )
from codemaster.models.actors.items import platforms
from codemaster.models.actors.decorations import Water
from codemaster.models.actors.npcs import (
    BatBlack,
    )
from codemaster.models.actors.items import (
    DoorLeftBlue,
    DoorRightMagenta,
    )
from codemaster.levels.level_base import Level


class LevelTest3(Level):

    def __init__(self, game):
        super().__init__(game)
        self.id = 2
        self.name = str(self.id + 1)
        self.next_level_left = False
        self.next_level_right = False
        self.next_level_top = False
        self.next_level_bottom = False
        self.background = pg.image.load(self.file_name_im_get(9)).convert()
        self.level_limit = -3000
        self.level_limit_top = -1000
        self.player_start_pos_left = 220, 520
        self.player_start_pos_right = 520, 520
        self.player_start_pos_rtop = 800, -292
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
        level_plats = [[12, 420, 210, platforms.PLAT_TYPE_01],
                       [2, 1400, 200, platforms.PLAT_TYPE_01],
                       [2, 1580, 300, platforms.PLAT_TYPE_01],
                       [2, 1420, 575, platforms.PLAT_TYPE_01],
                       [21, 1640, 460, platforms.PLAT_TYPE_01],
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

        # Add NPCs
        self.npcs.add([
            BatBlack(560, 640, self.game, border_left=500, border_right=860, change_x=2),
            ])

        # Add doors
        self.doors.add([
            DoorLeftBlue(2, 550, self.game, level_dest=9, door_dest_pos=DOOR_DEST_NL),
            DoorRightMagenta(3640, 550, self.game, level_dest=11, door_dest_pos=DOOR_DEST_NL, is_locked=True),
            ])
