"""Module pumpkin_heads."""
__author__ = 'Joan A. Pinol  (japinol)'

from random import randint

from codemaster.config.constants import (
    BM_NPCS_FOLDER,
    DIRECTION_LEFT,
    DIRECTION_RIP,
    )
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.actors import NPC, NPC_STRENGTH_BASE
from codemaster.models.actors.spells import (
    DrainLifeA,
    DrainLifeB,
    VortexOfDoomB
    )
from codemaster.models.stats import Stats


class PumpkinHead(NPC):
    """Represents a pumpkin head.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_folder = BM_NPCS_FOLDER
        self.file_name_key = 'im_en_pumpkin_heads'
        self.images_sprite_no = 1
        self.can_cast_spells = True

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)


class PumpkinHeadA(PumpkinHead):
    """Represents a pumpkin head A."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.PUMPKIN_HEAD_A

        self.stats = Stats()
        self.stats.power = self.stats.power_total = 4
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 6
        self.stats.health = self.stats.health_total = self.stats.strength

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)

        self.magic_resistance = 116
        self.stats.time_between_spell_casting = 1000
        self.stats.time_between_energy_shield_casting = 1000
        self.spell_cast_x_delta_max = self.spell_cast_x_delta_max * 1.1
        self.spell_cast_y_delta_max = self.spell_cast_y_delta_max
        self.probability_to_cast_vortex_b = 4
        self.probability_to_cast_drain_life_a = 8

    def update_cast_spell_cast_actions(self):
        dice_shot = randint(1, 100)
        if all((
            self.game.player.direction != DIRECTION_RIP,
            dice_shot + self.probability_to_cast_vortex_b >= 100,
            sum(1 for x in self.game.level.magic_sprites
                if x.target == self.player and x.type.name == ActorType.VORTEX_OF_DOOM_B.name) < 1,
        )):
            spell_class = VortexOfDoomB
        elif all((
            dice_shot + self.probability_to_cast_drain_life_a >= 100,
            sum(1 for x in self.game.level.magic_sprites
                if x.target == self.player and x.type.name == ActorType.FIRE_BREATH_A.name) < 1,
        )):
            spell_class = DrainLifeA
        elif sum(1 for x in self.game.level.magic_sprites
                 if x.target == self.player and x.type.name == ActorType.FIRE_BREATH_B.name) < 3:
            spell_class = DrainLifeB
        else:
            return

        delta_x = -10 if self.direction == DIRECTION_LEFT else 20
        magic_attack = spell_class(
            self.rect.x+delta_x, self.rect.y+12, self.game,
            is_from_player_shot=False, owner=self,
            target=self.player)
        self.game.level.magic_sprites.add(magic_attack)
        self.player.target_of_spells_count[spell_class.__name__] += 1
        self.game.level.spells_on_level_count[spell_class.__base__.__name__] += 1
