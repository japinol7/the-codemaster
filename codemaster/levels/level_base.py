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


class Level:
    """Represents a base level.
    It is not intended to be instantiated.
    """
    SCROLL_LV_NEAR_RIGHT_SIDE = 150
    world_shift = 0
    world_shift_top = -500

    def __init__(self, game):
        self.id = None
        self.game = game
        self.player = game.player
        self.completed = False
        self.start_time = None
        self.door_previous_position = DOOR_POSITION_L
        self.door_previous_pos_player = 80, 480
        self.door_previous_pos_world = 0, -758
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.decors = pg.sprite.Group()
        self.clocks = pg.sprite.Group()
        self.batteries = pg.sprite.Group()
        self.files_disks = pg.sprite.Group()
        self.computers = pg.sprite.Group()
        self.npcs = pg.sprite.Group()
        self.npcs_moving_y = pg.sprite.Group()  # Used to update y-axis border limits for vertical moving NPCs
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

        self.game.level = self

    def start_up(self):
        self.start_time = self.game.current_time

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

    def add_actors(self, actors):
        snake_pieces = []
        dragon_pieces = []
        for actor in actors:
            if isinstance(actor, MovingActor):
                if actor.border_left:
                    actor.border_left -= self.world_shift
                if actor.border_right:
                    actor.border_right -= self.world_shift

            self.game.is_log_debug and log.debug(f"Add actor {actor.category_type} to level {self}")
            if actor.category_type == ActorCategoryType.NPC:
                self.npcs.add(actor)
            elif actor.category_type == ActorCategoryType.BATTERY:
                self.batteries.add(actor)
            elif actor.category_type == ActorCategoryType.FILES_DISK:
                self.files_disks.add(actor)
            elif actor.category_type == ActorCategoryType.COMPUTER:
                self.computers.add(actor)
                self.normal_items.add(actor)
            elif actor.category_type == ActorCategoryType.APPLE:
                self.apples.add(actor)
            elif actor.category_type == ActorCategoryType.CARTRIDGE:
                self.cartridges.add(actor)
            elif actor.category_type == ActorCategoryType.POTION:
                self.potions.add(actor)
            elif actor.category_type == ActorCategoryType.MINE:
                self.mines.add(actor)
            elif actor.category_type == ActorCategoryType.LIFE_RECOVERY:
                self.life_recs.add(actor)
            elif actor.category_type == ActorCategoryType.DOOR_KEY:
                self.door_keys.add(actor)
            elif actor.category_type == ActorCategoryType.DOOR:
                self.doors.add(actor)
            elif actor.category_type == ActorCategoryType.EXPLOSION:
                self.explosions.add(actor)
            elif actor.category_type == ActorCategoryType.CLOCK:
                self.clocks.add(actor)
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

    @staticmethod
    def factory(levels_module, game):
        return [getattr(levels_module, f"Level{level_id}")(game)
                for level_id in range(1, N_LEVELS + 1)]

    @staticmethod
    def factory_by_nums(levels_module, game, level_name_nums=None, level_name_prefix='Level'):
        return [getattr(levels_module, f"{level_name_prefix}{level_id}")(game)
                for level_id in level_name_nums]

    @staticmethod
    def file_name_im_get(id_):
        return path.join(BM_BACKGROUNDS_FOLDER,
                         f"{FILE_NAMES['im_backgrounds'][0]}_{id_:02d}."
                         f"{FILE_NAMES['im_backgrounds'][1]}")

    @staticmethod
    def levels_completed(game):
        return [(x.id, x.name) for x in game.levels if x.completed]

    @staticmethod
    def clean_entity_ids():
        clean_entity_ids()
