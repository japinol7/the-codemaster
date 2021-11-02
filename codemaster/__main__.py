"""Module __main__. Entry point."""
__author__ = 'Joan A. Pinol  (japinol)'
__version__ = '0.0.1'

from argparse import ArgumentParser
import gc
import traceback

import pygame as pg

from codemaster.game_entry_point import Game
from codemaster.config.settings import logger
from codemaster import screens


def main():
    """Entry point of The CodeMaster program."""
    # Parse optional arguments from the command line
    parser = ArgumentParser(description="The CodeMaster. Nightmare on Bots' Island.",
                            prog="codemaster",
                            usage="%(prog)s [-h] [-d] [-t]")
    parser.add_argument('-d', '--debug', default=None, action='store_true',
                        help='Debug actions, information and traces')
    parser.add_argument('-t', '--debugtraces', default=None, action='store_true',
                        help='Show debug back traces information when something goes wrong')
    args = parser.parse_args()

    pg.init()
    pg.mouse.set_visible(False)
    is_music_paused = False
    # Multiple games loop
    while not Game.is_exit_game:
        try:
            game = Game(is_debug=args.debug)
            game.is_music_paused = is_music_paused
            screen_start_game = screens.StartGame(game)
            while game.is_start_screen:
                screen_start_game.start_up()
            if not Game.is_exit_game:
                game.start()
                is_music_paused = game.is_music_paused
                del screen_start_game
                del game
                gc.collect()
        except FileNotFoundError as e:
            if args.debugtraces or args.debug:
                traceback.print_tb(e.__traceback__)
            logger.critical(f'File not found error: {e}')
            break
        except Exception as e:
            if args.debugtraces or args.debug:
                traceback.print_tb(e.__traceback__)
            logger.critical(f'Error: {e}')
            break
    pg.quit()


if __name__ == '__main__':
    main()
