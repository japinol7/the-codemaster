"""Module clocks."""
__author__ = 'Joan A. Pinol  (japinol)'

from enum import Enum

from codemaster.config.settings import Settings


class ClockType(Enum):
    """Clock types."""
    NONE = 0
    STOPWATCH = 1
    TIMER = 2


class ClockBase:
    """Represents a base clock.
    It is not intended to be instantiated.
    """
    def __init__(self, game, time_in_secs):
        self.fps = Settings.fps
        self.game = game
        self.initial_time_in_secs = time_in_secs
        self.time = time_in_secs * self.fps
        self.on = True
        self.trigger_event = False
        self.triggered_event = False

        if not getattr(self, 'type', None):
            self.type = ClockType.NONE

    def get_time(self, rounding=True):
        if rounding:
            return int(self.time / self.fps)
        return self.time / self.fps

    def set_time(self, seconds):
        self.time = seconds * self.fps

    def get_time_formatted(self):
        total_seconds = self.get_time()
        minutes = int((total_seconds - (total_seconds % 60)) / 60)
        seconds = int(total_seconds - (minutes * 60))
        return f'{minutes}:{seconds:02d}'

    def tick(self):
        if not self.on:
            return
        self._tick()

    def _tick(self):
        pass

    def set_on(self):
        self.on = True

    def set_off(self):
        self.on = False

    def restart(self):
        self.on = True
        self.set_time(self.initial_time_in_secs)


class ClockStopwatch(ClockBase):

    def __init__(self, game, time_in_secs=0):
        self.type = ClockType.STOPWATCH
        super().__init__(game, time_in_secs)

    def _tick(self):
        self.time += 1


class ClockTimer(ClockBase):

    def __init__(self, game, time_in_secs, trigger_method=None):
        self.type = ClockType.TIMER

        super().__init__(game, time_in_secs)

        if trigger_method:
            self.trigger_method = trigger_method
            self.trigger_event = True
            self.triggered_event = False

    def _tick(self):
        if self.time < 0:
            self.set_off()
            if not self.triggered_event:
                self.trigger_method()
                self.triggered_event = True
            return
        self.time -= 1

    def restart(self):
        super().restart()
        self.triggered_event = False
