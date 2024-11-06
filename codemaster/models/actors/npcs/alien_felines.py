"""Module alien_felines."""
__author__ = 'Joan A. Pinol  (japinol)'

from random import randint

from codemaster.config.constants import BM_NPCS_FOLDER
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.items.bullets import BulletType
from codemaster.models.actors.actors import NPC, NPC_STRENGTH_BASE
from codemaster.models.stats import Stats
from codemaster.models.actors import magic


class AlienFeline(NPC):
    """Represents an alien feline.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_folder = BM_NPCS_FOLDER
        self.file_name_key = 'im_en_alien_felines'
        self.images_sprite_no = 1
        self.transparency_alpha = True
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
        self.spell_1_name = ActorType.MUTENTRINOS_BOLT_A.name
        self.spell_2_name = ActorType.FIRE_BREATH_A.name
        self.spell_3_name = ActorType.FIRE_BREATH_B.name
        self.probability_to_cast_spell_1 = 5
        self.probability_to_cast_spell_2 = 10
        self.probability_to_cast_spell_3 = 100
        self.max_multi_spell_1 = 1
        self.max_multi_spell_2 = 2
        self.max_multi_spell_3 = 3

    def update_cast_spell_cast_actions(self):
        magic.update_cast_spell_cast_actions_3_spells(actor=self)


class AlienFelineMale(AlienFeline):
    """Represents a male alien feline."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.ALIEN_FELINE_MALE

        self.stats = Stats()
        self.stats.power = self.stats.power_total = 10
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 10
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)

        self.stats.time_between_shots = self.time_between_shots_base / 2
        self.shot_x_delta_max = self.shot_x_delta_max + 170

        self.stats.time_between_spell_casting = 1200
        self.magic_resistance = 90

    def update_shot_bullet_fire_shots(self):
        dice = randint(1, 100)
        if dice + 25 >= 100:
            self.shot_bullet(BulletType.T3_PHOTONIC)
        else:
            self.shot_bullet(BulletType.T2_LASER2)
