"""Module __main__. Entry point for the test suite."""
__author__ = 'Joan A. Pinol  (japinol)'

import logging
import traceback

from codemaster.tools.logger import logger
from codemaster.tools.logger.logger import log, LOGGER_FORMAT
from suiteoftests.test_suite.test_suite import GameTestSuite
from suiteoftests.test_player_fetch_items import TestPlayerFetchItems
from suiteoftests.test_player_big_jump import TestPlayerBigJump
from suiteoftests.test_player_shoots_npcs import TestPlayerShootsNPCs

logger.add_stdout_handler(LOGGER_FORMAT)
log.setLevel(logging.DEBUG)


if __name__ == '__main__':
    try:
        test_suite = GameTestSuite()
        TestPlayerFetchItems(test_suite)
        TestPlayerBigJump(test_suite)
        TestPlayerShootsNPCs(test_suite)
        test_suite.main()
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        log.critical(f'Error: {e}')
