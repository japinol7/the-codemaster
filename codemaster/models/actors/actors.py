"""Module actors."""
__author__ = 'Joan A. Pinol  (japinol)'

from collections import Counter, OrderedDict
from os import path
from random import randint

import pygame as pg

from codemaster.tools.utils import utils_graphics as libg_jp
from codemaster.tools.utils.colors import Color
from codemaster.tools.logger.logger import log
from codemaster.config.settings import Settings
from codemaster.config.constants import (
    FILE_NAMES,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
    )
from codemaster.models.experience_points import ExperiencePoints
from codemaster.models.actors.actor_types import ActorBaseType, ActorCategoryType, ActorType
from codemaster.models.actors.items import bullets
from codemaster.models.actors.items.bullets import Bullet, BulletType

NPC_STD_WIDTH = 61
NPC_STD_HEIGHT = 61
NPC_STRENGTH_BASE = 35


class DropItem:

    def __init__(self, actor_class, actor_type, probability_to_drop,
                 add_to_list, x_delta=0, y_delta=0, **args):
        self.type = actor_type
        self.class_ = actor_class
        self.add_to_list = add_to_list
        self.x_delta = x_delta
        self.y_delta = y_delta
        self.probability_to_drop = probability_to_drop
        self.args = args


class Actor(pg.sprite.Sprite):
    """Represents an actor.
    It is not intended to be instantiated.
    """
    type_id_count = Counter()
    # key: sprite_sheet_data_id, value: (image, walking_frames_l, walking_frames_r)
    sprite_images = {}
    # Security size so the sprite will not be too close to the border of the screen.
    CELL_SCREEN_SECURITY_SIZE = 1

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0, items_to_drop=None):
        super().__init__()
        Actor.type_id_count[self.type] += 1
        self.id = f"{self.type.name}_{Actor.type_id_count[self.type]:05d}"
        self.game = game
        self.player = game.player
        self.last_shot_time = 0
        self.time_between_shots_base = 1200
        self.last_spell_casted_time = 0
        self.time_between_spell_casting_base = 7200
        self.target_of_spells_count = Counter()

        if not getattr(self, 'base_type', None):
            self.base_type = ActorBaseType.NONE
        if not getattr(self, 'category_type', None):
            self.category_type = ActorCategoryType.NONE
        if not getattr(self, 'type', None):
            self.type = ActorType.NONE

        if not getattr(self, 'file_folder', None):
            self.file_folder = None
        if not getattr(self, 'file_mid_prefix', None):
            self.file_mid_prefix = None
        if not getattr(self, 'file_prefix', None):
            self.file_prefix = None
        if not getattr(self, 'file_name_key', None):
            self.file_name_key = None

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

        if not getattr(self, 'shot_x_delta_max', None):
            self.shot_x_delta_max = 500

        if not getattr(self, 'shot_y_delta', None):
            self.shot_y_delta = 75

        if not getattr(self, 'spell_cast_x_delta_max', None):
            self.spell_cast_x_delta_max = 500

        if not getattr(self, 'spell_cast_y_delta_max', None):
            self.spell_cast_y_delta_max = 500

        self.can_be_shot_by_its_owner = True
        self.name = name or 'unnamed'
        self.change_x = change_x
        self.change_y = change_y
        self.direction = DIRECTION_RIGHT

        self.init_before_load_sprites_hook()
        self._load_sprites()

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
                image.set_colorkey(Color.BLACK)
                walking_frames_l.append(image)
            Actor.sprite_images[self.type.name] = (image, walking_frames_l, walking_frames_r)
            self.image = walking_frames_r[0]
        else:
            self.image = Actor.sprite_images[self.type.name][0]

    def init_before_load_sprites_hook(self):
        pass

    def init_after_load_sprites_hook(self):
        pass

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
            log.debug(f"{self.id} hit by {bullet.id}, health: {str(round(self.stats.health, 2))}, "
                      f"bullet_power: {str(bullet.attack_power)}")
            self.stats.health -= bullet.attack_power
            has_been_hit = True
            bullet.kill()
            if bullet.owner == self.player and self.hostility_level == 0:
                self.hostility_level = 1

        has_been_hit and self.player.sound_effects and self.player.enemy_hit_sound.play()
        if self.stats.health <= 0:
            log.debug(f"{self.id}, !!! Dead by bullet {bullet.id} !!!")
            self.player.sound_effects and self.player.npc_killed_sound.play()
            if bullet.is_a_player_shot:
                self.player.stats['score'] += ExperiencePoints.xp_points[self.type.name]
            self.explosion()
            self.drop_items()
            self.kill_hook()

    def kill_hook(self):
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
                y=self.rect.y - Settings.sprite_health_bar_pos_rel.y,
                bar_width=Settings.sprite_health_bar_size.w,
                bar_height=Settings.sprite_health_bar_size.h,
                bar_outline=False, bar_up_line=True)

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
            log.debug(f"{self.id}, lucky_drop_dice: {str(lucky_drop)}, "
                      f"probability_to_drop: {item.probability_to_drop:3d}, "
                      f"item type: {item.type}")
            if lucky_drop + item.probability_to_drop >= 100:
                log.debug("Create item to drop")
                new_item = item.class_(
                    x=self.rect.x + item.x_delta, y=self.rect.y + item.y_delta, game=self.game,
                    **item.args)
                item.add_to_list.add(new_item)
                self.game.level.all_sprites.add(new_item)
                log.debug(f"Dropped: {new_item.id}")

    def is_actor_on_the_left(self, actor):
        if actor.rect.x < self.rect.x:
            return True
        return False

    def is_actor_on_the_right(self, actor):
        if actor.rect.x > self.rect.x:
            return True
        return False

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
        super().__init__(x, y, game, name=name)
        self.base_type = ActorBaseType.ITEM

    def draw_health(self):
        pass


class ActorMagic(Actor):
    """Represents a magic actor.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        super().__init__(x, y, game, name=name)
        self.base_type = ActorBaseType.MAGIC

    def kill_hook(self):
        self.target.target_of_spells_count[self.__class__.__name__] -= 1
        self.game.level.spells_on_level_count[self.__class__.__base__.__name__] -= 1
        self.kill()

    def draw_health(self):
        pass


class ActorMsg(Actor):
    """Represents a message actor.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        super().__init__(x, y, game, name=name)
        self.base_type = ActorBaseType.TEXT_MSG

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
    def get_npcs_health(game, sorted_by_level=True):
        """Returns an ordered dictionary with the npc id, its total health, its current health and
        the level where you can find them.
          Example:
              OrderedDict([('GHOST_GREEN_00001', ('health_total:   38.5', 'health:   38.5', 'level: 01  ', '  1')),
              ('BAT_BLUE_00002', ('health_total:  112.0', 'health:  112.0', 'level: 04  ', '  4'))])
        """
        res = {}
        for level in game.levels:
            for npc in level.npcs:
                res[npc.id] = (f"health_total: {npc.stats.health_total:6}",
                               f"health: {npc.stats.health:6}",
                               f"level: {level.name:4}", f"{level.id + 1:3d}")
        if sorted_by_level:
            return OrderedDict(sorted([x for x in res.items()], key=lambda x: (x[1][3], x[0])))
        return OrderedDict(sorted([x for x in res.items()]))


class PC(MovingActor):
    """Represents a PC.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None, change_x=0, change_y=0):
        self.base_type = ActorBaseType.PC
        self.category_type = ActorCategoryType.PC
        self.is_pc = True
        super().__init__(x, y, game, name=name, change_x=change_x, change_y=change_y)
        self.stats_old = None
        self.stats_render = None

    def update(self):
        super().update()
