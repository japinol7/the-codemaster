"""Module lightning bolts."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import BM_MAGIC_FOLDER
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorMagic
from codemaster.models.actors.items.explosions import ExplosionMagicC2
from codemaster.models.stats import Stats
from codemaster.config.settings import Settings


class LightningBolt(ActorMagic):
    """Represents a lightning bolt.
    It is not intended to be instantiated.
    """
    max_spells_on_level = 6

    def __init__(self, x, y, game, name=None, is_from_player_shot=None, owner=None, target=None):
        self.file_folder = BM_MAGIC_FOLDER
        self.file_name_key = 'im_lightning_bolt'
        self.images_sprite_no = 1
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
        self.animation_speed = 0.4
        self.collision_delta_y = 24
        super().__init__(x, -144, game, name=name)

        self.change_y = 12
        self.player.sound_effects and self.player.explosion_sound.play()

    def explosion(self):
        """When hit the target, explodes."""
        super().explosion()

        explosion = self.explosion_class(
                self.rect.centerx,
                self.target.rect.bottom - 60 - self.collision_delta_y,
                self.game, owner=self.player)
        self.game.level.explosions.add(explosion)
        self.game.level.all_sprites.add(explosion)

        explosion = self.explosion_class(
                self.rect.centerx,
                self.target.rect.centery - 60 - self.collision_delta_y,
                self.game, owner=self.player)
        self.game.level.explosions.add(explosion)
        self.game.level.all_sprites.add(explosion)

    def update_after_inc_index_hook(self):
        if self.target:
            self.rect.centerx = self.target.rect.centerx
        self.rect.y += self.change_y
        self.change_y += 2

        super().update_after_inc_index_hook()

        if self.rect.y > Settings.screen_height:
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


class LightningBoltA(LightningBolt):
    """Represents a lightning bolt of type A."""
    actor_type = ActorType.LIGHTNING_BOLT_A
    max_spells_on_target = 1
    power_min_to_use = {ActorType.LIGHTNING_BOLT_A.name: 30,
                        }
    power_consumption = {ActorType.LIGHTNING_BOLT_A.name: 25,
                         }

    def __init__(self, x, y, game, name=None, is_from_player_shot=None, owner=None, target=None):
        self.explosion_class = ExplosionMagicC2
        self.file_mid_prefix = '01'
        self.type = ActorType.LIGHTNING_BOLT_A
        super().__init__(x, y, game, name=name,
                         is_from_player_shot=is_from_player_shot,
                         owner=owner, target=target)
