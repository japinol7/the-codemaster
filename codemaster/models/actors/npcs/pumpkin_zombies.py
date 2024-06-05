"""Module pumpkin_zombies."""
__author__ = 'Joan A. Pinol  (japinol)'

from random import randint

from codemaster.config.constants import (
    BM_NPCS_FOLDER,
    DIRECTION_LEFT,
    )
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.actors import NPC, NPC_STRENGTH_BASE
from codemaster.models.actors.spells import DrainLifeA, DrainLifeB
from codemaster.models.stats import Stats


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
        self.spell_cast_x_delta_max = self.spell_cast_x_delta_max * 1.1
        self.spell_cast_y_delta_max = self.spell_cast_y_delta_max

    def update_cast_spell_cast_actions(self):
        probability_to_cast_spell_a = 13
        dice_shot = randint(1, 100)
        if dice_shot + probability_to_cast_spell_a >= 100:
            spell_class = DrainLifeA
        else:
            spell_class = DrainLifeB

        delta_x = -20 if self.direction == DIRECTION_LEFT else 40
        magic_attack = spell_class(
            self.rect.x+delta_x, self.rect.y-10, self.game,
            is_from_player_shot=False, owner=self,
            target=self.player)
        self.game.level.magic_sprites.add(magic_attack)
        self.player.target_of_spells_count[spell_class.__name__] += 1
        self.game.level.spells_on_level_count[spell_class.__base__.__name__] += 1
