"""Module cutscene level 112."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    DIRECTION_LEFT,
    DOOR_DEST_NL,
    SCREEN_NEAR_EARTH,
    )
from codemaster.models.actors.decorations import (
    Grass,
    Water,
    )
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.npcs import (
    KungFuFighterMale,
    )
from codemaster.models.actors.items import (
    platforms,
    DoorRightBlue,
    )
from codemaster.levels.level_base import Level
from codemaster.cutscenes.cutscene_112 import Cutscene112


class Level112(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(6)).convert()
        self.player_start_pos_left = 220, 408
        self.player_start_pos_right = 600, 408
        self.player_start_pos_rtop = 880, -292
        self.player_start_pos_ltop = 80, 100

        super().__init__(id_, game, name='cutscene_112', is_cutscene=True)

        # Special init attributes for this cutscene level
        self.door_previous_pos_player = self.player_start_pos_left
        self.door_previous_pos_world = self.world_start_pos_left
        self.cutscene = Cutscene112(self, game)
        self.level_to_return = None
        self.level_to_return_door = None
        self.done = False

    def clean_cutscene(self):
        self.cutscene.actor_cutscene_msg_holder = None
        for text_msg in self.game.text_msg_sprites:
            text_msg.kill_hook()
        self.level_to_return = None
        self.level_to_return_door = None
        self.game.level_cutscene = None
        if self.game.is_persist_data:
            self.game.ui_manager.ui_ingame.items['save_game_button'].enable()

    def update_pc_enter_level(self):
        self.done = False
        self.cutscene.update_pc_enter_level()

    def update(self):
        super().update()
        self.cutscene.update()

    def _add_actors_hook(self):
        # Add platforms (n_blocs, x, y, type)
        level_plats = [
            [3, 456, 586, platforms.PLAT_TYPE_01],
            [2, 660, 424, platforms.PLAT_TYPE_01],
            [6, 900, 350, platforms.PLAT_TYPE_01],
            [6, 1450, 350, platforms.PLAT_TYPE_01],
            [11, 2000, 350, platforms.PLAT_TYPE_01],
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

        # Add grass blocks
        Grass.create_grass(0, SCREEN_NEAR_EARTH , self.game, qty=28, qty_depth=2,
            actor_type=ActorType.PLAT_GRASS_U)

        # Add NPCs
        npc = KungFuFighterMale(2040, 269, self.game, change_x=0)
        self.npcs.add([
            npc,
            ])
        npc.direction = DIRECTION_LEFT

        # Add doors
        self.doors.add([
            DoorRightBlue(2900, 550, self.game, level_dest=0, door_dest_pos=DOOR_DEST_NL, is_locked=True),
            ])
