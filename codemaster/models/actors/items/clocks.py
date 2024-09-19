"""Module clocks."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import BM_CLOCKS_FOLDER
from codemaster.models.actors.actor_types import ActorCategoryType, ActorType
from codemaster.models.actors.actors import ActorItem
from codemaster.models.stats import Stats
from codemaster.models.clocks import ClockTimer
from codemaster.tools.utils.colors import Color
from codemaster.tools.utils import utils_graphics as libg_jp
from codemaster.tools.logger.logger import log


class Clock(ActorItem):
    """Represents a clock.
    It is not intended to be instantiated.
    """
    def __init__(self, x, y, game, name=None, owner=None):
        self.file_folder = BM_CLOCKS_FOLDER
        self.file_name_key = 'im_clocks'
        self.owner = owner or game.player
        self.images_sprite_no = 1
        self.category_type = ActorCategoryType.CLOCK
        self.stats = Stats()
        self.stats.health = self.stats.health_total = 1
        self.stats.power = self.stats.power_total = 0
        self.stats.strength = self.stats.strength_total = 1
        self.cannot_be_copied = True

        super().__init__(x, y, game, name=name)

        self.text_img_w = 80

    def update_when_hit(self):
        """Cannot be hit."""
        pass

    def set_on(self):
        pass


class ClockA(Clock):
    """Represents a clock of type A. It generates a clock timer A"""

    def __init__(self, x, y, game, time_in_secs, name=None):
        self.file_mid_prefix = '01'
        self.type = ActorType.CLOCK_A
        self.time_in_secs = time_in_secs
        super().__init__(x, y, game, name=name)

    def set_on(self):
        clock = ClockTimerA(0, 0, self.game, self.time_in_secs)
        self.game.active_sprites.add([clock])
        self.game.clock_sprites.add([clock])
        self.kill()


class ClockTimerA(Clock):
    """Represents a clock timer of type A."""

    def __init__(self, dx, dy, game, time_in_secs, name=None,
                 owner=None, x_centered=True, y_on_top=True):
        self.file_mid_prefix = 'timer_01'
        self.type = ActorType.CLOCK_TIMER_A

        super().__init__(0, 0, game, name=name, owner=owner)

        self.clock = ClockTimer(self.game, time_in_secs, trigger_method=self.die_hard)

        self.dx, self.dy = 0, 0
        if x_centered:
            self.dx = (self.owner.rect.w - self.text_img_w) // 2
        self.dx += dx
        if y_on_top:
            self.dy = -7
        self.dy += dy

    def update(self):
        self.rect.bottom = self.owner.rect.y + self.dy
        self.rect.x = self.owner.rect.x + self.dx
        super().update()
        self.clock.tick()

    def draw_text(self):
        libg_jp.draw_text_rendered(
            text=self.clock.get_time_formatted(),
            x=self.rect.x + 12, y=self.rect.y + 3,
            screen=self.game.screen, color=Color.GREEN)

    def die_hard(self):
        self.game.is_log_debug and log.debug(
            f"{self.id} killed when {self.clock.id} ticked {self.clock.get_time()} secs.")
        self.kill()
