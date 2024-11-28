"""Module base level."""
__author__ = 'Joan A. Pinol  (japinol)'

from collections import Counter
from os import path

import pygame as pg

from codemaster.config.constants import (
    FILE_NAMES, BM_BACKGROUNDS_FOLDER,
    DOOR_POSITION_L, N_LEVELS,
    )
from codemaster.tools.logger.logger import log
from codemaster.models.actors.actor_types import ActorBaseType, ActorCategoryType
from codemaster.clean_new_game import clean_entity_ids
from codemaster.models.actors.actors import MovingActor

LEVEL_SIZE_LIMIT_DEFAULT = -3000
LEVEL_SIZE_LIMIT_TOP_DEFAULT = -1000
LEVEL_WORLD_START_POS_LEFT = 0, -758


class LevelException(Exception):
    pass


class Level:
    """Represents a base level.
    It is not intended to be instantiated.
    """
    SCROLL_LV_NEAR_RIGHT_SIDE = 150

    def __init__(self, id_, game):
        self.id = id_
        self.name = str(self.id)
        self.game = game
        self.game.level_init = self
        self.player = game.player
        self.completed = False
        self.start_time = None
        self.world_shift_initial = 0
        self.world_shift_top_initial = -500
        self.world_shift = self.world_shift_initial
        self.world_shift_top = self.world_shift_top_initial
        self.door_previous_position = DOOR_POSITION_L
        self.door_previous_pos_player = 80, 480
        self.door_previous_pos_world = 0, -758
        self.previous_door_crossed = None
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.decors = pg.sprite.Group()
        self.clocks = pg.sprite.Group()
        self.batteries = pg.sprite.Group()
        self.files_disks = pg.sprite.Group()
        self.computers = pg.sprite.Group()
        self.npcs = pg.sprite.Group()
        self.apples = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.cartridges = pg.sprite.Group()
        self.potions = pg.sprite.Group()
        self.mines = pg.sprite.Group()
        self.life_recs = pg.sprite.Group()
        self.door_keys = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.normal_items = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.explosions = pg.sprite.Group()
        self.magic_sprites = pg.sprite.Group()
        self.particle_tuple_sprites = pg.sprite.Group()
        self.particle_sprites = pg.sprite.Group()
        self.snakes = pg.sprite.Group()
        self.snakes_body_pieces = pg.sprite.Group()
        self.dragons = pg.sprite.Group()
        self.dragons_body_pieces = pg.sprite.Group()

        self.spells_on_level_count = Counter()
        # Used to update y-axis border limits for vertical moving NPCs
        self.npcs_moving_y = pg.sprite.Group()

        self.game.level = self

        if not getattr(self, 'level_limit', None):
            self.level_limit = LEVEL_SIZE_LIMIT_DEFAULT

        if not getattr(self, 'level_limit_top', None):
            self.level_limit_top = LEVEL_SIZE_LIMIT_TOP_DEFAULT

        if not getattr(self, 'background', None):
            raise LevelException(f"Level {self.id} does not set attribute: background")

        if not getattr(self, 'player_start_pos_left', None):
            raise LevelException(f"Level {self.id} does not set attribute: player_start_pos_left")

        if not getattr(self, 'player_start_pos_right', None):
            raise LevelException(f"Level {self.id} does not set attribute: player_start_pos_right")

        if not getattr(self, 'player_start_pos_rtop', None):
            raise LevelException(f"Level {self.id} does not set attribute: player_start_pos_rtop")

        if not getattr(self, 'player_start_pos_ltop', None):
            raise LevelException(f"Level {self.id} does not set attribute: player_start_pos_ltop")

        if not getattr(self, 'world_start_pos_left', None):
            self.world_start_pos_left = LEVEL_WORLD_START_POS_LEFT

        self.world_start_pos_right = self.level_limit + self.SCROLL_LV_NEAR_RIGHT_SIDE, -758
        self.world_start_pos_rtop = self.level_limit + 500 + self.SCROLL_LV_NEAR_RIGHT_SIDE, -900
        self.world_start_pos_ltop = 0, -900

        self._add_actors()

    def start_up(self):
        self.start_time = self.game.current_time

    def _add_actors(self):
        self._add_actors_hook()
        self._sprites_all_add()

    def _add_actors_hook(self):
        pass

    def _sprites_all_add(self):
        for sprite in self.platforms:
            self.all_sprites.add(sprite)
            self.normal_items.add(sprite)
        for sprite in self.decors:
            self.all_sprites.add(sprite)
        for sprite in self.computers:
            self.all_sprites.add(sprite)
            self.normal_items.add(sprite)
            self.items.add(sprite)
        for sprite in self.doors:
            self.all_sprites.add(sprite)
        for sprite in self.clocks:
            self.all_sprites.add(sprite)
            self.items.add(sprite)
        for sprite in self.batteries:
            self.all_sprites.add(sprite)
            self.items.add(sprite)
        for sprite in self.files_disks:
            self.all_sprites.add(sprite)
            self.items.add(sprite)
        for sprite in self.cartridges:
            self.all_sprites.add(sprite)
            self.items.add(sprite)
        for sprite in self.potions:
            self.all_sprites.add(sprite)
            self.items.add(sprite)
        for sprite in self.life_recs:
            self.all_sprites.add(sprite)
            self.items.add(sprite)
        for sprite in self.door_keys:
            self.all_sprites.add(sprite)
            self.items.add(sprite)
        for sprite in self.apples:
            self.all_sprites.add(sprite)
            self.items.add(sprite)
        for sprite in self.mines:
            self.all_sprites.add(sprite)
            self.items.add(sprite)
        for sprite in self.dragons:
            self.npcs.add(sprite)
            for dragon_piece in sprite.body_pieces:
                self.dragons_body_pieces.add(dragon_piece)
                self.all_sprites.add(dragon_piece)
        for sprite in self.npcs:
            self.all_sprites.add(sprite)
            if sprite.border_top or sprite.border_down:
                self.npcs_moving_y.add(sprite)
        for sprite in self.snakes:
            self.npcs.add(sprite)
            self.all_sprites.add(sprite)
            for snake_piece in sprite.body_pieces:
                self.snakes_body_pieces.add(snake_piece)
                self.all_sprites.add(snake_piece)
        for sprite in self.explosions:
            self.all_sprites.add(sprite)
        for sprite in self.bullets:
            self.all_sprites.add(sprite)

    def update(self):
        self.all_sprites.update()
        self.magic_sprites.update()

    def draw(self):
        self.game.screen.blit(self.background, (self.world_shift // 3, self.world_shift_top))
        self.all_sprites.draw(self.game.screen)
        for actor in self.npcs:
            base_type = getattr(actor, 'base_type', None)
            if base_type and base_type.name == ActorBaseType.NPC.name:
                actor.draw_health()

    def shift_world(self, shift_x):
        self.world_shift += shift_x
        for sprite in self.all_sprites:
            sprite.rect.x += shift_x

        for sprite in self.game.text_msg_sprites:
            sprite.rect.x += shift_x
        for sprite in self.magic_sprites:
            sprite.rect.x += shift_x

        for sprite in self.particle_tuple_sprites:
            for particle in sprite.particles.values():
                particle[0][0] += shift_x

        for sprite in self.particle_sprites:
            for particle in sprite.particles:
                particle.position[0] += shift_x

    def shift_world_top(self, shift_y):
        self.world_shift_top += shift_y
        for sprite in self.all_sprites:
            sprite.rect.y += shift_y

        # Update border limits for moving NPCs
        for npc_moving_y in self.npcs_moving_y:
            npc_moving_y.border_top += shift_y
            npc_moving_y.border_down += shift_y

        for sprite in self.game.text_msg_sprites:
            sprite.rect.y += shift_y
        for sprite in self.magic_sprites:
            sprite.rect.y += shift_y

        for sprite in self.particle_tuple_sprites:
            for particle in sprite.particles.values():
                particle[0][1] += shift_y

        for sprite in self.particle_sprites:
            for particle in sprite.particles:
                particle.position[1] += shift_y

    def update_pc_enter_level(self):
        self.player.stats['levels_visited'].add(self.id)

    def add_actors(self, actors, shift_borders=True):
        snake_pieces = []
        dragon_pieces = []
        for actor in actors:
            actor.is_not_initial_actor = True
            if shift_borders and isinstance(actor, MovingActor):
                if actor.border_left:
                    actor.border_left -= self.world_shift
                if actor.border_right:
                    actor.border_right -= self.world_shift

            self.game.is_log_debug and log.debug(f"Add actor {actor.id} to level {self.id}")
            if actor.category_type == ActorCategoryType.NPC:
                self.npcs.add(actor)
            elif actor.category_type == ActorCategoryType.BATTERY:
                self.batteries.add(actor)
                self.items.add(actor)
            elif actor.category_type == ActorCategoryType.FILES_DISK:
                self.files_disks.add(actor)
                self.items.add(actor)
            elif actor.category_type == ActorCategoryType.COMPUTER:
                self.computers.add(actor)
                self.normal_items.add(actor)
                self.items.add(actor)
            elif actor.category_type == ActorCategoryType.APPLE:
                self.apples.add(actor)
                self.items.add(actor)
            elif actor.category_type == ActorCategoryType.CARTRIDGE:
                self.cartridges.add(actor)
                self.items.add(actor)
            elif actor.category_type == ActorCategoryType.POTION:
                self.potions.add(actor)
                self.items.add(actor)
            elif actor.category_type == ActorCategoryType.MINE:
                self.mines.add(actor)
                self.items.add(actor)
            elif actor.category_type == ActorCategoryType.LIFE_RECOVERY:
                self.life_recs.add(actor)
                self.items.add(actor)
            elif actor.category_type == ActorCategoryType.DOOR_KEY:
                self.door_keys.add(actor)
                self.items.add(actor)
            elif actor.category_type == ActorCategoryType.DOOR:
                self.doors.add(actor)
            elif actor.category_type == ActorCategoryType.EXPLOSION:
                self.explosions.add(actor)
            elif actor.category_type == ActorCategoryType.CLOCK:
                self.clocks.add(actor)
                self.items.add(actor)
            elif actor.category_type == ActorCategoryType.SNAKE:
                self.npcs.add(actor)
                self.snakes.add(actor)
                for snake_piece in actor.body_pieces:
                    self.snakes_body_pieces.add(snake_piece)
                    snake_pieces.append(snake_piece)
            elif actor.category_type == ActorCategoryType.DRAGON:
                self.npcs.add(actor)
                self.dragons.add(actor)
                for dragon_piece in actor.body_pieces:
                    self.dragons_body_pieces.add(dragon_piece)
                    dragon_pieces.append(dragon_piece)

        self.all_sprites.add(actors)
        snake_pieces and self.all_sprites.add(snake_pieces)
        dragon_pieces and self.all_sprites.add(dragon_pieces)

    def get_npcs_filtered_by_actor_type(self, actor_type):
        return [actor for actor in self.npcs if actor.type == actor_type]

    def get_npc_by_id(self, actor_id):
        return [actor for actor in self.npcs if actor.id == actor_id][0]

    def count_npcs_filtered_by_actor_type(self, actor_type):
        return sum(1 for actor in self.npcs if actor.type == actor_type)

    def get_items_filtered_by_actor_type(self, actor_type):
        return [actor for actor in self.items if actor.type == actor_type]

    def count_items_filtered_by_actor_type(self, actor_type):
        return sum(1 for actor in self.items if actor.type == actor_type)

    def get_actors_in_group_filtered_by_actor_type(self, actor_type, actor_group):
        return [actor for actor in actor_group if actor.type == actor_type]

    def count_actors_in_group_filtered_by_actor_type(self, actor_type, actor_group):
        return sum(1 for actor in actor_group if actor.type == actor_type)

    def get_scroll_shift_delta(self):
        return abs(self.world_shift) - self.world_shift_initial

    def get_scroll_shift_top_delta(self):
        return self.world_shift_top - self.world_shift_top_initial

    @staticmethod
    def get_scroll_shift_delta_from_params(world_shift, world_shift_initial):
        return abs(world_shift) - world_shift_initial

    @staticmethod
    def get_scroll_shift_top_delta_from_params(world_shift_top, world_shift_top_initial):
        return world_shift_top - world_shift_top_initial

    @staticmethod
    def get_scroll_shift_delta_tuple(game_level, level_data):
        return (
            game_level.get_scroll_shift_delta_from_params(
                level_data['world_shift'], level_data['world_shift_initial']),
            game_level.get_scroll_shift_top_delta_from_params(
                level_data['world_shift_top'], level_data['world_shift_top_initial']),
            )

    @staticmethod
    def factory(levels_module, game):
        return [getattr(levels_module, f"Level{level_id}")(level_id, game)
                for level_id in range(1, N_LEVELS + 1)]

    @staticmethod
    def factory_by_nums(levels_module, game, level_ids=None, level_name_prefix='Level'):
        return [getattr(levels_module, f"{level_name_prefix}{level_id}")(level_id, game)
                for level_id in level_ids]

    @staticmethod
    def file_name_im_get(id_):
        return path.join(BM_BACKGROUNDS_FOLDER,
                         f"{FILE_NAMES['im_backgrounds'][0]}_{id_:02d}."
                         f"{FILE_NAMES['im_backgrounds'][1]}")

    @staticmethod
    def levels_completed_ids(game):
        return [x.id for x in game.levels if x.completed]

    @staticmethod
    def levels_completed_names(game):
        return [x.name for x in game.levels if x.completed]

    @staticmethod
    def levels_completed_count(game):
        return sum(1 for x in game.levels if x.completed)

    @staticmethod
    def clean_entity_ids():
        clean_entity_ids()
