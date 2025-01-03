"""Module __main__. Entry point."""
__author__ = 'Joan A. Pinol  (japinol)'

import logging
from argparse import ArgumentParser
import gc
import traceback
import sys

import pygame as pg

from codemaster.game_entry_point import Game
from codemaster.tools.logger import logger
from codemaster.tools.logger.logger import log, LOGGER_FORMAT, LOGGER_FORMAT_NO_DATE
from codemaster.screens import ScreenStartGame
from codemaster.config.constants import LOG_START_APP_MSG, LOG_END_APP_MSG


def main():
    """Entry point of The CodeMaster program."""
    # Parse optional arguments from the command line
    parser = ArgumentParser(description="The CodeMaster. Nightmare on Bots' Island.",
                            prog="codemaster",
                            usage="%(prog)s [-h] [-f] [-l] [-m] [-n] [-p] [-u] [-d] [-t]")
    parser.add_argument('-f', '--fullscreen', default=False, action='store_true',
                        help='Full screen display activated when starting the game')
    parser.add_argument('-l', '--multiplelogfiles', default=False, action='store_true',
                        help='A log file by app execution, instead of one unique log file')
    parser.add_argument('-m', '--stdoutlog', default=False, action='store_true',
                        help='Print logs to the console along with writing them to the log file')
    parser.add_argument('-n', '--nologdatetime', default=False, action='store_true',
                        help='Logs will not print a datetime')
    parser.add_argument('-p', '--nopersistdata', default=False, action='store_true',
                        help='Deactivate feature: Persist and recover game data, which '
                             'automatically save the game state when the user exits the game.')
    parser.add_argument('-u', '--nodisplayscaled', default=False, action='store_true',
                        help='Remove the scaling of the game screen. '
                             'Resolution depends on desktop size and scale graphics. '
                             'Note that Pygame scaled is considered an experimental API '
                             'and is subject to change. '
                             'In most systems, is better to have the scaling activated when '
                             'using the full screen display mode')
    parser.add_argument('-d', '--debug', default=None, action='store_true',
                        help='Debug actions, information and traces. '
                             'This does not set the log level to debug. '
                             'Use the key shortcut ^ L_Alt + numpad_divide to toggle log levels')
    parser.add_argument('-t', '--debugtraces', default=None, action='store_true',
                        help='Show debug back traces information when something goes wrong')
    args = parser.parse_args()

    logger_format = LOGGER_FORMAT_NO_DATE if args.nologdatetime else LOGGER_FORMAT
    args.stdoutlog and logger.add_stdout_handler(logger_format)
    logger.add_file_handler(args.multiplelogfiles, logger_format)
    log.setLevel(logging.INFO)

    pg.init()
    is_music_paused = False

    log.info(LOG_START_APP_MSG)
    not args.stdoutlog and print(LOG_START_APP_MSG)
    log.info(f"App arguments: {' '.join(sys.argv[1:])}")

    # Multiple games loop
    while not Game.is_exit_game:
        try:
            Game.new_game = False
            pg.mouse.set_visible(True)
            game = Game(is_debug=args.debug, is_full_screen=args.fullscreen,
                        is_persist_data=not args.nopersistdata,
                        is_no_display_scaled=args.nodisplayscaled)
            game.is_music_paused = is_music_paused
            Game.ui_manager.set_game_data(game)
            game.screen_start_game = ScreenStartGame(game)
            while game.is_start_screen:
                game.screen_start_game.start_up()
            if not Game.is_exit_game:
                game.start()
                is_music_paused = game.is_music_paused
                del game.screen_start_game
                del game
                gc.collect()
        except FileNotFoundError as e:
            if args.debugtraces or args.debug:
                traceback.print_tb(e.__traceback__)
            log.critical(f'File not found error: {e}')
            break
        except Exception as e:
            if args.debugtraces or args.debug:
                traceback.print_tb(e.__traceback__)
            log.critical(f'ERROR. Abort execution: {e}')
            not args.stdoutlog and print(f'CRITICAL ERROR. Abort execution: {e}')
            break

    log.info(LOG_END_APP_MSG)
    not args.stdoutlog and print(LOG_END_APP_MSG)
    pg.quit()


if __name__ == '__main__':
    main()
