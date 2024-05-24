"""Module drain_life."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import BM_MAGIC_FOLDER, DIRECTION_RIP
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorMagic
from codemaster.models.stats import Stats
from codemaster.config.settings import Settings
from codemaster import resources
from codemaster.tools.logger.logger import log
from codemaster.tools.utils.utils import Point


class DrainLife(ActorMagic):
    """Represents a drain life spell.
    It is not intended to be instantiated.
    """
    max_spells_on_level = 6

    def __init__(self, x, y, game, name=None, is_from_player_shot=None, owner=None, target=None):
        self.file_folder = BM_MAGIC_FOLDER
        self.file_name_key = 'im_drain_life'
        self.images_sprite_no = 3
        self.category_type = ActorCategoryType.MAGIC
        self.is_from_player_shot = is_from_player_shot
        self.owner = owner
        self.owner_stats_key = 'magic_attack_spells'
        self.target = target
        self.is_a_player_shot = True if owner == game.player else False
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.power = self.stats.power_total = 0
        self.stats.strength = self.stats.strength_total = 1
        self.animation_speed = 0.8
        self.collision_delta_y = 2
        self.max_distance_to_origin = 1000

        super().__init__(x, y, game, name=name)

        self.origin = Point(self.rect.x, self.rect.y)
        self.change_y = 2
        self.player.sound_effects and resources.Resource.bullet_t4_sound.play()

    def explosion(self):
        """When hit the target, explodes."""
        super().explosion()

        if self.owner == self.game.player and self.target.hostility_level < 1:
            self.target.hostility_level = 1

        if self.target.direction == DIRECTION_RIP or self.target.invulnerable:
            return

        self.game.is_log_debug and log.debug(
            f"{self.target.id} hit by {self.id}, "
            f"pc_health: {str(round(self.target.health, 2))}, "
            f"magic_attach_power: {str(self.stats.power)}, "
            f"magic_res: {self.target.magic_resistance:.2f}, ")

        attack_power_res = self.power - self.target.magic_resistance
        if attack_power_res > 0:
            self.target.health -= attack_power_res

        if self.target.health <= 0:
            self.game.is_log_debug and log.debug(
                f"{self.target.id}, !!! Dead by magic_attach {self.id}, "
                f"owner: {self.owner.id} !!!")
            self.target.die_hard()

    def update_after_inc_index_hook(self):
        if self.target:
            delta_x, delta_y = 1, 1
            max_delta = 11
            if self.rect.x > self.target.rect.x:
                delta_x *= -1
            if self.rect.centery > self.target.rect.centery:
                delta_y *= -1
            self.change_x += delta_x
            self.change_y += delta_y

            if self.change_x > max_delta:
                self.change_x = max_delta
            if self.change_y > max_delta:
                self.change_y = max_delta
            if self.change_x < -max_delta:
                self.change_x = -max_delta
            if self.change_y < -max_delta:
                self.change_y = -max_delta

        self.rect.x += self.change_x
        self.rect.y += self.change_y

        super().update_after_inc_index_hook()

        if self.rect.y > Settings.screen_height:
            self.kill_hook()
        elif self.origin.y - self.rect.y > self.max_distance_to_origin:
            self.kill_hook()
        elif self.origin.x - self.rect.x > self.max_distance_to_origin:
            self.kill_hook()

    def update_when_hit(self):
        """Can only hit the target."""
        if not self.target:
            return

        self.target.rect.y += self.collision_delta_y
        target_hit_list = pg.sprite.spritecollide(self, [self.target], False)
        for _ in target_hit_list:
            self.explosion()
            self.kill_hook()
        self.target.rect.y -= self.collision_delta_y


class DrainLifeB(DrainLife):
    """Represents a drain life spell of type B."""
    actor_type = ActorType.DRAIN_LIFE_B
    max_spells_on_target = 2
    power_min_to_use = {ActorType.DRAIN_LIFE_B.name: 30,
                        }
    power_consumption = {ActorType.DRAIN_LIFE_B.name: 25,
                         }

    def __init__(self, x, y, game, name=None, is_from_player_shot=None, owner=None, target=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.DRAIN_LIFE_B

        super().__init__(x, y, game, name=name,
                         is_from_player_shot=is_from_player_shot,
                         owner=owner, target=target)

        self.stats.power = self.stats.power_total = self.game.player.stats['magic_resistance_base'] + 4
        self.max_distance_to_origin = 1200


class DrainLifeA(DrainLife):
    """Represents a drain life spell of type A."""
    actor_type = ActorType.DRAIN_LIFE_A
    max_spells_on_target = 2
    power_min_to_use = {ActorType.DRAIN_LIFE_A.name: 30,
                        }
    power_consumption = {ActorType.DRAIN_LIFE_A.name: 25,
                         }

    def __init__(self, x, y, game, name=None, is_from_player_shot=None, owner=None, target=None):
        self.file_mid_prefix = '02'
        self.type = ActorType.DRAIN_LIFE_A

        super().__init__(x, y, game, name=name,
                         is_from_player_shot=is_from_player_shot,
                         owner=owner, target=target)

        self.stats.power = self.stats.power_total = self.game.player.stats['magic_resistance_base'] + 9
        self.max_distance_to_origin = 1200
