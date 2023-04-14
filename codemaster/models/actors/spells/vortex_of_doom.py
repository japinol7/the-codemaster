"""Module vortex of doom."""
__author__ = 'Joan A. Pinol  (japinol)'

import math
import random

import pygame as pg

from codemaster.config.constants import BM_MAGIC_FOLDER
from codemaster.tools.utils.colors import Color
from codemaster.models.experience_points import ExperiencePoints
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorMagic
from codemaster.models.clocks import ClockTimer
from codemaster.models.special_effects.vortex import Vortex, VortexDrawMethod
from codemaster.models.stats import Stats
from codemaster.tools.logger.logger import log


class VortexOfDoom(ActorMagic):
    """Represents a vortex of doom.
    It is not intended to be instantiated.
    """
    max_spells_on_level = 3

    def __init__(self, x, y, game, name=None, is_from_player_shot=None, owner=None, target=None):
        self.file_folder = BM_MAGIC_FOLDER
        self.file_name_key = 'im_vortex_of_doom'
        self.images_sprite_no = 1
        self.category_type = ActorCategoryType.MAGIC
        self.is_from_player_shot = is_from_player_shot
        self.owner = owner
        self.owner_stats_key = 'magic_attack_spells'
        self.target = target
        self.is_a_player_shot = True if owner == game.player else False
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.strength = self.stats.strength_total = 1
        self.animation_speed = 0.4
        self.collision_delta_y = 24
        self.time_in_secs = 10
        super().__init__(x, y, game, name=name)

        self.player.sound_effects and self.player.explosion_sound.play()
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

    def update(self):
        self.clock_dying.tick()
        self.clock_dying_2 and self.clock_dying_2.tick()
        self.clock.tick()

    def kill_hook(self):
        super().kill_hook()

    def update_target_health(self, divider):
        log.debug(f"{self.target.id} hit by {self.id}, npc_health: {str(round(self.target.stats.health, 2))}, "
                  f"vortex_partial_power: {str(self.stats.power / divider)}")
        self.target.stats.health -= self.stats.power / divider
        self.stats.power -= self.stats.power / divider

    def die_soft(self):
        self.particle_pos_delta_y = 0.28
        self.particle_delta_size = 0.1

        self.update_target_health(divider=5)
        self.clock_dying_2 = ClockTimer(self.game, 2, trigger_method=self.die_soft_2)

    def die_soft_2(self):
        self.particle_delta_size = 0.4
        self.particle_create_new = False

        self.update_target_health(divider=4)

    def die_hard(self):
        log.debug(f"{self.id} killed when {self.clock.id} ticked {self.clock.get_time()} secs.")
        log.debug(f"{self.target.id} hit by {self.id}, npc_health: {str(round(self.target.stats.health, 2))}, "
                  f"vortex_partial_power: {str(self.stats.power)}")
        self.target.stats.health -= self.stats.power
        if self.target.stats.health <= 0:
            npc = self.target
            log.debug(f"{npc.id}, !!! Dead by {self.id} !!!")
            if self.is_a_player_shot:
                self.game.player.stats['score'] += ExperiencePoints.xp_points[npc.type.name]
            npc.drop_items()
            npc.kill_hook()
            self.game.player.sound_effects and self.game.player.enemy_hit_sound.play()

            self.target.kill_hook()
        self.kill_hook()

    def update_particle_sprites(self):
        """This method will not be executed the same way as the other update methods.
        It will be updated along with all the rest of the special effects:
        after all normal sprites have been drawn to the screen.
        """

        if not self.target.alive():
            log.debug(f"{self.id} killed because target {self.target.id} is not alive.")
            self.kill_hook()

        if self.target:
            self.rect.centerx = self.target.rect.centerx
            self.rect.centery = self.target.rect.centery

        for i, vortex in sorted(enumerate(self.particles), reverse=True):
            vortex.move(0.8)
            vortex.draw(self.game.screen)
            if not vortex.alive:
                self.particles.pop(i)

        if self.particle_create_new:
            for i in range(3):
                self.particles.append(
                    Vortex([self.rect.x + 4, self.rect.y + 4],
                           angle=math.radians(random.randint(0, 360)),
                           speed=random.randint(2, 6),
                           color=self.color_external, scale=2.6))
            for i in range(1):
                self.particles.append(
                    Vortex([self.rect.x, self.rect.y],
                           angle=math.radians(random.randint(0, 360)),
                           speed=random.randint(2, 6),
                           color=self.color, scale=1.5,
                           draw_method=VortexDrawMethod.POLYGON))

        if not self.particles:
            self.die_hard()


class VortexOfDoomB(VortexOfDoom):
    """Represents a vortex of doom of type B."""
    actor_type = ActorType.VORTEX_OF_DOOM_B
    max_spells_on_target = 1
    power_min_to_use = {ActorType.VORTEX_OF_DOOM_B.name: 18,
                        }
    power_consumption = {ActorType.VORTEX_OF_DOOM_B.name: 14,
                         }

    def __init__(self, x, y, game, name=None, is_from_player_shot=None, owner=None, target=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.VORTEX_OF_DOOM_B
        self.stats = Stats()
        super().__init__(x, y, game, name=name,
                         is_from_player_shot=is_from_player_shot,
                         owner=owner, target=target)
        self.stats.power = self.stats.power_total = 110
        self.color = Color.BLACK_SAFE
        self.color_external = Color.GREEN
        self.color_mode = pg.BLEND_RGB_ADD
        self.size_rand = (3, 8)
        self.size_ext_multiplier = 1.8


class VortexOfDoomA(VortexOfDoom):
    """Represents a vortex of doom of type A."""
    actor_type = ActorType.VORTEX_OF_DOOM_A
    max_spells_on_target = 1
    power_min_to_use = {ActorType.VORTEX_OF_DOOM_A.name: 20,
                        }
    power_consumption = {ActorType.VORTEX_OF_DOOM_A.name: 16,
                         }

    def __init__(self, x, y, game, name=None, is_from_player_shot=None, owner=None, target=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.VORTEX_OF_DOOM_A
        self.stats = Stats()

        super().__init__(x, y, game, name=name,
                         is_from_player_shot=is_from_player_shot,
                         owner=owner, target=target)

        self.stats.power = self.stats.power_total = 126
        self.color = Color.BLACK_SAFE
        self.color_external = Color.RED
        self.color_mode = pg.BLEND_RGB_ADD
        self.size_rand = (4, 9)
        self.size_ext_multiplier = 1.9
