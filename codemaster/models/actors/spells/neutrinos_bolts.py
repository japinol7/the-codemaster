"""Module neutrinos bolts."""
__author__ = 'Joan A. Pinol  (japinol)'

import math
import random
import time

import pygame as pg

from codemaster.config.constants import BM_MAGIC_FOLDER
from codemaster.tools.utils.colors import Color
from codemaster.models.experience_points import ExperiencePoints
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorMagic
from codemaster.models.clocks import ClockTimer
from codemaster.models.special_effects.fire_range import FireRange, VortexDrawMethod
from codemaster.models.stats import Stats
from codemaster.tools.logger.logger import log


class NeutrinosBolt(ActorMagic):
    """Represents a neutrinos bolt.
    It is not intended to be instantiated.
    """
    max_spells_on_level = 20

    def __init__(self, x, y, game, name=None, is_from_player_shot=None,
                 owner=None, target=None,
                 change_x=3.5, change_y=2.9):
        self.file_folder = BM_MAGIC_FOLDER
        self.file_name_key = 'im_neutrinos_bolt'
        self.images_sprite_no = 1
        self.category_type = ActorCategoryType.MAGIC
        self.is_from_player_shot = is_from_player_shot
        self.owner = owner
        self.owner_stats_key = 'magic_attack_spells'
        self.target = target
        self.is_a_player_shot = True if owner == game.player else False
        self.stats = Stats()
        self.health = self.health_total = 1
        self.stats.strength = self.stats.strength_total = 1
        self.change_x = change_x
        self.change_y = change_y
        self.animation_speed = 0.4
        self.collision_delta_y = 24
        self.time_in_secs = 6

        super().__init__(x, y, game, name=name)

        self.player.sound_effects and self.player.magic_bolt_sound.play()
        self.game.level.particle_sprites.add(self)
        self.particles = []
        self.color_mode = None
        self.color = None
        self.color_external = None
        self.size_rand = None
        self.size_ext_multiplier = None
        self.particle_pos_delta_y = 0.15
        self.particle_delta_size = 0.05
        self.particle_create_new = True
        self.clock_dying = ClockTimer(self.game, 3, trigger_method=self.die_soft)
        self.clock_dying_2 = None
        self.clock = ClockTimer(self.game, self.time_in_secs, trigger_method=self.die_hard)
        self.x_direction_multiplier = -1 if self.is_actor_on_the_left(self.player) else 1
        self.y_direction_multiplier = -1 if self.is_actor_on_top(self.player) else 1
        self.y_direction_multiplier *= 0 if self.is_actor_centered_on_y(self.player, epsilon=50) else 1
        self.damage_multiplier = 1.3
        self.time_last_updated_target_health = None

    def update(self):
        self.clock_dying.tick()
        self.clock_dying_2 and self.clock_dying_2.tick()
        self.clock.tick()
        self.update_target_health()

    def kill_hook(self):
        super().kill_hook()

    def update_target_health(self):
        if self.target == self.game.player and self.target.invulnerable:
            return

        if not self.time_last_updated_target_health:
            self.time_last_updated_target_health = time.perf_counter()

        if time.perf_counter() - self.time_last_updated_target_health < 0.2:
            return

        self.time_last_updated_target_health = time.perf_counter()

        if self.owner == self.game.player and self.target.hostility_level < 1:
            self.target.hostility_level = 1

        damage_range = 78
        is_between_x_boundaries = (self.player.rect.x - damage_range < self.rect.x
                                   < self.player.rect.x + damage_range)
        is_between_y_boundaries = (self.player.rect.y - damage_range < self.rect.y
                                   < self.player.rect.y + damage_range)
        if not (is_between_x_boundaries and is_between_y_boundaries):
            return

        self.game.is_log_debug and log.debug(
            f"{self.target.id} hit by {self.id}, health: {round(self.target.health, 2)}, "
            f"fire_range_partial_power: {self.power * self.damage_multiplier:.2f}, "
            f"magic_res: {self.target.magic_resistance * self.damage_multiplier:.2f}, "
            f"owner: {self.owner.id}")

        attack_power_res = self.power * self.damage_multiplier - self.target.magic_resistance * self.damage_multiplier
        if attack_power_res > 0:
            self.target.health -= attack_power_res

        if self.target.health <= 0:
            self.game.is_log_debug and log.debug(
                f"{self.target.id}, !!! Dead by {self.id}, owner: {self.owner.id} !!!")
            if self.is_a_player_shot:
                self.game.player.stats['score'] += ExperiencePoints.xp_points[self.target.type.name]

            if self.target != self.game.player:
                self.target.drop_items()
                self.target.kill_hook()
                self.game.player.sound_effects and self.game.player.enemy_hit_sound.play()
            else:
                self.target.die_hard()

    def die_soft(self):
        self.particle_pos_delta_y = 0.28
        self.particle_delta_size = 0.1
        self.damage_multiplier = 0.9

        self.clock_dying_2 = ClockTimer(self.game, 2, trigger_method=self.die_soft_2)

    def die_soft_2(self):
        self.particle_delta_size = 0.4
        self.damage_multiplier = 0.5

    def die_hard(self):
        self.damage_multiplier = 0.3
        self.particle_create_new = False

        self.update_target_health()

        if self.game.is_log_debug:
            log.debug(f"{self.id} killed when {self.clock.id} ticked {self.clock.get_time()} secs.")

        self.kill_hook()

    def update_particle_sprites(self):
        """This method will not be executed the same way as the other update methods.
        It will be updated along with all the rest of the special effects:
        after all normal sprites have been drawn to the screen.
        """

        if not self.target.alive():
            self.game.is_log_debug and log.debug(f"{self.id} killed because target {self.target.id} is not alive.")
            self.kill_hook()

        self.rect.centerx += self.change_x * self.x_direction_multiplier
        self.rect.centery += self.change_y * self.y_direction_multiplier

        for i, fire_range in sorted(enumerate(self.particles), reverse=True):
            fire_range.move(1)
            fire_range.draw(self.game.screen)
            if not fire_range.alive:
                self.particles.pop(i)

        if self.particle_create_new:
            for _ in range(3):
                self.particles.append(
                    FireRange([self.rect.x + 4, self.rect.y + 4],
                              angle=math.radians(random.randint(0, 360)),
                              speed=random.randint(3, 6),
                              color=self.color_external, scale=2,
                              color_transparency_ratio=0.7))
            for _ in range(2):
                self.particles.append(
                    FireRange([self.rect.x + 3, self.rect.y + 3],
                              angle=math.radians(random.randint(0, 360)),
                              speed=random.randint(2, 6),
                              color=self.color, scale=2.1,
                              color_transparency_ratio=0.7))
            self.particles.append(
                FireRange([self.rect.x + 1, self.rect.y + 1],
                          angle=math.radians(random.randint(0, 360)),
                          speed=random.randint(2, 6),
                          color=self.color, scale=1.0,
                          draw_method=VortexDrawMethod.POLYGON,
                          color_transparency_ratio=0.7))
            self.particles.append(
                FireRange([self.rect.x, self.rect.y],
                          angle=math.radians(random.randint(0, 360)),
                          speed=random.randint(3, 6),
                          color=self.color_external, scale=1.0,
                          draw_method=VortexDrawMethod.POLYGON,
                          color_transparency_ratio=0.7))

        if not self.particles:
            self.die_hard()


class NeutrinosBoltB(NeutrinosBolt):
    """Represents a neutrinos bolt, of type B."""
    actor_type = ActorType.NEUTRINOS_BOLT_B
    max_spells_on_target = 1
    power_min_to_use = {ActorType.NEUTRINOS_BOLT_B.name: 18,
                        }
    power_consumption = {ActorType.NEUTRINOS_BOLT_B.name: 14,
                         }

    def __init__(self, x, y, game, name=None, is_from_player_shot=None,
                 owner=None, target=None,
                 change_x=6.35, change_y=4.7):
        self.file_mid_prefix = '01'
        self.type = ActorType.NEUTRINOS_BOLT_B
        self.stats = Stats()
        super().__init__(x, y, game, name=name,
                         is_from_player_shot=is_from_player_shot,
                         owner=owner, target=target,
                         change_x=change_x, change_y=change_y)
        self.power = self.power_total = 110
        self.color = Color.BLUE_VIOLET
        self.color_external = 250, 0, 0
        self.color_mode = pg.BLEND_RGB_ADD
        self.size_rand = 3, 8
        self.size_ext_multiplier = 1.8


class NeutrinosBoltA(NeutrinosBolt):
    """Represents a neutrinos bolt, of type A."""
    actor_type = ActorType.NEUTRINOS_BOLT_A
    max_spells_on_target = 1
    power_min_to_use = {ActorType.NEUTRINOS_BOLT_A.name: 20,
                        }
    power_consumption = {ActorType.NEUTRINOS_BOLT_A.name: 16,
                         }

    def __init__(self, x, y, game, name=None, is_from_player_shot=None,
                 owner=None, target=None,
                 change_x=7.1, change_y=6.5):
        self.file_mid_prefix = '01'
        self.type = ActorType.NEUTRINOS_BOLT_A
        self.stats = Stats()

        super().__init__(x, y, game, name=name,
                         is_from_player_shot=is_from_player_shot,
                         owner=owner, target=target,
                         change_x=change_x, change_y=change_y)

        self.power = self.power_total = 125
        self.color = Color.BLUE_VIOLET
        self.color_external = 250, 150, 0
        self.color_mode = pg.BLEND_RGB_ADD
        self.size_rand = 4, 9
        self.size_ext_multiplier = 1.9
