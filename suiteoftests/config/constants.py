"""Module constants."""
__author__ = 'Joan A. Pinol  (japinol)'

from collections import namedtuple

from codemaster.version import version
from codemaster.config.constants import APP_TECH_NAME
from codemaster.models.actors.items.bullets import BulletType


PLAYER_HEALTH_SUPER_HERO = 90_000
CLOCK_TIMER_IN_SECS = 10

IS_LOG_DEBUG_DEFAULT = True

LOG_START_TEST_APP_MSG = f"Test app {APP_TECH_NAME} version: {version.get_version()}"
LOG_END_TEST_APP_MSG = f"End Testing {APP_TECH_NAME}"

IN_GAME_START_MSG = f"Let's test app {APP_TECH_NAME}\nversion: {version.get_version()}"

GROUP_DASHES_LINE = '-' * 62
DASHES_LINE_SHORT = '-' * 20

TestMethodWithSetupLevels = namedtuple(
    'TestMethodWithSetupLevels', ['test', 'level_name_nums', 'starting_level_n', 'skip']
    )

PlayerActionMethodArgs = namedtuple('PlayerActionsArgs', ['method_name', 'kwargs'])
PLAYER_ACTION_METHODS_MAP = {
    'go_right': PlayerActionMethodArgs('go_right', kwargs={}),
    'go_left': PlayerActionMethodArgs('go_left', kwargs={}),
    'jump': PlayerActionMethodArgs('jump', kwargs={}),
    'shot_bullet_t3_photonic': PlayerActionMethodArgs(
        'shot_bullet', kwargs={'bullet_type': BulletType.T3_PHOTONIC}),
    'stop': PlayerActionMethodArgs('stop', kwargs={}),
    }
