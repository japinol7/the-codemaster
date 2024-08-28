"""Module constants."""
__author__ = 'Joan A. Pinol  (japinol)'

from collections import namedtuple

from codemaster.version import version
from codemaster.config.constants import APP_TECH_NAME


PLAYER_HEALTH_SUPER_HERO = 90_000
CLOCK_TIMER_IN_SECS = 5
TEST_TIMEOUT_MIN = 1.5

IS_LOG_DEBUG_DEFAULT = False

LOG_START_TEST_APP_MSG = f"Test app {APP_TECH_NAME} version: {version.get_version()}"
LOG_END_TEST_APP_MSG = f"End Testing {APP_TECH_NAME}"

IN_GAME_START_MSG = f"Let's test app {APP_TECH_NAME}\nversion: {version.get_version()}"

GROUP_DASHES_LINE = '-' * 64
DASHES_LINE_SHORT = '-' * 22

TestFuncWithSetupLevels = namedtuple(
    'TestMethodWithSetupLevels', [
        'test_func', 'level_ids', 'starting_level_n', 'timeout', 'skip'
        ]
    )
