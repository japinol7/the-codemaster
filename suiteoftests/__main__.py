"""Module __main__. Entry point for the test suite."""
__author__ = 'Joan A. Pinol  (japinol)'

import logging
import traceback

from codemaster.tools.logger import logger
from codemaster.tools.logger.logger import log, LOGGER_FORMAT
from suiteoftests.test_code_master import Game

logger.add_stdout_handler(LOGGER_FORMAT)
log.setLevel(logging.DEBUG)


if __name__ == '__main__':
    try:
        test_code_master = Game()
        test_code_master.main()
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        log.critical(f'Error: {e}')
