"""Module energy shields."""
__author__ = 'Joan A. Pinol  (japinol)'

from random import randint

import pygame as pg

from codemaster.config.constants import (
    BM_ENERGY_SHIELD_FOLDER,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
    )
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import Actor, ActorItem
from codemaster.models.stats import Stats


class EnergyShield(ActorItem):
    """Represents an energy shield.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None,
                 random_min=0, random_max=0):
        self.images_sprite_no = 2
        self.category_type = ActorCategoryType.ENERGY_SHIELD
        self.owner_stats_key = 'energy_shields_stock'
        self.transparency_alpha = True
        self.stats = Stats()
        self.random_min = random_min
        self.random_max = random_max
        self.stats.strength = self.stats.strength_total = 1
        self.calculate_power()
        self.can_move = True

        super().__init__(x, y, game, name=name)

        self.is_activated = False
        self.can_be_shot_by_its_owner = False

    def _load_sprites(self):
        if not Actor.sprite_images.get(self.type.name):
            walking_frames_l = []
            walking_frames_r = []
            walking_frames_l_low = []
            walking_frames_r_low = []
            walking_frames_l_medium = []
            walking_frames_r_medium = []
            image = None
            for i in range(self.images_sprite_no):
                image = pg.image.load(self.file_name_im_get(
                            self.file_folder, self.file_name_key,
                            self.file_mid_prefix, suffix_index=i + 1
                            )).convert_alpha()
                walking_frames_r.append(image)

                image_l = pg.transform.flip(image, True, False)
                walking_frames_l.append(image_l)

                image = pg.image.load(self.file_name_im_get(
                            self.file_folder, self.file_name_key,
                            f"{self.file_mid_prefix}_low" , suffix_index=i + 1
                            )).convert_alpha()
                walking_frames_r_low.append(image)

                image_l = pg.transform.flip(image, True, False)
                walking_frames_l_low.append(image_l)

                image = pg.image.load(self.file_name_im_get(
                            self.file_folder, self.file_name_key,
                            f"{self.file_mid_prefix}_medium" , suffix_index=i + 1
                            )).convert_alpha()
                walking_frames_r_medium.append(image)

                image_l = pg.transform.flip(image, True, False)
                walking_frames_l_medium.append(image_l)

            Actor.sprite_images[self.type.name] = (image, walking_frames_l, walking_frames_r,
                                                   walking_frames_l_low, walking_frames_r_low,
                                                   walking_frames_l_medium, walking_frames_r_medium)
            self.image = walking_frames_l[0]
        else:
            self.image = Actor.sprite_images[self.type.name][0]

    def update(self):
        self.rect.y = self.player.rect.y - 8
        self.direction = DIRECTION_LEFT if self.player.direction == DIRECTION_LEFT else DIRECTION_RIGHT
        if self.player.direction == DIRECTION_RIGHT:
            self.rect.x = self.player.rect.x + self.rect.w + 22
        elif self.player.direction == DIRECTION_LEFT:
            self.rect.x = self.player.rect.x - self.rect.w - 8

        if self.is_activated and self.owner == self.player:
            self.owner.stats['power'] -= self.power_cost
            if self.owner.stats['power'] <= 0:
                self.deactivate()

        super().update()

    def update_sprite_image(self):
        image_direction = self.direction
        if self.stats.health < self.stats.health_total // 3.6:
            image_direction = 3 if self.direction == DIRECTION_LEFT else 4
        elif self.stats.health < self.stats.health_total // 1.9:
            image_direction = 5 if self.direction == DIRECTION_LEFT else 6
        self.image = Actor.sprite_images[self.type.name][image_direction][int(self.frame_index)]

    def calculate_power(self):
        if self.random_min == 0 and self.random_max == 0:
            if randint(1, 100) > 85:
                self.stats.power = randint(32, 85)
            else:
                self.stats.power = randint(25, 40)
            self.stats.power_total = self.stats.power
            return
        self.stats.power = randint(self.random_min, self.random_max)
        self.stats.power_total = self.stats.power

    def kill_hook(self):
        self.player.stats['power'] -= self.power_killed_cost
        self.deactivate()
        super().kill_hook()

    def activate(self):
        self.is_activated = True
        self.owner.is_energy_shield_activated = True
        if self.stats.health < 0:
            self.stats.health = self.stats.health_total
        self.game.active_sprites.add(self)

    def deactivate(self):
        self.is_activated = False
        self.owner.is_energy_shield_activated = False
        self.game.active_sprites.remove(self)


class EnergyShieldA(EnergyShield):
    """Represents an energy shield of type A."""

    def __init__(self, x, y, game, name=None,
                 random_min=0, random_max=0):
        self.file_folder = BM_ENERGY_SHIELD_FOLDER
        self.file_name_key = 'im_energy_shields'
        self.file_mid_prefix = 't1_01'
        self.type = ActorType.ENERGY_SHIELD_A
        self.owner_stats_key = 'energy_shield_a'

        super().__init__(x, y, game, name=name,
                         random_min=random_min, random_max=random_max)

        self.power_cost = 0.02
        self.power_killed_cost = 12
        self.stats.health = self.stats.health_total = 150
        self.stats.strength = self.stats.strength_total = 1
