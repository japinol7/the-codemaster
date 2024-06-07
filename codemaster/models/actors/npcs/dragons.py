"""Module dragons."""
__author__ = 'Joan A. Pinol  (japinol)'

from collections import Counter

import pygame as pg

from codemaster.config.constants import (
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
    DIRECTION_DOWN_LEFT,
    DIRECTION_DOWN_RIGHT,
    DIRECTION_UP_LEFT,
    DIRECTION_UP_RIGHT,
    BM_DRAGONS_FOLDER,
    )
from codemaster.models.actors.actor_types import ActorCategoryType, ActorBaseType, ActorType
from codemaster.models.actors.actors import NPC, Actor, NPC_STRENGTH_BASE
from codemaster.models.stats import Stats
from codemaster.tools.utils.colors import Color
from codemaster import resources
from codemaster.models.actors import magic

DRAGON_BODY_MAPPING = {
    ActorType.DRAGON_GREEN: ActorType.DRAGON_BODY_PART_G,
    ActorType.DRAGON_BLUE: ActorType.DRAGON_BODY_PART_B,
    ActorType.DRAGON_YELLOW: ActorType.DRAGON_BODY_PART_Y,
    ActorType.DRAGON_RED: ActorType.DRAGON_BODY_PART_R,
    }


class DragonBodyPiece(pg.sprite.Sprite):
    """Represents a body piece of a dragon."""
    type_id_count = Counter()
    sprite_images = {}

    def __init__(self, dragon, previous_body_piece, x, y):
        super().__init__()
        self.dragon = dragon
        self.previous_body_piece = previous_body_piece
        self.direction = DIRECTION_RIGHT
        self.rect = False
        self.rect_old = False
        self.base_type = ActorBaseType.DRAGON_BODY_PART
        self.category_type = ActorCategoryType.DRAGON_BODY_PART
        self.type = DRAGON_BODY_MAPPING[dragon.type]
        DragonBodyPiece.type_id_count[self.type] += 1
        self.id = f"{self.type.name}_{DragonBodyPiece.type_id_count[self.type]:05d}"

        # Dragon's body piece
        if not DragonBodyPiece.sprite_images.get(self.dragon.color):
            dragon_type_short = 'body'
            image = pg.image.load(resources.file_name_get(
                folder=BM_DRAGONS_FOLDER,
                name='im_dragon_',
                subname=dragon_type_short,
                num=self.dragon.color, subnum=1)).convert()
            image = pg.transform.smoothscale(image, (self.dragon.cell_size, self.dragon.cell_size))
            image.set_colorkey(Color.BLACK)
            self.image = image
            DragonBodyPiece.sprite_images[self.dragon.color] = self.image
        else:
            self.image = DragonBodyPiece.sprite_images[self.dragon.color]

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
        self.direction = self.previous_body_piece.direction_old


class Dragon(NPC):
    """Represents a dragon.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_folder = BM_DRAGONS_FOLDER
        self.file_name_key = ''
        self.images_sprite_no = 1
        self.cell_size = 36
        self.body_pieces = []
        self.rect_old = None
        self.direction_old = None
        self.direction_complete = None
        self.is_a_dragon = True
        self.can_cast_spells = True
        self.health_bar_delta_y = 50

        super().__init__(x, y, game, name, change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)

        self.category_type = ActorCategoryType.DRAGON
        self.image_head = None

        self.hostility_level = 1
        self.spell_cast_x_delta_max = self.spell_cast_x_delta_max * 1.6
        self.spell_cast_y_delta_max = self.spell_cast_y_delta_max * 1.6
        self.spell_1_name = ActorType.VORTEX_OF_DOOM_A.name
        self.spell_2_name = ActorType.FIRE_BREATH_A.name
        self.spell_3_name = ActorType.FIRE_BREATH_B.name
        self.probability_to_cast_spell_1 = 4
        self.probability_to_cast_spell_2 = 8
        self.probability_to_cast_spell_3 = 100
        self.max_multi_spell_1 = 1
        self.max_multi_spell_2 = 2
        self.max_multi_spell_3 = 4

    def _load_sprites(self):
        # We want to draw the dragon's head on top of the body,
        # for this reason, we make the usual actor image invisible
        self.image = pg.image.load(self.file_name_im_get(
            self.file_folder, 'im_dragon_head',
            mid_prefix='invisible', suffix_index=1
        )).convert()
        self.image.set_colorkey(Color.BLACK)

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
                    self.file_folder, 'im_dragon_head',
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

                image_u_r = pg.transform.rotate(image, 0)
                image_u_r.set_colorkey(Color.BLACK)
                walking_frames_u_r.append(image_u_r)

                image_u_l = pg.transform.flip(image_u_r, True, False)
                image_u_l.set_colorkey(Color.BLACK)
                walking_frames_u_l.append(image_u_l)

                image_d_r = pg.transform.rotate(image, -90)
                image_d_r.set_colorkey(Color.BLACK)
                walking_frames_d_r.append(image_d_r)

                image_d_l = pg.transform.flip(image_d_r, True, False)
                image_d_l.set_colorkey(Color.BLACK)
                walking_frames_d_l.append(image_d_l)

            Actor.sprite_images[self.type.name] = (image, walking_frames_l, walking_frames_r,
                                                   walking_frames_u, walking_frames_d,
                                                   walking_frames_u_l, walking_frames_u_r,
                                                   walking_frames_d_l, walking_frames_d_r)
            self.image_head = walking_frames_l[0]
        else:
            self.image_head = Actor.sprite_images[self.type.name][0]

    def init_after_load_sprites_hook(self):
        self.rect_old = self.image.get_rect()
        self.rect_old.x = self.rect.x
        self.rect_old.y = self.rect.y
        self.change_x += self.cell_size // 8
        self.change_y += self.cell_size // 8

        # Dragon's body and tail
        previous_body_piece = self
        for i in range(self.body_length):
            self.body_pieces.append(
                DragonBodyPiece(dragon=self, previous_body_piece=previous_body_piece,
                                x=self.rect.x-((i+1)*2), y=self.rect.y))
            previous_body_piece = self.body_pieces[i]

    def draw(self):
        # Draw dragon head at the right position
        x_delta = y_delta = 0
        if self.direction_complete == DIRECTION_DOWN_LEFT:
            x_delta = -54
            y_delta = +10
        elif self.direction_complete == DIRECTION_DOWN_RIGHT:
            x_delta = -10
        elif self.direction_complete == DIRECTION_UP_LEFT:
            x_delta = -62
            y_delta = -50
        elif self.direction_complete == DIRECTION_UP_RIGHT:
            x_delta = +10
            y_delta = -50
        self.game.screen.blit(self.image_head, (self.rect.x + x_delta, self.rect.y + y_delta))

    def update(self):
        # Previous position. It will be used for the first piece of the body
        self.rect_old.x = self.rect.x
        self.rect_old.y = self.rect.y
        self.direction_old = self.direction

        if self.direction_old == self.direction and self.game.current_time % self.direction_stability == 0:
            self.change_y *= -1

        # When a dragon hit a player energy shield, it changes its x direction
        if self.player.is_energy_shield_activated and self.direction_old == self.direction:
            energy_shield_hit_list = pg.sprite.spritecollide(
                self,
                self.player.stats['energy_shields_stock'] or [],
                False)
            for shield in energy_shield_hit_list:
                if shield.direction == DIRECTION_RIGHT and shield.is_actor_on_the_left(self):
                    self.change_x *= -1
                    shield.stats.health -= 2
                elif shield.direction == DIRECTION_LEFT and shield.is_actor_on_the_right(self):
                    self.change_x *= -1
                    shield.stats.health -= 2

        super().update()

    def update_sprite_image(self):
        is_player_to_the_left = self.is_actor_on_the_left(self.player)
        if not is_player_to_the_left:
            self.direction_complete = DIRECTION_UP_RIGHT
        else:
            self.direction_complete = DIRECTION_UP_LEFT

        self.image_head = Actor.sprite_images[self.type.name][self.direction_complete][int(self.frame_index)]

    def kill_hook(self):
        for item in self.body_pieces:
            item.kill()
        super().kill_hook()

    def add_body_piece(self):
        dragon_body_piece = DragonBodyPiece(
            dragon=self, previous_body_piece=self.body_pieces[self.body_length-1],
            x=self.body_pieces[self.body_length-1].previous_body_piece.rect_old.x,
            y=self.body_pieces[self.body_length-1].previous_body_piece.rect_old.y)
        self.body_pieces.append(dragon_body_piece)
        self.body_length += 1

    def update_cast_spell_cast_actions(self):
        magic.update_cast_spell_cast_actions_3_spells(actor=self)


class DragonGreen(Dragon):
    """Represents a green dragon."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '01'
        self.color = 1
        self.type = ActorType.DRAGON_GREEN
        self.body_len_start = self.body_length = 110
        self.direction_stability = 46
        self.stats = Stats()
        self.stats.power = self.stats.power_total = 7
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 8
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name, change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)

        self.stats.time_between_spell_casting = 1000
        self.magic_resistance = 130
        self.probability_to_cast_spell_1 = 0
        self.probability_to_cast_spell_2 = 9
        self.probability_to_cast_spell_3 = 100
        self.max_multi_spell_1 = 0
        self.max_multi_spell_2 = 1
        self.max_multi_spell_3 = 2


class DragonBlue(Dragon):
    """Represents a blue dragon."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '03'
        self.color = 3
        self.type = ActorType.DRAGON_BLUE
        self.body_len_start = self.body_length = 78
        self.direction_stability = 40
        self.stats = Stats()
        self.stats.power = self.stats.power_total = 10
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 10
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name, change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)

        self.stats.time_between_spell_casting = 1000
        self.magic_resistance = 156
        self.probability_to_cast_spell_1 = 6
        self.probability_to_cast_spell_2 = 13
        self.probability_to_cast_spell_3 = 100
        self.max_multi_spell_1 = 1
        self.max_multi_spell_2 = 1
        self.max_multi_spell_3 = 3


class DragonYellow(Dragon):
    """Represents a yellow dragon."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '02'
        self.color = 2
        self.type = ActorType.DRAGON_YELLOW
        self.body_len_start = self.body_length = 86
        self.direction_stability = 36
        self.stats = Stats()
        self.stats.power = self.stats.power_total = 15
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 19
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name, change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)

        self.stats.time_between_spell_casting = 900
        self.magic_resistance = 175
        self.probability_to_cast_spell_1 = 8
        self.probability_to_cast_spell_2 = 13
        self.probability_to_cast_spell_3 = 100
        self.max_multi_spell_1 = 1
        self.max_multi_spell_2 = 2
        self.max_multi_spell_3 = 3


class DragonRed(Dragon):
    """Represents a red dragon."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '04'
        self.color = 4
        self.type = ActorType.DRAGON_RED
        self.body_len_start = self.body_length = 98
        self.direction_stability = 33
        self.stats = Stats()
        self.stats.power = self.stats.power_total = 20
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 22
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name, change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)

        self.stats.time_between_spell_casting = 750
        self.magic_resistance = 194
        self.probability_to_cast_spell_1 = 10
        self.probability_to_cast_spell_2 = 16
        self.probability_to_cast_spell_3 = 100
        self.max_multi_spell_1 = 1
        self.max_multi_spell_2 = 2
        self.max_multi_spell_3 = 5
