"""Module __main__. Entry point for the test suite."""
__author__ = 'Joan A. Pinol  (japinol)'

from argparse import ArgumentParser
import logging
import traceback

from codemaster.tools.logger import logger
from codemaster.tools.logger.logger import log, LOGGER_FORMAT
from suiteoftests.test_suite.test_suite import GameTestSuite
from suiteoftests.test_suite.game_test import GameTest

# Import the tests to run
from . import tests

logger.add_stdout_handler(LOGGER_FORMAT)
log.setLevel(logging.DEBUG)


def main():
    # Parse optional arguments from the command line
    parser = ArgumentParser(description="Test suite for: The CodeMaster.",
                            prog="suiteoftests")
    parser.add_argument('-n', '--names', default=None,
                        help="a comma separated list of tests to run.")
    parser.add_argument('-f', '--fullscreen', default=False, action='store_true',
                        help='Full screen display activated when starting the test suite')
    parser.add_argument('-d', '--debug', default=None, action='store_true',
                        help='Set the log level to debug.')
    args = parser.parse_args()

    try:
        GameTest.set_tests_to_run(args.names or None)
        test_suite = GameTestSuite()
        GameTest(test_suite)
        test_suite.run(is_debug=args.debug, is_full_screen=args.fullscreen)

        if test_suite.tests_failed or test_suite.tests_aborted:
            quit(1)
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        log.critical(f'Error: {e}')


if __name__ == '__main__':
    main()
