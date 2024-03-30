"""Module bullets."""
__author__ = 'Joan A. Pinol  (japinol)'

import math
from collections import Counter
from enum import Enum
from random import randint

import pygame as pg

from codemaster.models.actors.actor_types import ActorType, ActorCategoryType
from codemaster.tools.utils.colors import Color
from codemaster.config import constants as consts
from codemaster.tools.utils import utils
from codemaster import resources
from codemaster.config.settings import Settings
from codemaster.config.constants import DIRECTION_RIP
from codemaster.tools.logger.logger import log


BULLET_STD_WIDTH = 12
BULLET_STD_HEIGHT = 17
BULLET_STD_RANGE = 375
BULLET_STD_VELOCITY = 15
BULLET_POWER_BASE = 5
BULLET_MAX_QTY = 499
BULLET_BOUNDARY_EXTEND_MULT = 1.6


BULLET_TYPE_01_ID = 1
BULLET_TYPE_02_ID = 2
BULLET_TYPE_03_ID = 3
BULLET_TYPE_04_ID = 4


# bullet types  (X, Y, width, height, id, power_min_to_use, power_consumption) of sprite
BULLET_TYPE_01 = (0, 0, BULLET_STD_WIDTH, BULLET_STD_HEIGHT,  BULLET_TYPE_01_ID, 1, 0.2)
BULLET_TYPE_02 = (0, 0, BULLET_STD_WIDTH, BULLET_STD_HEIGHT,  BULLET_TYPE_02_ID, 10, 0.5)
BULLET_TYPE_03 = (0, 0, 15, 21,  BULLET_TYPE_03_ID, 20, 2)
BULLET_TYPE_04 = (0, 0, 15, 21,  BULLET_TYPE_04_ID, 35, 6)


class BulletType(Enum):
    """Bullet types."""
    T1_LASER1 = 'bullets_t01'
    T2_LASER2 = 'bullets_t02'
    T3_PHOTONIC = 'bullets_t03'
    T4_NEUTRONIC = 'bullets_t04'


class Bullet(pg.sprite.Sprite):
    """Represents a bullet."""
    actor_type = ActorType.BULLET
    cell_added_size = utils.Size(w=-1, h=-1)     # Added size to the defined cell size.
    cell_size_multiplier = 1
    cell_size_ratio = 1
    size = None
    sprite_images = {}
    power_min_to_use = {BulletType.T1_LASER1.name: 1,
                        BulletType.T2_LASER2.name: 10,
                        BulletType.T3_PHOTONIC.name: 20,
                        BulletType.T4_NEUTRONIC.name: 35,
                        }
    power_consumption = {BulletType.T1_LASER1.name: 0.2,
                         BulletType.T2_LASER2.name: 0.5,
                         BulletType.T3_PHOTONIC.name: 3,
                         BulletType.T4_NEUTRONIC.name: 7,
                         }
    type_id_count = Counter()

    def __init__(self, x, y, bullet_type, game, owner, change_x=0, change_y=0):
        super().__init__()
        self.level = game.level
        self.images_sprite_no = 1
        self.frame = randint(0, self.images_sprite_no - 1)
        self.rect = None
        self.game = game
        self.owner = owner
        self.category_type = ActorCategoryType.BULLET
        self.type = self.bullet_type = bullet_type
        self.id_key = f"{self.bullet_type}_f_{self.owner.id}"
        Bullet.type_id_count[self.id_key] += 1
        if Bullet.type_id_count[self.id_key] > 999999:
            Bullet.type_id_count[self.id_key] = 1
        self.id = f"{self.type.name}_{Bullet.type_id_count[self.id_key]:07d}_from_{self.owner.id}"
        self.is_a_player_shot = False
        self.bullet_type_txt = None
        self.health_total = 100
        self.health = self.health_total
        self.attack_power = None
        self.bullet_range = BULLET_STD_RANGE
        self.border_left = None
        self.border_right = None
        self.border_top = None
        self.border_down = None
        self.change_x = change_x
        self.change_y = change_y
        self.direction = None
        self.animate_timer = self.game.current_time
        self.bullet_sound = None

        self.bullet_type_txt = self.bullet_type.value
        if self.bullet_type.name == BulletType.T1_LASER1.name:
            bullet_type_short = 't1'
            self.attack_power = BULLET_POWER_BASE
            self.bullet_range = int(self.bullet_range * 1.6)
            self.bullet_sound = resources.Resource.bullet_t1_sound
        elif self.bullet_type.name == BulletType.T2_LASER2.name:
            bullet_type_short = 't2'
            self.attack_power = BULLET_POWER_BASE * 1.4
            self.bullet_range = int(self.bullet_range * 1.4)
            self.bullet_sound = resources.Resource.bullet_t2_sound
        elif self.bullet_type.name == BulletType.T3_PHOTONIC.name:
            bullet_type_short = 't3'
            self.attack_power = BULLET_POWER_BASE * 4
            self.bullet_sound = resources.Resource.bullet_t3_sound
        elif self.bullet_type.name == BulletType.T4_NEUTRONIC.name:
            bullet_type_short = 't4'
            self.attack_power = BULLET_POWER_BASE * 8
            self.bullet_range = int(self.bullet_range * 1.3)
            self.bullet_sound = resources.Resource.bullet_t4_sound

        if not Bullet.sprite_images.get((self.bullet_type, consts.DIRECTION_RIGHT)):
            self.__class__.init()
            image_quality = '_md' if Settings.cell_size >= consts.CELL_SIZE_MIN_FOR_IM_MD else ''

            image = pg.image.load(resources.file_name_get(folder=consts.BM_BULLETS_FOLDER,
                                                          name='im_bullet_', subname=bullet_type_short,
                                                          quality=image_quality, num=1)).convert()
            image = pg.transform.smoothscale(image, Bullet.size)
            image.set_colorkey(Color.BLACK)
            Bullet.sprite_images[(self.bullet_type, consts.DIRECTION_RIGHT)] = image

            image = pg.image.load(resources.file_name_get(folder=consts.BM_BULLETS_FOLDER,
                                                          name='im_bullet_', subname=bullet_type_short,
                                                          quality=image_quality, num=1)).convert()
            image = pg.transform.flip(image, True, False)
            image = pg.transform.smoothscale(image, Bullet.size)
            image.set_colorkey(Color.BLACK)
            Bullet.sprite_images[(self.bullet_type, consts.DIRECTION_LEFT)] = image

            image = pg.image.load(resources.file_name_get(folder=consts.BM_BULLETS_FOLDER,
                                                          name='im_bullet_', subname=bullet_type_short,
                                                          quality=image_quality, num=1)).convert()
            image = pg.transform.rotate(image, 90)
            image = pg.transform.smoothscale(image, Bullet.size)
            image.set_colorkey(Color.BLACK)
            Bullet.sprite_images[(self.bullet_type, consts.DIRECTION_UP)] = image

            image = pg.image.load(resources.file_name_get(folder=consts.BM_BULLETS_FOLDER,
                                                          name='im_bullet_', subname=bullet_type_short,
                                                          quality=image_quality, num=1)).convert()
            image = pg.transform.rotate(image, 270)
            image = pg.transform.smoothscale(image, Bullet.size)
            image.set_colorkey(Color.BLACK)
            Bullet.sprite_images[(self.bullet_type, consts.DIRECTION_DOWN)] = image

        self.image = Bullet.sprite_images[(self.bullet_type, consts.DIRECTION_RIGHT)]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        if self.owner.direction == consts.DIRECTION_LEFT:
            self.direction = consts.DIRECTION_LEFT
            self.change_x *= -1
            self.rect.x -= owner.rect.w // 5
            self.rect.x -= owner.bullet_start_position_delta_x
        else:
            self.direction = consts.DIRECTION_RIGHT
            self.rect.x += (owner.rect.w + 1)
            self.rect.x += owner.bullet_start_position_delta_x

        self.rect.y += owner.rect.w // 1.5 + (
                not change_x and ((owner.rect.h + 1) * int(change_y / math.fabs(change_y))) or 0)

        self.initialize_boundaries()

        self.is_a_player_shot = self.owner.__getattribute__('is_a_player')

        # Add a bullet to the active sprite list
        self.level.bullets.add(self)
        self.level.all_sprites.add(self)

        if self.is_a_player_shot and self.game.sound_effects:
            self.bullet_sound.play()

    def initialize_boundaries(self):
        self.border_left = self.rect.x - self.level.world_shift - self.owner.rect.width - self.bullet_range
        self.border_right = self.rect.x - self.level.world_shift + self.owner.rect.width + self.bullet_range
        self.border_top = self.rect.y + self.owner.rect.height // 2
        self.border_down = self.border_top

    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        self.image = Bullet.sprite_images[(self.bullet_type, self.direction)]

        # Check boundaries and see if we need to kill the bullet
        cur_pos = self.rect.x - self.level.world_shift
        if self.change_x < 0 and cur_pos < self.border_left:
            self.kill()
        if self.change_x >= 0 and cur_pos > self.border_right:
            self.kill()

        if Settings.are_bullets_allowed_to_collide:
            # Check if it hit any other bullet, not considering bullets from the same player
            # or bullets from the same type of actor
            bullet_hit_list = pg.sprite.spritecollide(self, self.level.bullets, False)
            for bullet in bullet_hit_list:
                if bullet is not self and bullet.owner.type.name != self.owner.type.name:
                    self.game.sound_effects and resources.Resource.bullet_hit_sound.play()
                    self.kill()
                    bullet.kill()

        # Check if we hit any player
        players_hit_list = pg.sprite.spritecollide(self, self.game.players, False)
        for pc in players_hit_list:
            if pc.direction == DIRECTION_RIP or pc.invulnerable:
                continue
            self.game.is_log_debug and log.debug(
                f"{pc.id} hit by {self.id}, pc_health: {str(round(pc.stats['health'], 2))}, "
                f"bullet_power: {str(self.attack_power)}")
            pc.stats['health'] -= self.attack_power
            self.kill()
            if pc.stats['health'] <= 0:
                self.game.is_log_debug and log.debug(f"{pc.id}, !!! Dead by bullet {self.id} !!!")
                pc.die_hard()
            self.kill()

    @classmethod
    def init(cls):
        cls.size = utils.Size(
            w=int(Settings.cell_size * Bullet.cell_size_ratio
                  * Bullet.cell_size_multiplier + cls.cell_added_size.w),
            h=int(Settings.cell_size * Bullet.cell_size_multiplier
                  + cls.cell_added_size.h))

    @classmethod
    def shot(cls, bullet_type, change_x, change_y, owner, game):
        if bullet_type == BulletType.T1_LASER1:
            game.sound_effects and resources.Resource.bullet_t1_sound.play()
        elif bullet_type == BulletType.T2_LASER2:
            game.sound_effects and resources.Resource.bullet_t2_sound.play()
        elif bullet_type == BulletType.T3_PHOTONIC:
            game.sound_effects and resources.Resource.bullet_t3_sound.play()
        elif bullet_type == BulletType.T4_NEUTRONIC:
            game.sound_effects and resources.Resource.bullet_t4_sound.play()

        Bullet(x=owner.rect.x, y=owner.rect.y,
               bullet_type=bullet_type, game=game, change_x=change_x,
               change_y=not change_x and change_y or 0, owner=owner)
