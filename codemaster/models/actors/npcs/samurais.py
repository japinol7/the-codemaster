"""Module samurais."""
__author__ = 'Joan A. Pinol  (japinol)'

from random import randint

from codemaster.config.constants import (
    DIRECTION_LEFT,
    BM_NPCS_FOLDER,
    )
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.actors import NPC, NPC_STRENGTH_BASE
from codemaster.models.actors.items.bullets import BulletType
from codemaster.models.actors.spells import SamutrinosBoltA, SamutrinosBoltB
from codemaster.models.stats import Stats


class Samurai(NPC):
    """Represents a samurai.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_folder = BM_NPCS_FOLDER
        self.file_name_key = 'im_en_samurais'
        self.images_sprite_no = 1
        self.can_shot = True
        self.can_cast_spells = True
        self.bullet_start_position_delta_x = 14
        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)

        self.hostility_level = 1
        self.spell_cast_x_delta_max = self.spell_cast_x_delta_max * 1.6
        self.spell_cast_y_delta_max = self.spell_cast_y_delta_max * 1.6

        self.probability_to_cast_samutrinos_bolt_a = 6

    def update_cast_spell_cast_actions(self):
        dice_shot = randint(1, 100)
        if all((
            dice_shot + self.probability_to_cast_samutrinos_bolt_a >= 100,
            sum(1 for x in self.game.level.magic_sprites
                if x.target == self.player and x.type.name == ActorType.FIRE_BREATH_A.name) < 1,
        )):
            spell_class = SamutrinosBoltA
        elif sum(1 for x in self.game.level.magic_sprites
                 if x.target == self.player and x.type.name == ActorType.FIRE_BREATH_B.name) < 3:
            spell_class = SamutrinosBoltB
        else:
            return

        delta_x = -10 if self.direction == DIRECTION_LEFT else 20
        magic_attack = spell_class(
            self.rect.x+delta_x, self.rect.y+15, self.game,
            is_from_player_shot=False, owner=self,
            target=self.player)
        self.game.level.magic_sprites.add(magic_attack)
        self.player.target_of_spells_count[spell_class.__name__] += 1
        self.game.level.spells_on_level_count[spell_class.__base__.__name__] += 1


class SamuraiMale(Samurai):
    """Represents a classic male samurai."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.SAMURAI_MALE

        self.stats = Stats()
        self.stats.power = self.stats.power_total = 10
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 9
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)

        self.stats.time_between_shots = self.time_between_shots_base / 3.7
        self.shot_x_delta_max = self.shot_x_delta_max + 240

        self.stats.time_between_spell_casting = 1800
        self.magic_resistance = 28
        self.probability_to_cast_samutrinos_bolt_a = 8
        self.max_multi_samutrinos_bolt_a = 1
        self.max_multi_samutrinos_bolt_b = 2

    def update_shot_bullet_fire_shots(self):
        dice = randint(1, 100)
        if dice + 40 >= 100:
            self.shot_bullet(BulletType.T2_LASER2)
        else:
            self.shot_bullet(BulletType.T1_LASER1)