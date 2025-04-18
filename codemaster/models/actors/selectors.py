"""Module selectors."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    BM_SELECTORS_FOLDER,
    DIRECTION_RIP,
    )
from codemaster.models.actors.actor_types import (
    ActorBaseType,
    ActorCategoryType,
    ActorType,
    )
from codemaster.models.actors.actors import ActorItem
from codemaster.models.stats import Stats
from codemaster.tools.utils.colors import Color
from codemaster.models.special_effects.light import Light, LightGrid
from codemaster.tools.logger.logger import log
from codemaster import resources
from codemaster.config.settings import Settings


class Selector(ActorItem):
    """Represents a selector.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None):
        self.file_folder = BM_SELECTORS_FOLDER
        self.file_name_key = 'im_selectors'
        self.images_sprite_no = 1
        self.base_type = ActorBaseType.SELECTOR
        self.category_type = ActorCategoryType.SELECTOR
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.power = self.stats.power_total = 0
        self.stats.strength = self.stats.strength_total = 1
        self.light_grid = None
        self.light_grid_surf_size = 34, 34
        self.light_grid_surf_size_half = self.light_grid_surf_size[0] // 2, self.light_grid_surf_size[1] // 2
        self.light_color = Color.GREEN
        self.sel_selected_actor_id = None
        self.sel_selected_actor_pos = 0, 0
        self.sel_selected_actor_world_shift = 0
        self.sel_selected_actor_world_shift_top = 0

        super().__init__(x, y, game, name=name)

        self._create_light()

    def update_sprite_image(self):
        pass

    def _create_light(self):
        self.light_grid = LightGrid(self.light_grid_surf_size)
        self.light_grid.add_light(
            Light((0, 0), radius=18, color=self.light_color, alpha=255),
            )

    def update_after_inc_index_hook(self):
        mx, my = self.game.mouse_pos
        self.rect.centerx, self.rect.centery = mx, my

        if Settings.has_selector_no_light:
            return

        # Create a surface with only the part of the screen that is needed for the light grid render
        sub_screen_rect = pg.Rect(
            mx - self.light_grid_surf_size_half[0],
            my - self.light_grid_surf_size_half[1],
            self.light_grid_surf_size[0],
            self.light_grid_surf_size[1])
        grid_surface = pg.Surface(sub_screen_rect.size)
        grid_surface.blit(self.game.screen, (0, 0), sub_screen_rect)

        # Render all the lights of the light grid
        for light in self.light_grid.lights.values():
            light.set_color(self.light_color, override_alpha=True)
            light.position = (self.light_grid_surf_size_half[0],
                              self.light_grid_surf_size_half[1])
        self.light_grid.render(grid_surface)
        self.game.screen.blit(grid_surface, sub_screen_rect)

    def update_when_hit(self):
        """Cannot be hit."""
        pass

    def get_pointed_sprites(self):
        hit_list = []

        if self.player.direction == DIRECTION_RIP:
            return hit_list

        if self.game.is_log_debug:
            hit_list = pg.sprite.spritecollide(
                self, self.game.level.sprites_for_debug_selector, False)
            for sprite in hit_list:
                log.debug(
                    f"Mouse sprites: {sprite.id} in pos: "
                    f"({sprite.rect.x}, {sprite.rect.y}) - lev pos: "
                    f"({sprite.rect.x + self.game.level.get_scroll_shift_delta()}, "
                    f"{sprite.rect.y - self.game.level.get_scroll_shift_top_delta()})")

        if not self.game.is_magic_on:
            return hit_list

        if not self.game.player.stats['magic_attack']:
            return hit_list

        magic_attack_cls = self.player.stats['magic_attack']
        if self.game.player.power < magic_attack_cls.power_min_to_use[magic_attack_cls.actor_type.name]:
            self.game.sound_effects and resources.Resource.weapon_empty_sound.play()
            return hit_list

        snake_body_hit_list = pg.sprite.spritecollide(self, self.game.level.snakes_body_pieces, False)
        for sprite in snake_body_hit_list:
            if sprite.snake.target_of_spells_count[magic_attack_cls.__name__] >= magic_attack_cls.max_spells_on_target:
                continue
            self.game.player.power -= magic_attack_cls.power_consumption[magic_attack_cls.actor_type.name]
            magic_attack = magic_attack_cls(
                        sprite.rect.centerx, sprite.rect.y, self.game,
                        is_from_player_shot=True, owner=self.game.player,
                        target=sprite.snake)
            hit_list.append(magic_attack)
            self.game.level.magic_sprites.add(magic_attack)
            sprite.snake.target_of_spells_count[magic_attack_cls.__name__] += 1
            break

        if snake_body_hit_list:
            return snake_body_hit_list

        dragon_body_hit_list = pg.sprite.spritecollide(self, self.game.level.dragons_body_pieces, False)
        for sprite in dragon_body_hit_list:
            if sprite.dragon.target_of_spells_count[magic_attack_cls.__name__] >= magic_attack_cls.max_spells_on_target:
                continue
            self.game.player.power -= magic_attack_cls.power_consumption[magic_attack_cls.actor_type.name]
            magic_attack = magic_attack_cls(
                        sprite.rect.centerx, sprite.rect.y, self.game,
                        is_from_player_shot=True, owner=self.game.player,
                        target=sprite.dragon)
            hit_list.append(magic_attack)
            self.game.level.magic_sprites.add(magic_attack)
            sprite.dragon.target_of_spells_count[magic_attack_cls.__name__] += 1
            break

        if dragon_body_hit_list:
            return dragon_body_hit_list

        hit_list = pg.sprite.spritecollide(self, self.game.level.npcs, False)
        for sprite in hit_list:
            if sprite.target_of_spells_count[magic_attack_cls.__name__] >= magic_attack_cls.max_spells_on_target:
                continue

            if self.game.level.spells_on_level_count[magic_attack_cls.__base__.__name__] >= magic_attack_cls.max_spells_on_level:
                continue

            self.game.player.power -= magic_attack_cls.power_consumption[magic_attack_cls.actor_type.name]
            magic_attack = magic_attack_cls(
                        sprite.rect.centerx, sprite.rect.y, self.game,
                        is_from_player_shot=True, owner=self.game.player,
                        target=sprite)
            self.game.level.magic_sprites.add(magic_attack)
            sprite.target_of_spells_count[magic_attack_cls.__name__] += 1
            self.game.level.spells_on_level_count[magic_attack_cls.__base__.__name__] += 1
            break

        return hit_list

    def selector_copy_actor(self, group):
        actors_hit = []
        if not self.game.is_log_debug or  self.player.direction == DIRECTION_RIP:
            return actors_hit

        if self.game.is_log_debug:
            hit_list = pg.sprite.spritecollide(self, group, False)
            for sprite in hit_list:
                if sprite.cannot_be_copied:
                    log.debug(f"Copy actor disabled for this type of actor: "
                              f"{sprite.type.name}")
                    continue
                actors_hit.append(sprite)

        if not actors_hit:
            return  None

        actor = actors_hit[0]
        log.debug(
            f"[COPY] Mouse actors: {actor.id} in pos: "
            f"({actor.rect.x}, {actor.rect.y}) - lev pos: "
            f"({actor.rect.x + self.game.level.get_scroll_shift_delta()}, "
            f"{actor.rect.y - self.game.level.get_scroll_shift_top_delta()})")
        self.sel_selected_actor_id = actor.id
        self.sel_selected_actor_level_id = self.game.level.id
        self.sel_selected_actor_pos = actor.rect.x, actor.rect.y
        self.sel_selected_actor_world_shift = self.game.level.world_shift
        self.sel_selected_actor_world_shift_top = self.game.level.world_shift_top
        return actor

    def selector_paste_actor(self):
        if (not self.sel_selected_actor_id
                or self.sel_selected_actor_level_id != self.game.level.id
                or not self.get_actor_if_exists(self.sel_selected_actor_id)):
            return

        world_shift = self.sel_selected_actor_world_shift - self.game.level.world_shift
        world_shift_top = self.sel_selected_actor_world_shift_top - self.game.level.world_shift_top
        dx = self.game.mouse_pos[0] - self.sel_selected_actor_pos[0] + world_shift
        dy = self.game.mouse_pos[1] - self.sel_selected_actor_pos[1] + world_shift_top

        self.copy_actor(
            self.sel_selected_actor_id, delta_x=dx, delta_y=dy,
            game=self.game)


class SelectorA(Selector):
    """Represents a selector of type A."""

    def __init__(self, x, y, game, name=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.SELECTOR_A
        super().__init__(x, y, game, name=name)
