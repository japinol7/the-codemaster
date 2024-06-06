"""Module mage."""
__author__ = 'Joan A. Pinol  (japinol)'

from random import randint

import pygame as pg

from codemaster.config.constants import (
    BM_NPCS_FOLDER,
    MSG_NPC_DURATION_LONG,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
    DIRECTION_RIP,
    )
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.actors import NPC, NPC_STRENGTH_BASE
from codemaster.models.actors.spells import DrainLifeA, DrainLifeB, VortexOfDoomB
from codemaster.models.actors.items.energy_shields import EnergyShield
from codemaster.models.actors.text_msgs import TextMsg
from codemaster.models.stats import Stats


class Mage(NPC):
    """Represents a Mage.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_folder = BM_NPCS_FOLDER
        self.file_name_key = 'im_en_mages'
        self.images_sprite_no = 1
        self.can_cast_spells = True

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)

        self.probability_to_cast_vortex_b = 8
        self.probability_to_cast_spell_a = 13
        self.probability_to_cast_spell_b = 100


class MageFemaleA(Mage):
    """Represents a Mage Female A."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '02'
        self.type = ActorType.MAGE_FEMALE_A

        self.stats = Stats()
        self.stats.power = self.stats.power_total = NPC_STRENGTH_BASE
        self.stats.power_recovery = 10
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 7
        self.stats.health = self.stats.health_total = NPC_STRENGTH_BASE * 8
        self.msg_texts = [
            "Prepare to Die!",
            "I SAID:\nYou shall not pass!\nI am the guardian\nof the gate.",
            "Listen handsome...\nI will only say this\nonce more...",
            "You shall not pass!\nI am the guardian\nof the gate.",
            ]
        self.msg_text_to_repeat = "I SAID...\nYou shall not pass!\nI am the guardian\nof the gate.\nDie!"
        self.msgs_delta_max = 310, 310
        self.msgs = pg.sprite.Group()

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)

        self.magic_resistance = 150
        self.hostility_level = 0
        self.stats.time_between_spell_casting = 1000
        self.stats.time_between_energy_shield_casting = 1000
        self.spell_cast_x_delta_max = self.spell_cast_x_delta_max * 1.6
        self.spell_cast_y_delta_max = self.spell_cast_y_delta_max * 1.6

        EnergyShield.actor_acquire_energy_shield(self, self.game)

    def kill_hook(self):
        for msg in self.msgs:
            msg.kill()

        super().kill_hook()

    def update_after_inc_index_hook(self):
        self.direction = DIRECTION_LEFT if self.is_actor_on_the_left(self.player) else DIRECTION_RIGHT

        if self.msg_texts and not self.msgs:
            is_between_x_boundaries = (self.player.rect.x - self.msgs_delta_max[0] < self.rect.x
                                       < self.player.rect.x + self.msgs_delta_max[0])
            is_between_y_boundaries = (self.player.rect.y - self.msgs_delta_max[1] < self.rect.y
                                       < self.player.rect.y + self.msgs_delta_max[1])
            if is_between_x_boundaries and is_between_y_boundaries:
                msg = TextMsg.create(
                    self.msg_texts.pop(), self.game,
                    time_in_secs=MSG_NPC_DURATION_LONG,
                    delta_x=180, delta_y=34, owner=self)
                self.msgs.add([msg])

        if not self.msg_texts:
            self.hostility_level = 1
            self.stats.energy_shield.activate()
            self.msg_texts.append(self.msg_text_to_repeat)

        super().update_after_inc_index_hook()

    def update_cast_spell_cast_actions(self):
        dice_shot = randint(1, 100)
        if all([
            self.game.player.direction != DIRECTION_RIP,
            dice_shot + self.probability_to_cast_vortex_b > 100,
            sum(1 for x in self.game.level.magic_sprites
                if x.target == self.player and x.type.name == ActorType.VORTEX_OF_DOOM_B.name) < 1,
        ]):
            spell_class = VortexOfDoomB
        elif all([
            dice_shot + self.probability_to_cast_spell_a > 100,
            sum(1 for x in self.game.level.magic_sprites
                if x.target == self.player and x.type.name == ActorType.DRAIN_LIFE_A.name) < 1,
        ]):
            spell_class = DrainLifeA
        elif all([
            dice_shot + self.probability_to_cast_spell_b > 100,
            sum(1 for x in self.game.level.magic_sprites
                if x.target == self.player and x.type.name == ActorType.DRAIN_LIFE_B.name) < 1,
        ]):
            spell_class = DrainLifeB
        else:
            return

        delta_x = -20 if self.direction == DIRECTION_LEFT else 40
        magic_attack = spell_class(
            self.rect.x+delta_x, self.rect.y-10, self.game,
            is_from_player_shot=False, owner=self,
            target=self.player)
        self.game.level.magic_sprites.add(magic_attack)
        self.player.target_of_spells_count[spell_class.__name__] += 1
        self.game.level.spells_on_level_count[spell_class.__base__.__name__] += 1


class MageFemaleAVanished(Mage):
    """Represents a Mage Female A vanished."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '02_vanished'
        self.type = ActorType.MAGE_FEMALE_A_VANISHED

        self.stats = Stats()
        self.stats.power = self.stats.power_total = 0.01
        self.stats.power_recovery = 10
        self.stats.strength = self.stats.strength_total = NPC_STRENGTH_BASE * 7
        self.stats.health = self.stats.health_total = NPC_STRENGTH_BASE * 12
        self.msg_texts = [
            "You've vanished me!\nBut, I will return!\nYou.. Jerk!",
            ]
        self.msg_text_to_repeat = "I will return!"
        self.msgs_delta_max = 310, 310
        self.msgs = pg.sprite.Group()

        super().__init__(x, y, game, name=name,
                         change_x=change_x, change_y=change_y,
                         border_left=border_left, border_right=border_right,
                         border_top=border_top, border_down=border_down,
                         items_to_drop=items_to_drop)

        self.magic_resistance = 990
        self.hostility_level = 0
        self.stats.time_between_spell_casting = 10000
        self.stats.time_between_energy_shield_casting = 10000

    def update_when_hit(self):
        """Vanished mages cannot be hit with normal weapons.
        They are out of phase.
        Because of this, they cannot be killed with bullets.
        """
        pass

    def kill_hook(self):
        for msg in self.msgs:
            msg.kill()

        super().kill_hook()

    def update_after_inc_index_hook(self):
        self.direction = DIRECTION_LEFT if self.is_actor_on_the_left(self.player) else DIRECTION_RIGHT

        if self.msg_texts and not self.msgs:
            is_between_x_boundaries = (self.player.rect.x - self.msgs_delta_max[0] < self.rect.x
                                       < self.player.rect.x + self.msgs_delta_max[0])
            is_between_y_boundaries = (self.player.rect.y - self.msgs_delta_max[1] < self.rect.y
                                       < self.player.rect.y + self.msgs_delta_max[1])
            if is_between_x_boundaries and is_between_y_boundaries:
                msg = TextMsg.create(
                    self.msg_texts.pop(), self.game,
                    time_in_secs=7,
                    delta_x=180, delta_y=34, owner=self)
                self.msgs.add([msg])

        if not self.msg_texts and not self.msgs:
            self.kill_hook()

        super().update_after_inc_index_hook()
