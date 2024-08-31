"""Module mage."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import (
    BM_NPCS_FOLDER,
    MSG_NPC_DURATION_LONG,
    DIRECTION_LEFT,
    DIRECTION_RIGHT,
    )
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.actors import NPC, NPC_STRENGTH_BASE
from codemaster.models.actors.items.energy_shields import EnergyShield
from codemaster.models.actors.text_msgs import TextMsg
from codemaster.models.stats import Stats
from codemaster.models.actors import magic


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

        self.spell_cast_x_delta_max = self.spell_cast_x_delta_max * 1.6
        self.spell_cast_y_delta_max = self.spell_cast_y_delta_max * 1.6
        self.spell_1_name = ActorType.VORTEX_OF_DOOM_A.name
        self.spell_2_name = ActorType.DRAIN_LIFE_A.name
        self.spell_3_name = ActorType.DRAIN_LIFE_B.name
        self.probability_to_cast_spell_1 = 8
        self.probability_to_cast_spell_2 = 13
        self.probability_to_cast_spell_3 = 100
        self.max_multi_spell_1 = 1
        self.max_multi_spell_2 = 2
        self.max_multi_spell_3 = 4
        self.npc_summoned_count = 0


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

        if not self.msg_texts or self.hostility_level > 0:
            self.hostility_level = 1
            self.stats.energy_shield.activate()
            self.msg_texts.clear()
            self.msg_texts.append(self.msg_text_to_repeat)

        super().update_after_inc_index_hook()

    def update_cast_spell_cast_actions(self):
        magic.update_cast_spell_cast_actions_3_spells(actor=self)

        if self.npc_summoned_count < 1:
            self._summon_npc_minions()

    def _summon_npc_minions(self):
        # Summon EwlanMale
        self.npc_summoned_count += 1
        npc_x = self.rect.x - 754
        npc = magic.summon_npc(
            'EwlanMale',
            npc_x,
            self.rect.y - 277,
            game=self.game,
            **{'change_x': 2,
               'border_left': npc_x - 190,
               'border_right': npc_x + 236,
               }
            )
        EnergyShield.actor_acquire_energy_shield(npc, self.game, health_total=200)

        # Summon Bats
        npcs_data = [
            {'class_name': 'BatBlack', 'x': self.rect.x - 920, 'y': self.rect.y},
            {'class_name': 'BatBlue', 'x': self.rect.x - 820, 'y': self.rect.y + 17},
            {'class_name': 'BatBlack', 'x': self.rect.x - 720, 'y': self.rect.y},
            ]
        self.npc_summoned_count += len(npcs_data)
        for npc_vals in npcs_data:
            magic.summon_npc(
                npc_vals['class_name'],
                npc_vals['x'],
                npc_vals['y'],
                game=self.game,
                **{'change_x': 2,
                   'border_left': npc_vals['x'] - 220,
                   'border_right': npc_vals['x'] + 220,
                   }
                )


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

        self.hostility_level = 0
        self.magic_resistance = 990
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
