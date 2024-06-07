"""Module pumpkin_zombies."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import BM_NPCS_FOLDER
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.actors import NPC, NPC_STRENGTH_BASE
from codemaster.models.stats import Stats
from codemaster.models.actors import magic


class PumpkinZombie(NPC):
    """Represents a pumpkin zombie.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_folder = BM_NPCS_FOLDER
        self.file_name_key = 'im_en_pumpkin_zombies'
        self.images_sprite_no = 1
        self.can_cast_spells = True

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)

        self.spell_cast_x_delta_max = self.spell_cast_x_delta_max * 1.1
        self.spell_cast_y_delta_max = self.spell_cast_y_delta_max
        self.spell_1_name = ActorType.DRAIN_LIFE_A.name
        self.spell_2_name = ActorType.DRAIN_LIFE_B.name
        self.probability_to_cast_spell_1 = 13
        self.probability_to_cast_spell_2 = 100
        self.max_multi_spell_1 = 1
        self.max_multi_spell_2 = 2


class PumpkinZombieA(PumpkinZombie):
    """Represents a pumpkin zombie A."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.PUMPKIN_ZOMBIE_A

        self.stats = Stats()
        self.stats.power = self.stats.power_total = 4
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 7
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)

        self.magic_resistance = 100
        self.stats.time_between_spell_casting = 1000
        self.stats.time_between_energy_shield_casting = 1000

    def update_cast_spell_cast_actions(self):
        magic.update_cast_spell_cast_actions(actor=self)
