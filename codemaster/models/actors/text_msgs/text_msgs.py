"""Module text msgs."""
__author__ = 'Joan A. Pinol  (japinol)'

from enum import Enum

import pygame as pg

from codemaster.config.constants import (
    BM_TEXT_MSGS_FOLDER,
    MSG_PC_DURATION,
    MSG_PC_DELTA_X,
    MSG_PC_DELTA_Y
    )
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorMsg
from codemaster.models.stats import Stats
from codemaster.models.clocks import ClockTimer
from codemaster.tools.utils.colors import Color
from codemaster.tools.utils import utils_graphics as libg_jp
from codemaster.tools.logger.logger import log


class TextMsgPosition(Enum):
    """Text msg positions."""
    NONE = 0
    ABSOLUTE = 1
    NEAR_ACTOR = 2
    NEAR_OBJECT = 3
    NEAR_TOP_LEFT = 4
    NARRATOR_CENTER_DOWN = 5


class TextMsg(ActorMsg):
    """Represents a base text message.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, time_in_secs, name=None,
                 delta_x=0, delta_y=0, owner=None):
        self.owner = owner
        self.file_folder = BM_TEXT_MSGS_FOLDER
        self.file_name_key = 'text_msgs'
        self.images_sprite_no = 1
        self.category_type = ActorCategoryType.TEXT_MSG
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.power = self.stats.power_total = 0
        self.stats.strength = self.stats.strength_total = 1
        self.lines_count = 0
        self.balloon_lines = 0
        self.balloon_height = 0
        self.balloon_width = 0
        self.balloon_rect_y_delta = 0

        if not getattr(self, 'type', None):
            self.msg_position = TextMsgPosition.NONE

        super().__init__(x, y, game, name=name)

        self.clock = ClockTimer(self.game, time_in_secs, trigger_method=self.die_hard)

    def update(self):
        self.clock.tick()

    def update_when_hit(self):
        """Cannot be hit."""
        pass

    def draw_text(self):
        self.draw_speech_balloon(self.color or Color.GREEN)
        if '\n' not in self.name:
            text_render_method = libg_jp.draw_text_rendered
            optional_args = {}
        else:
            text_render_method = libg_jp.draw_text_multi_lines_rendered
            optional_args = {'space_btw_lines': 21}
        text_render_method(
            text=self.name,
            x=self.rect.x + 12, y=self.rect.y + 3 - self.lines_count * 22,
            screen=self.game.screen, color=self.color or Color.GREEN, is_font_fixed=True,
            space_btw_chars=12, space_btw_words=14, **optional_args)

    def die_hard(self):
        self.game.is_log_debug and log.debug(
            f"{self.id} killed when {self.clock.id} "
            f"ticked {self.clock.get_time()} secs.")
        self.kill()

    def draw_speech_balloon(self, color):
        pg.draw.rect(
            self.game.screen, color,
            (self.rect.x, self.rect.y + self.balloon_rect_y_delta,
             self.balloon_width, self.balloon_height),
            width=1)

    @staticmethod
    def create(text, game, time_in_secs=MSG_PC_DURATION, msg_class=None,
               x=None, y=None, color=None, delta_x=None, delta_y=None,
               owner=None, balloon_lines_count=0, balloon_chars_for_line=0):
        class_ = msg_class or TextMsgActor
        owner = owner or game.player
        delta_x = MSG_PC_DELTA_X if delta_x is None else delta_x
        delta_y = MSG_PC_DELTA_Y if delta_y is None else delta_y
        text_msg = class_(
               x or owner.rect.x - delta_x,
               y or owner.rect.y - delta_y,
               game, time_in_secs, name=text,
               color=color, delta_x=delta_x, delta_y=delta_y,
               owner=owner)
        game.active_sprites.add([text_msg])
        game.text_msg_sprites.add([text_msg])

        for old_pc_msg in game.text_msg_pc_sprites:
            if old_pc_msg.owner == owner:
                old_pc_msg.kill()
        game.text_msg_pc_sprites.add([text_msg])

        text_msg.lines_count = text_msg.name.count('\n')

        text_msg.update()

        # Calculate speech balloon attributes
        text_msg.balloon_lines = balloon_lines_count or text_msg.lines_count
        if text_msg.balloon_lines > 1:
            text_len = balloon_chars_for_line or len(max(text_msg.name.splitlines(), key=len))
            text_msg.balloon_height = 29 + 22 * text_msg.balloon_lines
        else:
            text_len = balloon_chars_for_line or len(text_msg.name)
            text_msg.balloon_height = text_msg.rect.height
        text_msg.balloon_width = 2 + 14 * text_len if text_len < 20 else 13.1 * text_len
        text_msg.balloon_rect_y_delta = -text_msg.balloon_lines * 22
        text_msg.balloon_width = int(text_msg.balloon_width)
        text_msg.balloon_height = int(text_msg.balloon_height)

        return text_msg


class TextMsgAbsolute(TextMsg):
    """Represents a text message in an absolute position."""

    def __init__(self, x, y, game, time_in_secs, name=None, color=None,
                 delta_x=0, delta_y=0, owner=None):
        self.file_mid_prefix = 'timer_01'
        self.color = color
        self.msg_position = TextMsgPosition.ABSOLUTE
        self.type = ActorType.TEXT_MSG_ABS
        super().__init__(x, y, game, name=name, time_in_secs=time_in_secs,
                         delta_x=delta_x, delta_y=delta_y, owner=owner)


class TextMsgActor(TextMsg):
    """Represents a text message from an actor."""

    def __init__(self, x, y, game, time_in_secs, name=None, color=None,
                 delta_x=0, delta_y=0, owner=None):
        self.file_mid_prefix = 'timer_01'
        self.color = color
        self.msg_position = TextMsgPosition.NEAR_ACTOR
        self.type = ActorType.TEXT_MSG_PLAYER if owner == game.player else ActorType.TEXT_MSG_ACTOR

        super().__init__(x, y, game, name=name, time_in_secs=time_in_secs,
                         delta_x=delta_x, delta_y=delta_y, owner=owner)

    def update(self):
        self.rect.x = self.owner.rect.x - self.delta_x
        self.rect.bottom = self.owner.rect.y - self.delta_y
        super().update()


class TextMsgActorTop(TextMsg):
    """Represents a text message from an actor on top ot the screen."""

    def __init__(self, x, y, game, time_in_secs, name=None, color=None,
                 delta_x=0, delta_y=0, owner=None):
        self.file_mid_prefix = 'timer_01'
        self.color = color
        self.msg_position = TextMsgPosition.NEAR_TOP_LEFT
        self.type = ActorType.TEXT_MSG_PLAYER if owner == game.player else ActorType.TEXT_MSG_ACTOR

        super().__init__(x, y, game, name=name, time_in_secs=time_in_secs,
                         delta_x=delta_x, delta_y=delta_y, owner=owner)

    def update(self):
        self.rect.x = 20
        self.rect.y = 250 - 21 * (8 - self.lines_count)
        super().update()

class TextMsgActorNarrator(TextMsg):
    """Represents a text message to be used for the narrator in cutscenes."""

    def __init__(self, x, y, game, time_in_secs, name=None, color=None,
                 delta_x=0, delta_y=0, owner=None):
        self.file_mid_prefix = 'timer_01'
        self.color = color
        self.msg_position = TextMsgPosition.NARRATOR_CENTER_DOWN
        self.type = ActorType.TEXT_MSG_PLAYER if owner == game.player else ActorType.TEXT_MSG_ACTOR

        super().__init__(x, y, game, name=name, time_in_secs=time_in_secs,
                         delta_x=delta_x, delta_y=delta_y, owner=owner)

    def update(self):
        self.rect.x = 240
        self.rect.y = 620
        super().update()
