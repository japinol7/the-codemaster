"""Module cutscene level 111."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    DIRECTION_LEFT,
    SCREEN_NEAR_EARTH,
    )
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.npcs import (
    BirdGreen,
    BirdBrown,
    Kaede,
    SquirrelA,
    )
from codemaster.models.actors.decorations import (
    Grass,
    Water,
    )
from codemaster.models.actors.items import (
    platforms,
    TreeA,
    TreeB,
    SunA,
    )
from codemaster.levels.level_base import Level
from codemaster.cutscenes.cutscene_111 import Cutscene111


class Level111(Level):

    def __init__(self, id_, game):
        self.background = pg.image.load(self.file_name_im_get(2)).convert()
        self.player_start_pos_left = 220, 408
        self.player_start_pos_right = 600, 408
        self.player_start_pos_rtop = 880, -292
        self.player_start_pos_ltop = 80, 100

        super().__init__(id_, game, name='cutscene_111', is_cutscene=True)

        # Special init attributes for this cutscene level
        self.door_previous_pos_player = self.player_start_pos_left
        self.door_previous_pos_world = self.world_start_pos_left
        self.cutscene = Cutscene111(self, game)
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
            [60, 0, SCREEN_NEAR_EARTH, platforms.PLAT_TYPE_05_EARTH],
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
        Grass.create_grass(0, SCREEN_NEAR_EARTH , self.game, qty=3, qty_depth=2)
        Grass.create_grass(
            648, SCREEN_NEAR_EARTH , self.game, qty=6, qty_depth=2,
            actor_type=ActorType.PLAT_GRASS_B)
        Grass.create_grass(1944, SCREEN_NEAR_EARTH , self.game, qty=11, qty_depth=2)

        # Add item decors - item trees, flowers...
        self.item_decors.add([
            TreeB(-24, 132, self.game),
            TreeA(1220, 60, self.game),
            SunA(590, 290, self.game),
            ])

        # Add NPCs
        npc_kaede = Kaede(1440, 666, self.game, change_x=0)
        self.npcs.add([
            BirdBrown(8, 428, self.game, border_left=0, border_right=3800, change_x=1),
            BirdGreen(1490, 370, self.game, border_left=640, border_right=1500, change_x=2),
            BirdBrown(1660, 430, self.game, border_left=920, border_right=1670, change_x=1),
            BirdGreen(800, 460, self.game, border_left=700, border_right=1600, change_x=1),
            BirdBrown(2590, 470, self.game, border_left=650, border_right=2600, change_x=1.5),
            BirdGreen(2690, 376, self.game, border_left=710, border_right=2700, change_x=1),
            SquirrelA(110, 686, self.game, border_left=50, border_right=650, change_x=1),
            SquirrelA(330, 686, self.game, border_left=60, border_right=650, change_x=1),
            SquirrelA(600, 686, self.game, border_left=50, border_right=650, change_x=2),
            SquirrelA(1600, 686, self.game, border_left=1492, border_right=2100, change_x=2),
            SquirrelA(1700, 686, self.game, border_left=1500, border_right=2100, change_x=1),
            SquirrelA(1800, 686, self.game, border_left=1492, border_right=2100, change_x=1.5),
            SquirrelA(1900, 686, self.game, border_left=1500, border_right=2100, change_x=1),
            SquirrelA(2000, 686, self.game, border_left=1492, border_right=2100, change_x=1),

            npc_kaede,
            ])
        npc_kaede.direction = DIRECTION_LEFT
