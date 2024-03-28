"""Module mage."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from codemaster.config.constants import BM_NPCS_FOLDER, MSG_NPC_DURATION_LONG, DIRECTION_RIP
from codemaster.tools.logger.logger import log
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.actors import NPC, NPC_STRENGTH_BASE
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


class MageFemaleA(Mage):
    """Represents a Mage Female A."""

    def __init__(self, x, y, game, name=None, change_x=0, change_y=0,
                 border_left=0, border_right=0,
                 border_top=0, border_down=0,
                 items_to_drop=None):
        self.file_mid_prefix = '02'
        self.type = ActorType.MAGE_FEMALE_A

        self.stats = Stats()
        self.stats.power = self.stats.power_total = 0.07
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

        self.hostility_level = 0
        self.stats.time_between_spell_casting = 1000 # self.time_between_spell_casting_base
        self.spell_cast_x_delta_max = self.spell_cast_x_delta_max * 1.6
        self.spell_cast_y_delta_max = self.spell_cast_y_delta_max * 1.6

    def update_after_inc_index_hook(self):
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
            self.msg_texts.append(self.msg_text_to_repeat)

        super().update_after_inc_index_hook()

    def update_cast_spell_cast_actions(self):
        pc = self.player
        attack_power = 5

        if pc.direction == DIRECTION_RIP or pc.invulnerable:
            return
        log.debug(f"{pc.id} hit by {self.id}, "
                  f"pc_health: {str(round(pc.stats['health'], 2))}, "
                  f"magic_attach_power: {str(attack_power)}")
        pc.stats['health'] -= attack_power
        if pc.stats['health'] <= 0:
            log.debug(f"{pc.id}, !!! Dead by magic_attach {self.id} !!!")
            pc.die_hard()
