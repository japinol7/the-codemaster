"""Module selectors."""
__author__ = 'Joan A. Pinol  (japinol)'

import logging

import pygame as pg


from codemaster.config.constants import BM_SELECTORS_FOLDER
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorItem
from codemaster.models.stats import Stats
from codemaster.utils.colors import Color
from codemaster.models.special_effects.light import Light, LightGrid
from codemaster.config.settings import logger
from codemaster.models.actors.items import LightningA
from codemaster import resources


class Selector(ActorItem):
    """Represents a selector.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        self.file_folder = BM_SELECTORS_FOLDER
        self.file_name_key = 'im_selectors'
        self.images_sprite_no = 1
        self.category_type = ActorCategoryType.SELECTOR
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.power = self.stats.power_total = 0
        self.stats.strength = self.stats.strength_total = 1
        self.light_grid = None
        self.light_color = None

        super().__init__(x, y, game, name=name)

        self._create_light()

    def _create_light(self):
        self.light_color = Color.GREEN
        self.light_grid = LightGrid(self.game.screen.get_size())
        self.light_grid.add_light(
            Light((0, 0), radius=30, color=self.light_color, alpha=255),
            )

    def update_after_inc_index_hook(self):
        mx, my = self.game.mouse_pos
        self.rect.centerx, self.rect.centery = mx, my
        for light in self.light_grid.lights.values():
            light.set_color(self.light_color, override_alpha=True)
            light.position = (mx, my)
        self.light_grid.render(self.game.screen)

    def update_when_hit(self):
        """Cannot be hit."""
        pass

    def get_pointed_sprites(self):
        hit_list = []

        if logging.getLevelName(logger.level) == 'DEBUG':
            hit_list = pg.sprite.spritecollide(self, self.game.level.all_sprites, False)
            for sprite in hit_list:
                logger.debug(f"Mouse sprites: {sprite.id} in pos: ({sprite.rect.x}, {sprite.rect.y})")

        if not self.game.is_magic_on:
            return hit_list

        if self.game.player.stats['level'] < 2:
            return hit_list

        if self.game.player.stats['power'] < LightningA.power_min_to_use[ActorType.LIGHTNING_A.name]:
            self.game.sound_effects and resources.Resource.weapon_empty_sound.play()
            return hit_list

        snake_body_hit_list = pg.sprite.spritecollide(self, self.game.level.snakes_body_pieces, False)
        for sprite in snake_body_hit_list:
            self.game.player.stats['power'] -= LightningA.power_consumption[ActorType.LIGHTNING_A.name]
            lightning = LightningA(sprite.rect.centerx, sprite.rect.y, self.game,
                                   is_from_player_shot=True, owner=self.game.player, target=sprite.snake)
            hit_list.append(lightning)
            self.game.magic_sprites.add(lightning)
            self.game.active_sprites.add(lightning)
            break

        if snake_body_hit_list:
            return snake_body_hit_list

        hit_list = pg.sprite.spritecollide(self, self.game.level.npcs, False)
        for sprite in hit_list:
            self.game.player.stats['power'] -= LightningA.power_consumption[ActorType.LIGHTNING_A.name]
            lightning = LightningA(sprite.rect.centerx, sprite.rect.y, self.game,
                                   is_from_player_shot=True, owner=self.game.player, target=sprite)
            self.game.magic_sprites.add(lightning)
            self.game.active_sprites.add(lightning)
            break

        return hit_list


class SelectorA(Selector):
    """Represents a selector of type A."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.SELECTOR_A
        super().__init__(x, y, game, name=name)
