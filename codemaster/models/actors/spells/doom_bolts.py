"""Module doom bolts."""
__author__ = 'Joan A. Pinol  (japinol)'

import random

import pygame as pg

from codemaster.config.constants import BM_MAGIC_FOLDER, DIRECTION_RIGHT
from codemaster.tools.utils.colors import Color
from codemaster.tools.utils import utils_graphics as libg_jp
from codemaster.models.experience_points import ExperiencePoints
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import Actor, ActorMagic
from codemaster.models.actors.items.explosions import ExplosionMagicC4
from codemaster.models.clocks import ClockTimer
from codemaster.models.stats import Stats
from codemaster.tools.logger.logger import log
from codemaster.config.settings import Settings


class DoomBolt(ActorMagic):
    """Represents a doom bolt.
    It is not intended to be instantiated.
    """
    max_spells_on_level = 6
    surface_renders = {}

    def __init__(self, x, y, game, name=None, is_from_player_shot=None, owner=None, target=None):
        self.file_folder = BM_MAGIC_FOLDER
        self.file_name_key = 'im_doom_bolt'
        self.images_sprite_no = 2
        self.category_type = ActorCategoryType.MAGIC
        self.is_from_player_shot = is_from_player_shot
        self.owner = owner
        self.owner_stats_key = 'magic_attack_spells'
        self.target = target
        self.is_a_player_shot = True if owner == game.player else False
        self.stats = Stats()
        self.health = self.health_total = 1
        self.stats.strength = self.stats.strength_total = 1
        self.animation_speed = 0.4
        self.collision_delta_y = 24
        self.time_in_secs = 10
        super().__init__(x, -136, game, name=name)

        self.change_y = 12
        self.has_hit_target = False
        self.direction = DIRECTION_RIGHT
        self.player.sound_effects and self.player.explosion_sound.play()
        self.game.level.particle_tuple_sprites.add(self)
        self.particles = {}
        self.particle_id = 0
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

    def update_sprite_image(self):
        if not self.has_hit_target:
            self.image = Actor.sprite_images[self.type.name][self.direction][0]
            return
        self.image = Actor.sprite_images[self.type.name][self.direction][1]

    def update_after_inc_index_hook(self):
        if self.target:
            self.rect.centerx = self.target.rect.centerx
        if not self.has_hit_target:
            self.rect.y += self.change_y
            self.change_y += 2
            super().update_after_inc_index_hook()

        if self.rect.y > Settings.screen_height:
            self.has_hit_target = True

    def update_when_hit(self):
        """Can only hit the target."""
        if not self.target:
            return

        self.target.rect.y += self.collision_delta_y
        target_hit_list = pg.sprite.spritecollide(self, [self.target], False)
        for _ in target_hit_list:
            self.has_hit_target = True
        self.target.rect.y -= self.collision_delta_y

    def update(self):
        super().update()
        self.clock_dying.tick()
        self.clock_dying_2 and self.clock_dying_2.tick()
        self.clock.tick()

    def update_target_health(self, divider):
        if self.target == self.game.player and self.target.invulnerable:
            return

        if self.owner == self.game.player and self.target.hostility_level < 1:
            self.target.hostility_level = 1

        self.game.is_log_debug and log.debug(
            f"{self.target.id} hit by {self.id}, health: {round(self.target.health, 2)}, "
            f"doom_bolt_partial_power: {self.power / divider:.2f}, "
            f"magic_res: {self.target.magic_resistance / divider:.2f}, owner: {self.owner.id}")

        attack_power_res = self.power / divider - self.target.magic_resistance / divider
        if attack_power_res > 0:
            self.target.health -= attack_power_res

        if self.target == self.game.player:
            self.power -= self.power / divider

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
        target = self.target

        self.game.is_log_debug and log.debug(
            f"{self.id} killed when {self.clock.id} ticked {self.clock.get_time()} secs.")

        self.update_target_health(divider=1)

        if target.health <= 0:
            self.game.is_log_debug and log.debug(
                f"{target.id}, !!! Dead by {self.id}, owner: {self.owner.id} !!!")
            if self.is_a_player_shot:
                self.game.player.stats['score'] += ExperiencePoints.xp_points[target.type.name]

            if target != self.game.player:
                target.drop_items()
                target.kill_hook()
                self.game.player.sound_effects and self.game.player.enemy_hit_sound.play()
            else:
                target.die_hard()

        self.explosion()
        self.kill_hook()

    def explosion(self):
        """When hit the target, explodes."""
        super().explosion()

        explosion = self.explosion_class(
                self.target.rect.centerx - 40,
                self.target.rect.bottom - 60 - self.collision_delta_y,
                self.game, owner=self.owner)
        self.game.level.explosions.add(explosion)
        self.game.level.all_sprites.add(explosion)

        explosion = self.explosion_class(
                self.target.rect.centerx - 40,
                self.target.rect.centery - 60 - self.collision_delta_y,
                self.game, owner=self.owner)
        self.game.level.explosions.add(explosion)
        self.game.level.all_sprites.add(explosion)

    def update_particle_sprites(self):
        """This method will not be executed the same way as the other update methods.
        It will be updated along with all the rest of the special effects:
        after all normal sprites have been drawn to the screen.
        """
        if not self.has_hit_target:
            return

        if not self.target.alive():
            self.game.is_log_debug and log.debug(
                f"{self.id} killed because target {self.target.id} is not alive.")
            self.kill_hook()

        if self.target:
            self.rect.centerx = self.target.rect.centerx
            self.rect.centery = self.target.rect.centery

        if self.particle_create_new:
            self.particles.update({
                self.particle_id:
                    [[self.rect.centerx, self.rect.centery],
                     [random.randint(0, 22) / 10 - 1, -6],
                     random.randint(self.size_rand[0], self.size_rand[1])]
                    })
            self.particle_id += 1

        particles_to_remove = []
        for key, particle in self.particles.items():
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[1][1] += self.particle_pos_delta_y
            particle[2] -= self.particle_delta_size

            if particle[2] <= 0:
                particles_to_remove.append(key)
                continue

            radius = particle[2]
            radius_ext = radius * self.size_ext_multiplier

            self.game.screen.blit(
                    libg_jp.create_circle_surface_cached(
                        radius_ext, self.color_external,
                        surface_renders=self.__class__.surface_renders),
                    (int(particle[0][0] - radius_ext), int(particle[0][1] - radius_ext)),
                    special_flags=self.color_mode)

            libg_jp.create_circle_in_surface_cached(
                    self.game.screen, self.color,
                    position=(int(particle[0][0] - radius), int(particle[0][1] - radius)),
                    radius=int(particle[2]),
                    surface_renders=self.__class__.surface_renders)

            if particle[2] <= 0:
                particles_to_remove.append(key)

        for particle_key in particles_to_remove:
            self.particles.pop(particle_key, None)

        if not self.particles:
            self.die_hard()


class DoomBoltB(DoomBolt):
    """Represents a doom bolt of type B."""
    actor_type = ActorType.DOOM_BOLT_B
    max_spells_on_target = 1
    power_min_to_use = {ActorType.DOOM_BOLT_B.name: 30,
                        }
    power_consumption = {ActorType.DOOM_BOLT_B.name: 25,
                         }

    def __init__(self, x, y, game, name=None, is_from_player_shot=None, owner=None, target=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.DOOM_BOLT_B
        self.explosion_class = ExplosionMagicC4

        super().__init__(x, y, game, name=name,
                         is_from_player_shot=is_from_player_shot,
                         owner=owner, target=target)
        self.power = self.power_total = 110
        self.color = Color.YELLOW
        self.color_external = Color.GREEN
        self.color_mode = pg.BLEND_RGB_ADD
        self.size_rand = (3, 8)
        self.size_ext_multiplier = 1.8


class DoomBoltA(DoomBolt):
    """Represents a doom bolt of type A."""
    actor_type = ActorType.DOOM_BOLT_A
    max_spells_on_target = 1
    power_min_to_use = {ActorType.DOOM_BOLT_A.name: 38,
                        }
    power_consumption = {ActorType.DOOM_BOLT_A.name: 32,
                         }

    def __init__(self, x, y, game, name=None, is_from_player_shot=None, owner=None, target=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.DOOM_BOLT_A
        self.explosion_class = ExplosionMagicC4

        super().__init__(x, y, game, name=name,
                         is_from_player_shot=is_from_player_shot,
                         owner=owner, target=target)

        self.power = self.power_total = 126
        self.color = (240, 240, 240)
        self.color_external = Color.RED
        self.color_mode = pg.BLENDMODE_NONE
        self.size_rand = (4, 9)
        self.size_ext_multiplier = 1.9
