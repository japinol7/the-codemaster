"""Module snakes."""
__author__ = 'Joan A. Pinol  (japinol)'

from collections import Counter

import pygame as pg

from codemaster.config.constants import (
    BM_SNAKES_FOLDER,
    )
import codemaster.config.constants as consts
from codemaster.models.actors.actor_types import ActorCategoryType, ActorBaseType, ActorType
from codemaster.models.actors.actors import NPC, Actor, NPC_STRENGTH_BASE
from codemaster.models.stats import Stats
from codemaster.tools.utils.colors import Color
from codemaster import resources

SNAKE_BODY_MAPPING = {
    ActorType.SNAKE_GREEN: ActorType.SNAKE_BODY_PART_G,
    ActorType.SNAKE_BLUE: ActorType.SNAKE_BODY_PART_B,
    ActorType.SNAKE_YELLOW: ActorType.SNAKE_BODY_PART_Y,
    ActorType.SNAKE_RED: ActorType.SNAKE_BODY_PART_R,
}


class SnakeBodyPiece(pg.sprite.Sprite):
    """Represents a body piece of a snake."""
    type_id_count = Counter()
    sprite_images = {}

    def __init__(self, snake, previous_body_piece, x, y):
        super().__init__()
        self.snake = snake
        self.previous_body_piece = previous_body_piece
        self.direction = consts.DIRECTION_RIGHT
        self.rect = False
        self.rect_old = False
        self.base_type = ActorBaseType.SNAKE_BODY_PART
        self.category_type = ActorCategoryType.SNAKE_BODY_PART
        self.type = SNAKE_BODY_MAPPING[snake.type]
        SnakeBodyPiece.type_id_count[self.type] += 1
        self.id = f"{self.type.name}_{SnakeBodyPiece.type_id_count[self.type]:05d}"

        # Snake's body piece
        if not SnakeBodyPiece.sprite_images.get(self.snake.color):
            snake_type_short = 'body'
            image_quality = '_md' if self.snake.cell_size >= consts.CELL_SIZE_MIN_FOR_IM_MD else ''
            image = pg.image.load(resources.file_name_get(folder=consts.BM_SNAKES_FOLDER,
                                                          name='im_snake_',
                                                          subname=snake_type_short,
                                                          quality=image_quality,
                                                          num=self.snake.color, subnum=1)).convert()
            image = pg.transform.smoothscale(image, (self.snake.cell_size, self.snake.cell_size))
            image.set_colorkey(Color.BLACK)
            self.image = image
            SnakeBodyPiece.sprite_images[self.snake.color] = self.image
        else:
            self.image = SnakeBodyPiece.sprite_images[self.snake.color]

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect_old = self.image.get_rect()
        self.rect_old.x = self.rect.x
        self.rect_old.y = self.rect.y

    def update(self):
        self.rect_old.x = self.rect.x
        self.rect_old.y = self.rect.y
        self.direction_old = self.direction
        self.rect.x = self.previous_body_piece.rect_old.x
        self.rect.y = self.previous_body_piece.rect_old.y
        self.direction = self.previous_body_piece.direction


class Snake(NPC):
    """Represents a snake.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_folder = BM_SNAKES_FOLDER
        self.file_name_key = ''
        self.images_sprite_no = 1
        self.cell_size = 14
        self.body_pieces = []
        self.rect_old = None
        self.direction_old = None
        self.is_a_snake = True
        super().__init__(x, y, game, name, change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)
        self.category_type = ActorCategoryType.SNAKE

    def _load_sprites(self):
        if not Actor.sprite_images.get(self.type.name):
            walking_frames_l = []
            walking_frames_r = []
            walking_frames_u = []
            walking_frames_d = []
            walking_frames_u_l = []
            walking_frames_u_r = []
            walking_frames_d_l = []
            walking_frames_d_r = []
            image = None
            for i in range(self.images_sprite_no):
                image = pg.image.load(self.file_name_im_get(
                    self.file_folder, 'im_snake_head',
                    self.file_mid_prefix, suffix_index=i+1
                )).convert()
                image.set_colorkey(Color.BLACK)
                walking_frames_r.append(image)

                image_l = pg.transform.flip(image, True, False)
                image_l.set_colorkey(Color.BLACK)
                walking_frames_l.append(image_l)

                image_u = pg.transform.rotate(image, 90)
                image_u.set_colorkey(Color.BLACK)
                walking_frames_u.append(image_u)

                image_d = pg.transform.rotate(image, -90)
                image_d.set_colorkey(Color.BLACK)
                walking_frames_d.append(image_d)

                image_u_r = pg.image.load(self.file_name_im_get(
                    self.file_folder, 'im_snake_head_u_r',
                    self.file_mid_prefix, suffix_index=i+1
                )).convert()
                image_u_r.set_colorkey(Color.BLACK)
                walking_frames_u_r.append(image_u_r)

                image_u_l = pg.transform.flip(image_u_r, True, False)
                image_u_l.set_colorkey(Color.BLACK)
                walking_frames_u_l.append(image_u_l)

                image_d_r = pg.image.load(self.file_name_im_get(
                    self.file_folder, 'im_snake_head_d_r',
                    self.file_mid_prefix, suffix_index=i+1
                )).convert()
                image_d_r.set_colorkey(Color.BLACK)
                walking_frames_d_r.append(image_d_r)

                image_d_l = pg.transform.flip(image_d_r, True, False)
                image_d_l.set_colorkey(Color.BLACK)
                walking_frames_d_l.append(image_d_l)

            Actor.sprite_images[self.type.name] = (image, walking_frames_l, walking_frames_r,
                                                   walking_frames_u, walking_frames_d,
                                                   walking_frames_u_l, walking_frames_u_r,
                                                   walking_frames_d_l, walking_frames_d_r)
            self.image = walking_frames_l[0]
        else:
            self.image = Actor.sprite_images[self.type.name][0]

    def init_after_load_sprites_hook(self):
        self.rect_old = self.image.get_rect()
        self.rect_old.x = self.rect.x
        self.rect_old.y = self.rect.y
        self.change_x += self.cell_size // 2.6
        self.change_y += self.cell_size // 2.6

        # Snake's body and tail
        previous_body_piece = self
        for i in range(self.body_length):
            self.body_pieces.append(
                SnakeBodyPiece(snake=self, previous_body_piece=previous_body_piece,
                               x=self.rect.x-((i+1)*self.cell_size), y=self.rect.y))
            previous_body_piece = self.body_pieces[i]

    def update(self):
        # Previous position. It will be used for the first piece of the body
        self.rect_old.x = self.rect.x
        self.rect_old.y = self.rect.y
        self.direction_old = self.direction

        if self.direction_old == self.direction and self.game.current_time % self.direction_stability == 0:
            self.change_y *= -1

        # When a snake hit a player energy shield it changes its x direction
        if self.player.is_energy_shield_activated and self.direction_old == self.direction:
            energy_shield_hit_list = pg.sprite.spritecollide(
                self,
                self.player.stats['energy_shields_stock'] or [],
                False)
            for shield in energy_shield_hit_list:
                if shield.direction == consts.DIRECTION_RIGHT and shield.is_actor_on_the_left(self):
                    self.change_x *= -1
                    shield.stats.health -= 2
                elif shield.direction == consts.DIRECTION_LEFT and shield.is_actor_on_the_right(self):
                    self.change_x *= -1
                    shield.stats.health -= 2

        super().update()

    def update_sprite_image(self):
        if self.change_y >= 1:
            if -0.8 < self.change_x < 0.8:
                self.image = Actor.sprite_images[self.type.name][consts.DIRECTION_DOWN][int(self.frame_index)]
            elif self.change_x >= 1:
                self.image = Actor.sprite_images[self.type.name][consts.DIRECTION_DOWN_RIGHT][int(self.frame_index)]
            elif self.change_x <= -1:
                self.image = Actor.sprite_images[self.type.name][consts.DIRECTION_DOWN_LEFT][int(self.frame_index)]
        elif self.change_y <= -1:
            if -0.8 < self.change_x < 0.8:
                self.image = Actor.sprite_images[self.type.name][consts.DIRECTION_UP][int(self.frame_index)]
            elif self.change_x >= 1:
                self.image = Actor.sprite_images[self.type.name][consts.DIRECTION_UP_RIGHT][int(self.frame_index)]
            elif self.change_x <= -1:
                self.image = Actor.sprite_images[self.type.name][consts.DIRECTION_UP_LEFT][int(self.frame_index)]
        else:
            self.image = Actor.sprite_images[self.type.name][self.direction][int(self.frame_index)]

    def kill_hook(self):
        for item in self.body_pieces:
            item.kill()
        super().kill_hook()

    def add_body_piece(self):
        snake_body_piece = SnakeBodyPiece(
            snake=self, previous_body_piece=self.body_pieces[self.body_length-1],
            x=self.body_pieces[self.body_length-1].previous_body_piece.rect_old.x,
            y=self.body_pieces[self.body_length-1].previous_body_piece.rect_old.y)
        self.body_pieces.append(snake_body_piece)
        self.body_length += 1


class SnakeGreen(Snake):
    """Represents a green snake."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '01'
        self.color = 1
        self.type = ActorType.SNAKE_GREEN
        self.body_len_start = self.body_length = 32
        self.direction_stability = 46
        self.stats = Stats()
        self.stats.power = self.stats.power_total = 5
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 1.4
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name, change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)


class SnakeBlue(Snake):
    """Represents a blue snake."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '03'
        self.color = 3
        self.type = ActorType.SNAKE_BLUE
        self.body_len_start = self.body_length = 40
        self.direction_stability = 40
        self.stats = Stats()
        self.stats.power = self.stats.power_total = 10
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 5
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name, change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)


class SnakeYellow(Snake):
    """Represents a yellow snake."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '02'
        self.color = 2
        self.type = ActorType.SNAKE_YELLOW
        self.body_len_start = self.body_length = 64
        self.direction_stability = 32
        self.stats = Stats()
        self.stats.power = self.stats.power_total = 5
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 17
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name, change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)


class SnakeRed(Snake):
    """Represents a red snake."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '04'
        self.color = 4
        self.type = ActorType.SNAKE_RED
        self.body_len_start = self.body_length = 92
        self.direction_stability = 30
        self.stats = Stats()
        self.stats.power = self.stats.power_total = 16
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 18
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name, change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)
