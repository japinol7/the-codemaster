"""Module tutorial level 101."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    SCREEN_NEAR_EARTH,
    DOOR_DEST_NL,
    )
from codemaster.models.actors.decorations import Water
from codemaster.models.actors.items import (
    platforms,
    DoorRightBlue,
    DoorKeyBlue,
    SignMessageA,
    )
from codemaster.levels.level_base import Level
from codemaster.tutorials.tutorial_101 import Tutorial101


class Level101(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(3)).convert()
        self.player_start_pos_left = 220, 408
        self.player_start_pos_right = 600, 408
        self.player_start_pos_rtop = 880, -292
        self.player_start_pos_ltop = 80, 100

        super().__init__(id_, game, name='tutorial_101', is_tutorial=True)

        # Special init attributes for this tutorial level
        self.tutorial = Tutorial101(self, game)

    def update_pc_enter_level(self):
        self.tutorial.update_pc_enter_level()

    def update(self):
        super().update()
        self.tutorial.update()

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [
            [3, 456, 586, platforms.PLAT_TYPE_01],
            [2, 660, 424, platforms.PLAT_TYPE_01],
            [6, 900, 350, platforms.PLAT_TYPE_01],
            [6, 1450, 350, platforms.PLAT_TYPE_01],
            [10, 2000, 350, platforms.PLAT_TYPE_01],
            [56, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
            ]
        plats = []
        for platform in level_plats:
            plats += platforms.Platform.sprite_sheet_data_for_n_blocks(
                platform[0], platform[1], platform[2], platform[3])
        for platform in plats:
            block = platforms.Platform(platform[0], platform[1], platform[2], self.game)
            self.platforms.add(block)

        # Add water blocks
        Water.create_water(0, SCREEN_NEAR_EARTH + 216, self.game, qty=20, qty_depth=3)

        # Add sign messages
        self.sign_messages.add([
            SignMessageA(3300, 450, self.game)
            ])

        # Add doors
        self.doors.add([
            DoorRightBlue(3400, 550, self.game, level_dest=0, door_dest_pos=DOOR_DEST_NL, is_locked=True),
            ])

        # Add door keys
        self.door_keys.add([
            DoorKeyBlue(3720, 700, self.game, door=[door for door in self.doors if door.is_locked][0]),
            ])