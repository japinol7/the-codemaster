"""Module actors."""
__author__ = 'Joan A. Pinol  (japinol)'

from collections import Counter, OrderedDict
from itertools import chain
from os import path
from random import randint

import pygame as pg

from codemaster.config.settings import Settings
from codemaster.config.constants import (
    FILE_NAMES,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
    ACTOR_TIME_BETWEEN_ENERGY_SHIELD_CASTING_DEFAULT,
    )
from codemaster.models.experience_points import ExperiencePoints
from codemaster.models.actors.actor_types import (
    ActorBaseType,
    ActorCategoryType,
    ActorType
    )
from codemaster.tools.utils import utils_graphics as libg_jp
from codemaster.tools.utils.colors import Color
from codemaster.persistence.persistence_utils import is_json_serializable
from codemaster.models.actors.items import bullets
from codemaster.models.actors.items.bullets import Bullet, BulletType
from codemaster.tools.logger.logger import log

NPC_STD_WIDTH = 61
NPC_STD_HEIGHT = 61
NPC_STRENGTH_BASE = 35


class DropItem:

    def __init__(self, actor_class, probability_to_drop=100,
                 x_delta=0, y_delta=0, **kwargs):
        self.class_ = actor_class
        self.probability_to_drop = probability_to_drop
        self.x_delta = x_delta
        self.y_delta = y_delta
        self.args = kwargs


class Actor(pg.sprite.Sprite):
    """Represents an actor.
    It is not intended to be instantiated.
    """
    type_id_count = Counter()
    # key: sprite_sheet_data_id, value: (image, walking_frames_l, walking_frames_r)
    sprite_images = {}
    actors = {}

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0, items_to_drop=None):
        super().__init__()

        if not getattr(self, 'type', None):
            self.type = ActorType.NONE

        Actor.type_id_count[self.type] += 1
        self.id = f"{self.type.name}_{Actor.type_id_count[self.type]:05d}"
        self.game = game
        self.player = game.player
        self.last_shot_time = 0
        self.time_between_shots_base = 1200
        self.last_spell_casted_time = 0
        self.energy_shield_casted_time = 0
        self.time_between_spell_casting_base = 7200
        self.time_between_energy_shield_casting_base = ACTOR_TIME_BETWEEN_ENERGY_SHIELD_CASTING_DEFAULT
        self.target_of_spells_count = Counter()

        if not getattr(self, 'base_type', None):
            self.base_type = ActorBaseType.NONE

        if self.base_type.name in (ActorBaseType.ITEM.name, ActorBaseType.NPC.name):
            Actor.actors[self.id] = self

        if not getattr(self, 'category_type', None):
            self.category_type = ActorCategoryType.NONE

        if not getattr(self, 'file_folder', None):
            self.file_folder = None
        if not getattr(self, 'file_mid_prefix', None):
            self.file_mid_prefix = None
        if not getattr(self, 'file_prefix', None):
            self.file_prefix = None
        if not getattr(self, 'file_name_key', None):
            self.file_name_key = None

        if not getattr(self, 'location_in_inventory', None):
            self.is_location_in_inventory = False

        if not getattr(self, 'images_sprite_no', None):
            self.images_sprite_no = 1
        if not getattr(self, 'animation_speed', None):
            self.animation_speed = 0.1
        if not getattr(self, 'frame_index', None):
            self.frame_index = 0

        if not getattr(self, 'owner', None):
            self.owner = None

        if not getattr(self, 'is_pc', None):
            self.is_pc = False
            self.is_a_player = False
        if not getattr(self, 'is_npc', None):
            self.is_npc = False
        if not getattr(self, 'can_move', None):
            self.can_move = False
        if not getattr(self, 'is_item', None):
            self.is_item = False
        if not getattr(self, 'is_a_snake', None):
            self.is_a_snake = False
        if not getattr(self, 'is_a_dragon', None):
            self.is_a_dragon = False

        if not getattr(self, 'is_not_initial_actor', None):
            self.is_not_initial_actor = False

        if not getattr(self, 'cannot_be_copied', None):
            self.cannot_be_copied = False

        if getattr(self, 'can_be_killed_normally', None) is None:
            self.can_be_killed_normally = True

        if not getattr(self, 'stats', None):
            self.stats = None

        if not getattr(self, 'transparency_alpha', None):
            self.transparency_alpha = False

        self.items_to_drop = items_to_drop or []
        if not getattr(self, 'can_drop_items', None):
            self.can_drop_items = True if self.items_to_drop else False

        if not getattr(self, 'hostility_level', None):
            self.hostility_level = 1

        if not getattr(self, 'can_shot', None):
            self.can_shot = False

        if not getattr(self, 'can_cast_spells', None):
            self.can_cast_spells = False

        if not getattr(self, 'is_magic_item', None):
            self.is_magic_item = False

        if not getattr(self, 'shot_x_delta_max', None):
            self.shot_x_delta_max = 500

        if not getattr(self, 'shot_y_delta', None):
            self.shot_y_delta = 75

        if not getattr(self, 'spell_cast_x_delta_max', None):
            self.spell_cast_x_delta_max = 500

        if not getattr(self, 'spell_cast_y_delta_max', None):
            self.spell_cast_y_delta_max = 500

        if not getattr(self, 'change_x', None):
            self.change_x = change_x

        if not getattr(self, 'change_y', None):
            self.change_y = change_y

        if not getattr(self, 'direction', None):
            self.direction = DIRECTION_RIGHT

        if not getattr(self, 'color', None):
            self.color = None

        if not getattr(self, 'spell_cast_y_delta_max', None):
            self.spell_cast_y_delta_max = 500

        if not getattr(self, 'health_bar_delta_y', None):
            self.health_bar_delta_y = 0

        if self.stats is not None:
            if not getattr(self.stats, 'power_recovery', None):
                self.stats.power_recovery = 0
            if not getattr(self.stats, 'energy_shield', None):
                self.stats.energy_shield = None
            if not getattr(self.stats, 'time_between_energy_shield_casting', None):
                self.stats.time_between_energy_shield_casting = 0
            if not getattr(self.stats, 'energy_shield_pos_delta_x', None):
                self.stats.energy_shield_pos_delta_x = 0
            if not getattr(self.stats, 'energy_shield_pos_delta_y', None):
                self.stats.energy_shield_pos_delta_y = 0

        if not getattr(self, 'npc_summoned_count', None):
            self.npc_summoned_count = 0

        self.can_be_shot_by_its_owner = True
        self.name = name or 'unnamed'

        self.init_before_load_sprites_hook()
        self._load_sprites()

        if not self.image:
            log.warning("Actor image missing: %s", self.id)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.init_after_load_sprites_hook()

    def _load_sprites(self):
        if not Actor.sprite_images.get(self.type.name):
            walking_frames_l = []
            walking_frames_r = []
            image = None
            for i in range(self.images_sprite_no):
                if self.transparency_alpha:
                    image = pg.image.load(self.file_name_im_get(
                                self.file_folder, self.file_name_key,
                                self.file_mid_prefix, suffix_index=i+1
                                )).convert_alpha()
                else:
                    image = pg.image.load(self.file_name_im_get(
                        self.file_folder, self.file_name_key,
                        self.file_mid_prefix, suffix_index=i + 1
                    )).convert()
                    image.set_colorkey(Color.BLACK)
                walking_frames_r.append(image)
            for i in range(self.images_sprite_no):
                if self.transparency_alpha:
                    image = pg.image.load(self.file_name_im_get(
                                self.file_folder, self.file_name_key,
                                self.file_mid_prefix, suffix_index=i+1
                                )).convert_alpha()
                else:
                    image = pg.image.load(self.file_name_im_get(
                        self.file_folder, self.file_name_key,
                        self.file_mid_prefix, suffix_index=i + 1
                    )).convert()
                    image.set_colorkey(Color.BLACK)
                walking_frames_r.append(image)
                if self.can_move:
                    image = pg.transform.flip(image, True, False)
                walking_frames_l.append(image)
            Actor.sprite_images[self.type.name] = (image, walking_frames_l, walking_frames_r)
            self.image = walking_frames_r[0]
        else:
            self.image = Actor.sprite_images[self.type.name][0]

    def init_before_load_sprites_hook(self):
        pass

    def init_after_load_sprites_hook(self):
        pass

    @property
    def power(self):
        return self.stats.power

    @power.setter
    def power(self, value):
        self.stats.power = value

    @property
    def health(self):
        return self.stats.health

    @health.setter
    def health(self, value):
        self.stats.health = value

    @property
    def magic_resistance(self):
        return self.stats.magic_resistance

    @magic_resistance.setter
    def magic_resistance(self, value):
        self.stats.magic_resistance = value

    def update(self):
        self.frame_index += self.animation_speed
        self.update_after_inc_index_hook()
        if self.frame_index >= self.images_sprite_no:
            self.frame_index = 0

        if self.hostility_level > 0 and self.can_shot:
            is_between_y_boundaries = (self.player.rect.y - self.shot_y_delta < self.rect.y
                                       < self.player.rect.y + self.shot_y_delta)
            shot_x_delta = abs(self.rect.x - self.player.rect.x)
            if (self.direction == DIRECTION_LEFT and shot_x_delta < self.shot_x_delta_max
                    and self.player.rect.x <= self.rect.x
                    and is_between_y_boundaries):
                self.update_shot_bullet()
            elif (self.direction == DIRECTION_RIGHT and shot_x_delta < self.shot_x_delta_max
                    and self.player.rect.x >= self.rect.x
                    and is_between_y_boundaries):
                self.update_shot_bullet()

        if self.hostility_level > 0 and self.can_cast_spells:
            is_between_x_boundaries = (self.player.rect.x - self.spell_cast_x_delta_max < self.rect.x
                                       < self.player.rect.x + self.spell_cast_x_delta_max)
            is_between_y_boundaries = (self.player.rect.y - self.spell_cast_y_delta_max < self.rect.y
                                       < self.player.rect.y + self.spell_cast_y_delta_max)
            if is_between_x_boundaries and is_between_y_boundaries:
                self.update_cast_spell()

        self.update_energy_shield()

        if self.power is None or self.power < 0:
            self.power = 0

        self.update_sprite_image()
        self.update_when_hit()

    def update_sprite_image(self):
        self.image = Actor.sprite_images[self.type.name][self.direction][int(self.frame_index)]

    def update_after_inc_index_hook(self):
        pass

    def update_when_hit(self):
        bullet_hit_list = pg.sprite.spritecollide(self, self.game.level.bullets, False)
        if not bullet_hit_list:
            return

        has_been_hit = False
        for bullet in bullet_hit_list:
            if self.base_type.name == bullet.owner.base_type.name:
                # Actors of the same base type do not shoot each other
                continue
            if not self.can_be_shot_by_its_owner and self.owner == bullet.owner:
                continue
            self.game.is_log_debug and log.debug(
                f"{self.id} hit by {bullet.id}, health: {str(round(self.stats.health, 2))}, "
                f"bullet_power: {str(bullet.attack_power)}")
            self.stats.health -= bullet.attack_power
            has_been_hit = True
            bullet.kill()
            if bullet.owner == self.player and self.hostility_level < 1:
                self.hostility_level = 1
                if self.stats.energy_shield and not self.stats.energy_shield.is_activated:
                    self.stats.energy_shield.activate()

        has_been_hit and self.player.sound_effects and self.player.enemy_hit_sound.play()
        if self.stats.health <= 0:
            self.game.is_log_debug and log.debug(f"{self.id}, !!! Dead by bullet {bullet.id} !!!")
            self.player.sound_effects and self.player.npc_killed_sound.play()
            if bullet.is_a_player_shot:
                self.player.stats['score'] += ExperiencePoints.xp_points[self.type.name]
            self.explosion()
            self.drop_items()
            self.kill_hook()

    def kill(self):
        if Actor.actors.get(self.id):
            del Actor.actors[self.id]
        super().kill()

    def kill_hook(self):
        if self.stats.energy_shield:
            self.stats.energy_shield.kill()
        self.kill()

    def update_shot_bullet(self):
        time_delta = self.game.current_time - self.last_shot_time
        if time_delta > self.stats.time_between_shots:
            self.last_shot_time = self.game.current_time
            self.update_shot_bullet_fire_shots()

    def update_shot_bullet_fire_shots(self):
        if randint(1, 100) + 60 >= 100:
            self.shot_bullet(BulletType.T1_LASER1)
        else:
            self.shot_bullet(BulletType.T2_LASER2)

    def update_energy_shield(self):
        time_delta = self.game.current_time - self.energy_shield_casted_time
        if time_delta > self.stats.time_between_energy_shield_casting:
            self.energy_shield_casted_time = self.game.current_time
            self.update_energy_shield_hook(self)

    def update_energy_shield_hook(self, actor):
        """Should be redefined on the EnergyShield class"""
        pass

    def update_cast_spell(self):
        time_delta = self.game.current_time - self.last_spell_casted_time
        if time_delta > self.stats.time_between_spell_casting:
            self.last_spell_casted_time = self.game.current_time
            self.update_cast_spell_cast_actions()

    def update_cast_spell_cast_actions(self):
        pass

    def draw_health(self):
        if self.stats.health < self.stats.health_total - 1:
            libg_jp.draw_bar_graphic(
                self.game.screen,
                amount_pct=self.stats.health / self.stats.health_total,
                x=self.rect.x + (self.rect.width // 2) - Settings.sprite_health_bar_pos_rel.x,
                y=self.rect.y - Settings.sprite_health_bar_pos_rel.y - self.health_bar_delta_y,
                bar_width=Settings.sprite_health_bar_size.w,
                bar_height=Settings.sprite_health_bar_size.h)

    def shot_bullet(self, bullet_type):
        Bullet.shot(bullet_type=bullet_type, change_x=bullets.BULLET_STD_VELOCITY,
                    change_y=0, owner=self, game=self.game)

    def explosion(self):
        pass

    def drop_items(self):
        if not self.can_drop_items:
            return

        for item in self.items_to_drop:
            lucky_drop = randint(1, 100)
            self.game.is_log_debug and log.debug(
                f"{self.id}, lucky_drop_dice: {str(lucky_drop)}, "
                f"probability_to_drop: {item.probability_to_drop:3d}, "
                f"item type: {item.class_.__name__}")
            if lucky_drop + item.probability_to_drop >= 100:
                self.game.is_log_debug and log.debug("Create item to drop")
                new_item = item.class_(
                    x=self.rect.x + item.x_delta,
                    y=self.rect.y + item.y_delta,
                    game=self.game,
                    **item.args)
                self.game.level.add_actors([new_item], shift_borders=False)
                self.game.is_log_debug and log.debug(f"Dropped: {new_item.id}")

    def is_actor_on_the_left(self, actor):
        if actor.rect.x <= self.rect.x:
            return True
        return False

    def is_actor_on_the_right(self, actor):
        if actor.rect.x > self.rect.x:
            return True
        return False

    def is_actor_on_top(self, actor):
        if actor.rect.y <= self.rect.y:
            return True
        return False

    def is_actor_on_bottom(self, actor):
        if actor.rect.y > self.rect.y:
            return True
        return False

    def is_actor_on_the_left_top(self, actor):
        if self.is_actor_on_the_left(actor) and self.is_actor_on_top(actor):
            return True
        return False

    def is_actor_on_the_left_bottom(self, actor):
        if self.is_actor_on_the_left(actor) and self.is_actor_on_bottom(actor):
            return True
        return False

    def is_actor_centered_on_y(self, actor, epsilon=0):
        if self.rect.centery - epsilon <= actor.rect.centery <= self.rect.centery + epsilon:
            return True
        return False

    def recover_power(self):
        if self.is_a_player:
            return

        self.stats.power += self.stats.power_recovery
        if self.stats.power > self.stats.power_total:
            self.stats.power = self.stats.power_total

    @staticmethod
    def copy_actor(
            actor_id, game, delta_x=0, delta_y=0,
            reverse_direction=False, same_borders=False, **kwargs):
        actor = Actor.actors[actor_id]
        args = {
            'x': actor.rect.x + delta_x,
            'y': actor.rect.y + delta_y,
            'game':game,
            }

        if isinstance(actor, MovingActor):
            change_x, change_y = 0, 0
            border_delta_x, border_delta_y = 0, 0
            if actor.change_x:
                change_x = actor.change_x * (-1 if reverse_direction else 1)
                if not same_borders:
                    border_delta_x = delta_x
            if actor.change_y:
                change_y = actor.change_y * (-1 if reverse_direction else 1)
                if not same_borders:
                    border_delta_y = delta_y
            scroll_shift_delta = game.level.get_scroll_shift_delta()
            args.update({
                'border_left': actor.border_left - scroll_shift_delta + border_delta_x,
                'border_right': actor.border_right - scroll_shift_delta + border_delta_x,
                'border_top': actor.border_top + border_delta_y,
                'border_down': actor.border_down + border_delta_y,
                'change_x': change_x,
                'change_y': change_y,
                })

        args.update(**kwargs)
        new_actor = actor.__class__(**args)

        new_actor.direction = actor.direction
        new_actor.hostility_level = actor.hostility_level
        new_actor.npc_summoned_count = actor.npc_summoned_count
        new_actor.health = actor.stats.health_total
        new_actor.power = actor.stats.power_total

        if actor.stats.energy_shield:
            actor.stats.energy_shield.__class__.actor_acquire_energy_shield(
                new_actor, game,
                health_total=actor.stats.energy_shield.stats.health_total)
            new_actor.stats.time_between_energy_shield_casting = \
                actor.stats.time_between_energy_shield_casting

        if new_actor.category_type == ActorCategoryType.FILES_DISK:
            new_actor.set_random_msg()

        game.level.add_actors([new_actor])
        return new_actor

    @staticmethod
    def copy_actor_mult(actor_id, game, qty, delta_x=0, delta_y=0,
                        reverse_direction=False, **kwargs):
        new_actors = []
        dx, dy = delta_x, delta_y
        for _ in range(qty):
            new_actors.append(Actor.copy_actor(
                actor_id=actor_id, game=game, delta_x=dx, delta_y=dy,
                reverse_direction=reverse_direction,
                **kwargs))
            dx += delta_x
            dy += delta_y
        return new_actors

    @staticmethod
    def get_actor(actor_id):
        return Actor.actors[actor_id]

    @staticmethod
    def get_actor_if_exists(actor_id):
        return Actor.actors.get(actor_id)

    @staticmethod
    def get_actors_by_ids(actor_ids):
        return [Actor.actors[k] for k in actor_ids]

    @staticmethod
    def get_actors_by_ids_if_exist(actor_ids):
        return [Actor.actors[k] for k in actor_ids if Actor.actors.get(k)]

    @staticmethod
    def factory(actors_module, type_name, x, y, game, kwargs):
        return getattr(actors_module, type_name)(x, y, game, **kwargs)

    @staticmethod
    def file_name_im_get(folder, file_name_key, mid_prefix, suffix_index):
        return path.join(folder, f"{FILE_NAMES[file_name_key][0]}"
                         f"{'_' if mid_prefix else ''}"
                         f"{mid_prefix or ''}"
                         f"_{suffix_index:02d}.{FILE_NAMES[file_name_key][1]}")


class ActorItem(Actor):
    """Represents an item actor.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        if not getattr(self, 'base_type', None):
            self.base_type = ActorBaseType.ITEM

        super().__init__(x, y, game, name=name)

    def draw_health(self):
        pass

    @staticmethod
    def get_all_item_ids_basic_info(game, sorted_by_level=True):
        """Returns an ordered dictionary with the item id and the level where you can find them.
          Example:
              OrderedDict({
              'BATTERY_A_00001': ('level: 1', '1'),
              'BATTERY_A_00002': ('level: 1', '1'),
              })
        """
        res = {}
        for level in game.levels:
            for item in level.items:
                res[item.id] = f"level: {level.name:4}", f"{level.id:3d}"

        if sorted_by_level:
            return OrderedDict(sorted([x for x in res.items()], key=lambda x: (x[1][1], x[0])))
        return OrderedDict(sorted([x for x in res.items()]))

    @staticmethod
    def get_all_item_ids_basic_info_from_level(level):
        """Returns an ordered dictionary with the item id of all items in the level.
          Example:
              OrderedDict({
              'BATTERY_A_00001': ('level: 1', '1'),
              'BATTERY_A_00002': ('level: 1', '1')
              })
        """
        res = {}
        for item in level.items:
            res[item.id] = f"level: {level.name:4}", f"{level.id:3d}"

        return OrderedDict(sorted([x for x in res.items()]))

    @staticmethod
    def get_items_stats_to_persist(game):
        """Returns a dictionary with all the items' stats to persist."""
        res = {'game_levels': {}}
        levels = res['game_levels']
        for game_level_id in sorted(list(game.player.stats['levels_visited'])):
            level = game.levels[game_level_id - 1]
            levels[game_level_id] = {
                'world_shift': level.world_shift,
                'world_shift_initial': level.world_shift_initial,
                'world_shift_top': level.world_shift_top,
                'world_shift_top_initial': level.world_shift_top_initial,
                'items': {},
                }
            for item in chain(level.items, level.doors):
                if item.is_not_initial_actor:
                    continue

                if item.category_type == ActorCategoryType.DOOR:
                    levels[level.id]['items'][item.id] = {
                        'category_type': item.category_type.name,
                        'type': item.type.name,
                        'door_type': item.door_type,
                        'is_locked': item.is_locked,
                        }
                    continue

                levels[level.id]['items'][item.id] = {
                    'category_type': item.category_type.name,
                    'type': item.type.name,
                    'health': item.stats.health,
                    'health_total': item.stats.health_total,
                    'x': item.rect.x,
                    'y': item.rect.y,
                    'direction': item.direction,
                    }

                if item.category_type == ActorCategoryType.COMPUTER:
                    levels[level.id]['items'][item.id].update({
                        'visited': item.visited,
                    })
        return res

    @staticmethod
    def get_items_not_initial_actor_stats_to_persist(game):
        """Returns a dictionary with the items' stats to persist
        only for items not initially in a fresh game.
        """
        res = {'game_levels': {}}
        levels = res['game_levels']
        for game_level in game.levels:
            level = {
                'world_shift': game_level.world_shift,
                'world_shift_initial': game_level.world_shift_initial,
                'world_shift_top': game_level.world_shift_top,
                'world_shift_top_initial': game_level.world_shift_top_initial,
                'items': {},
                }

            include_in_inventory_items = False
            if game_level.id == game.level.id:
                include_in_inventory_items = True
                items = chain(
                    game_level.items,
                    game.player.stats['apples_stock'],
                    game.player.stats['door_keys_stock'],
                    game.player.stats['potions_power'],
                    game.player.stats['potions_health'],
                    game.player.stats['files_disks_stock'],
                    )
            else:
                items = game_level.items

            for item in items:
                if not include_in_inventory_items and not item.is_not_initial_actor:
                    continue
                if include_in_inventory_items and not item.is_not_initial_actor \
                        and not item.is_location_in_inventory:
                    continue

                level['items'][item.id] = {
                    'is_not_initial_actor': item.is_not_initial_actor,
                    'name': item.name,
                    'base_type': item.base_type.name,
                    'category_type': item.category_type.name,
                    'type': item.type.name,
                    'type_name': item.__class__.__name__,
                    'health': item.stats.health,
                    'health_total': item.stats.health_total,
                    'direction': item.direction,
                    'frame_index': round(item.frame_index, 3),
                    'x': item.rect.x,
                    'y': item.rect.y,
                    'is_location_in_inventory': item.is_location_in_inventory
                    }

                if item.category_type == ActorCategoryType.POTION:
                    level['items'][item.id].update({
                        'power': item.stats.power,
                        'power_total': item.stats.power_total,
                        })
                elif item.category_type == ActorCategoryType.FILES_DISK:
                    level['items'][item.id].update({
                        'msg_id': item.msg_id,
                        'is_encrypted': item.is_msg_encrypted(item.msg_id, game),
                        'has_been_read': item.has_msg_been_read(item.msg_id, game),
                        })
                elif item.category_type == ActorCategoryType.DOOR_KEY:
                    level['items'][item.id].update({
                        'door': item.door.id,
                        })

                levels[game_level.id] = level
        return res


class ActorMagic(Actor):
    """Represents a magic actor.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        if not getattr(self, 'base_type', None):
            self.base_type = ActorBaseType.MAGIC

        super().__init__(x, y, game, name=name)

    def kill_hook(self):
        self.target.target_of_spells_count[self.__class__.__name__] -= 1
        self.game.level.spells_on_level_count[self.__class__.__base__.__name__] -= 1
        super().kill_hook()

    def draw_health(self):
        pass


class ActorMsg(Actor):
    """Represents a message actor.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        if not getattr(self, 'base_type', None):
            self.base_type = ActorBaseType.TEXT_MSG

        super().__init__(x, y, game, name=name)

    def draw_health(self):
        pass


class MovingActor(Actor):
    """Represents a moving actor.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.can_move = True
        super().__init__(x, y, game, name, change_x=change_x, change_y=change_y,
                         items_to_drop=items_to_drop)

        self.border_left = border_left
        self.border_right = border_right
        self.border_top = border_top
        self.border_down = border_down
        self.frame_index = randint(0, self.images_sprite_no)

    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        super().update()

        # Check the boundaries and see if we need to reverse direction.
        if self.change_y and (self.rect.y > self.border_down or self.rect.y < self.border_top):
            self.change_y *= -1

        cur_pos_x = self.rect.x - self.game.level.world_shift
        if self.change_x and (cur_pos_x < self.border_left or cur_pos_x > self.border_right):
            self.change_x *= -1
            self.direction = DIRECTION_LEFT if self.direction == DIRECTION_RIGHT else DIRECTION_RIGHT
            self.last_shot_time = self.game.current_time


class NPC(MovingActor):
    """Represents an NPC.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.base_type = ActorBaseType.NPC
        self.category_type = ActorCategoryType.NPC
        self.is_npc = True
        self.can_drop_items = True

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)

    def update(self):
        super().update()

    @staticmethod
    def get_npc_ids_health(game, sorted_by_level=True):
        """Returns an ordered dictionary with the npc id, its total health, its current health and
        the level where you can find them.
          Example:
              OrderedDict([
              ('GHOST_GREEN_00001', ('health_total:   38.5', 'health:   38.5', 'level: 1', '1')),
              ('BAT_BLUE_00002', ('health_total:  112.0', 'health:  112.0', 'level: 4', '4')),
              ])
        """
        res = {}
        for level in game.levels:
            for npc in level.npcs:
                res[npc.id] = (f"health_total: {npc.stats.health_total:6}",
                               f"health: {npc.stats.health:6}",
                               f"level: {level.name:4}", f"{level.id:3d}")
        if sorted_by_level:
            return OrderedDict(sorted([x for x in res.items()], key=lambda x: (x[1][3], x[0])))
        return OrderedDict(sorted([x for x in res.items()]))

    @staticmethod
    def get_npc_ids_health_from_level(level):
        """Returns an ordered dictionary with the npc id, its total health and its current health
        for all NPCs from the level.
          Example:
              OrderedDict([
              ('GHOST_GREEN_00001', ('health_total:   38.5', 'health:   38.5', 'level: 1', '1')),
              ('BAT_BLUE_00002', ('health_total:  112.0', 'health:  112.0', 'level: 4', '4')),
              ])
        """
        res = {}
        for npc in level.npcs:
            res[npc.id] = (f"health_total: {npc.stats.health_total:6}",
                           f"health: {npc.stats.health:6}",
                           f"level: {level.name:4}", f"{level.id:3d}")

        return OrderedDict(sorted([x for x in res.items()]))

    @staticmethod
    def get_npcs_stats_to_persist(game):
        """Returns a dictionary with all the NPCs' stats to persist."""
        res = {'game_levels': {}}
        levels = res['game_levels']
        for game_level_id in sorted(list(game.player.stats['levels_visited'])):
            level = game.levels[game_level_id - 1]
            levels[game_level_id] = {
                'world_shift': level.world_shift,
                'world_shift_initial': level.world_shift_initial,
                'world_shift_top': level.world_shift_top,
                'world_shift_top_initial': level.world_shift_top_initial,
                'npcs': {},
                }
            for npc in level.npcs:
                if npc.is_not_initial_actor:
                    continue
                levels[level.id]['npcs'][npc.id] = {
                    'category_type': npc.category_type.name,
                    'type': npc.type.name,
                    'health': npc.stats.health,
                    'health_total': npc.stats.health_total,
                    'x': npc.rect.x,
                    'y': npc.rect.y,
                    'change_x': npc.change_x,
                    'change_y': npc.change_y,
                    'direction': npc.direction,
                    'hostility_level': npc.hostility_level,
                    'energy_shield_health': npc.stats.energy_shield.stats.health
                                            if npc.stats.energy_shield else 0,
                    'npc_summoned_count':npc.npc_summoned_count,
                    }
        return res

    @staticmethod
    def get_npcs_not_initial_actor_stats_to_persist(game):
        """Returns a dictionary with the NPCs' stats to persist
        only for NPCs not initially in a fresh game.
        """
        res = {'game_levels': {}}
        levels = res['game_levels']
        for game_level in game.levels:
            level = {
                'world_shift': game_level.world_shift,
                'world_shift_initial': game_level.world_shift_initial,
                'world_shift_top': game_level.world_shift_top,
                'world_shift_top_initial': game_level.world_shift_top_initial,
                'npcs': {},
                }
            for npc in game_level.npcs:
                if not npc.is_not_initial_actor:
                    continue
                level['npcs'][npc.id] = {
                    'is_not_initial_actor': npc.is_not_initial_actor,
                    'name': npc.name,
                    'base_type': npc.base_type.name,
                    'category_type': npc.category_type.name,
                    'type': npc.type.name,
                    'type_name': npc.__class__.__name__,
                    'health': npc.stats.health,
                    'health_total': npc.stats.health_total,
                    'frame_index': round(npc.frame_index, 3),
                    'x': npc.rect.x,
                    'y': npc.rect.y,
                    'change_x': npc.change_x,
                    'change_y': npc.change_y,
                    'magic_resistance': npc.magic_resistance,
                    'hostility_level': npc.hostility_level,
                    'direction': npc.direction,
                    'shot_x_delta_max': npc.shot_x_delta_max,
                    'shot_y_delta': npc.shot_y_delta,
                    'spell_cast_x_delta_max': npc.spell_cast_x_delta_max,
                    'spell_cast_y_delta_max': npc.spell_cast_y_delta_max,
                    'health_bar_delta_y': npc.health_bar_delta_y,
                    'power_recovery': npc.stats.power_recovery,
                    'has_energy_shield': npc.stats.energy_shield and True or False,
                    'energy_shield_health': npc.stats.energy_shield.stats.health
                                            if npc.stats.energy_shield else 0,
                    'energy_shield_health_total': npc.stats.energy_shield.stats.health_total
                                            if npc.stats.energy_shield else 0,
                    'energy_shield_pos_delta_x': npc.stats.energy_shield_pos_delta_x,
                    'energy_shield_pos_delta_y': npc.stats.energy_shield_pos_delta_y,
                    'time_between_energy_shield_casting': npc.stats.time_between_energy_shield_casting,
                    'npc_summoned_count':npc.npc_summoned_count,
                    'border_left': npc.border_left,
                    'border_right': npc.border_right,
                    'border_top': npc.border_top,
                    'border_down': npc.border_down,
                    'items_to_drop': []
                    }
                if npc.can_drop_items and npc.items_to_drop:
                    items_to_drop = []
                    for item in npc.items_to_drop:
                        if is_json_serializable(item.args):
                            item_args = item.args
                        else:
                            log.error("Cannot persist drop args for NPC %s: "
                                        "%s", npc.id, item.class_.__name__)
                            continue
                        item_to_drop = {
                            'type_name': item.class_.__name__,
                            'probability_to_drop': item.probability_to_drop,
                            'x_delta': item.x_delta,
                            'y_delta': item.y_delta,
                            'args': item_args,
                            }
                        items_to_drop.append(item_to_drop)
                    level['npcs'][npc.id]['items_to_drop'] = items_to_drop

                levels[game_level.id] = level
        return res
