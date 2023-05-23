"""Module test_code_master."""

__author__ = 'Joan A. Pinol  (japinol)'

import traceback

import pygame as pg

from codemaster.models.actors.items import ClockTimerA
from codemaster.models.actors.player import Player
from codemaster.config.constants import (
    APP_NAME,
    FONT_DEFAULT_NAME, FONT_FIXED_DEFAULT_NAME
    )
from codemaster.models.actors.text_msgs import TextMsg
from codemaster.tools.logger.logger import log
from codemaster.tools.utils import utils_graphics as libg_jp
from codemaster.version import version

from codemaster.resources import Resource
from codemaster.config.settings import Settings
from codemaster import levels
from codemaster.level_scroll_screen import level_scroll_shift_control
from suiteoftests.levels.level_test_1 import LevelTest1

PLAYER_HEALTH_SUPER_HERO = 90_000
CLOCK_TIMER_IN_SECS = 10

LOG_START_TEST_APP_MSG = f"Test app {APP_NAME} version: {version.get_version()}"
LOG_END_TEST_APP_MSG = f"End Testing {APP_NAME}"

IN_GAME_START_MSG = f"Let's test app {APP_NAME}\nversion: {version.get_version()}"

GROUP_DASHES_LINE = f"{'-' * 62}"
DASHES_LINE_SHORT = f"{'-' * 20}"


class Game:
    """Tests code_master."""

    screen = None
    size = None
    screen_flags = None

    def __init__(self):
        self.test_num = 0
        self.test_aborted_count = 0
        self.test_failed_count = 0
        self.test_passed_count = 0
        self.tests_total = 2
        self.tests_passed = []
        self.tests_failed = []
        self.tests_aborted = []

        self.done = False
        self.aborted = False
        self.clock = None
        self.clock_timer = None
        self.start_time = None
        self.active_sprites = None
        self.clock_sprites = None
        self.text_msg_sprites = None
        self.text_msg_pc_sprites = None
        self.player = None
        self.players = None
        self.player_actions = []
        self.levels = []
        self.levels_qty = None
        self.level_no = None
        self.level = None
        self.current_time = None
        self.sound_effects = False

    def main(self):
        pg.init()
        tests = [
            self.test_big_jump_and_fetch_3_batteries_n_1_disk,
            self.test_big_jump_and_fetch_1_file_disk,
            self.test_fetch_two_apples,
            ]
        self.tests_total = len(tests)
        log.info(LOG_START_TEST_APP_MSG)
        log.info(f"Total tests to pass: {self.tests_total}")
        try:
            for test_n in range(self.tests_total):
                self.set_up()
                tests.pop()()
                self.tear_down()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            log.critical(f'Error while testing: {e}')
        finally:
            pg.quit()
            self._print_test_results()
            log.info(LOG_END_TEST_APP_MSG)

    def _print_test_results(self):
        log.info(GROUP_DASHES_LINE)
        log.info(GROUP_DASHES_LINE)
        if self.test_passed_count:
            for test_passed in self.tests_passed:
                log.info(f"OK:      {test_passed}")
        if self.test_aborted_count:
            for test_aborted in self.tests_aborted:
                log.info(f"ABORTED: {test_aborted}")
        if self.test_passed_count < self.tests_total:
            for test_failed in self.tests_failed:
                log.info(f"FAILED:  {test_failed}")
        log.info(DASHES_LINE_SHORT)
        log.info(f"{self.test_passed_count} tests passed of {self.tests_total}")
        log.info(GROUP_DASHES_LINE)
        log.info(GROUP_DASHES_LINE)

    def set_up(self):
        log.info("Set Up")
        self.aborted = False
        self._init_settings()

        log.info("Create PC")
        self.player = Player('Pac', self)
        self.active_sprites = pg.sprite.Group()
        self.text_msg_sprites = pg.sprite.Group()
        self.text_msg_pc_sprites = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.players.add(self.player)

        log.info("Load test level 1")
        self.levels = [LevelTest1(self)]
        self.levels_qty = len(self.levels)
        self.level_no = 0
        self.level = self.levels[self.level_no]

        log.info("Set clock")
        self.clock = pg.time.Clock()
        self.start_time = pg.time.get_ticks()
        self.active_sprites.add(self.player)

        log.info("Level start up")
        self.level.start_up()
        self.player.level = self.level
        self.player.start_time = self.start_time
        self.player.stats['levels_visited'].add(self.level.id)

        pg.display.set_caption(f"{APP_NAME}_test_suite")

    def tear_down(self):
        levels.Level.clean_entity_ids()

    def _clock_die_hard(self):
        self.clock_timer.die_hard()
        log.info("Exit test game triggered by the timer clock")
        self.done = True

    def _init_settings(self):
        log.info("Calculate settings")
        pg_display_info = pg.display.Info()
        Settings.display_start_width = pg_display_info.current_w
        Settings.display_start_height = pg_display_info.current_h
        Settings.calculate_settings(speed_pct=None)
        # Set screen to the settings configuration
        Game.size = [Settings.screen_width, Settings.screen_height]
        Game.screen_flags = pg.DOUBLEBUF | pg.HWSURFACE
        Game.screen = pg.display.set_mode(Game.size, Game.screen_flags)

        log.info("Load and render resources")
        Resource.load_and_render_background_images()
        Resource.load_and_render_scorebar_images_and_txt()
        # Render characters in some colors to use it as a cache
        libg_jp.chars_render_text_tuple(font_name=FONT_DEFAULT_NAME)
        libg_jp.chars_render_text_tuple(font_name=FONT_FIXED_DEFAULT_NAME)

    def _init_clock_timer(self, time_in_secs=CLOCK_TIMER_IN_SECS):
        self.clock_timer = ClockTimerA(
                            self.player.rect.x, self.player.rect.y - 60,
                            self, time_in_secs)
        self.clock_timer.clock.trigger_method = self._clock_die_hard
        self.active_sprites.add(self.clock_timer)
        self.clock_sprites = pg.sprite.Group()
        self.clock_sprites.add(self.clock_timer)

    def _update_screen(self):
        Game.screen.blit(Resource.images['background'], (0, 0))
        self.level.draw()
        self.active_sprites.draw(Game.screen)

        for text_msg in self.text_msg_sprites:
            text_msg.draw_text()
        for clock in self.clock_sprites:
            clock.draw_text()

        self.level.magic_sprites.draw(Game.screen)

    def _player_move(self):
        if not self.player_actions:
            return

        if self.player_actions[-1][1] > 1:
            player_action = self.player_actions[-1][0]
            self.player_actions[-1][1] -= 1
        else:
            player_action = self.player_actions.pop()[0]

        if player_action == 'go_right':
            self.player.go_right()
        elif player_action == 'go_left':
            self.player.go_left()
        elif player_action == 'jump':
            self.player.jump()
        elif player_action == 'stop':
            self.player.stop()

    def calc_test_result(self, failed_condition, failed_msg, test_name):
        if self.aborted:
            self.test_aborted_count += 1
            self.tests_aborted += [test_name]
            return

        if failed_condition:
            log.warning(failed_msg)
            self.tests_failed += [test_name]
            self.test_failed_count += 1
            return

        self.tests_passed += [test_name]
        self.test_passed_count += 1

    def _game_loop(self):
        log.info("Start game loop")
        self.done = False
        while not self.done:
            self.current_time = pg.time.get_ticks()
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    log.warning("Warning! Abort test suite by user request")
                    self.done = True
                    self.aborted = True
                    self.test_aborted_count += 1

            level_scroll_shift_control(game=self)

            self._player_move()

            self.active_sprites.update()
            self.level.update()

            self._update_screen()
            self.clock.tick(Settings.fps)
            pg.display.flip()

    def test_fetch_two_apples(self):
        test_name = 'test_fetch_two_apples'
        log.info(f"Start {test_name}")
        self.player.rect.x = 240
        self.player.rect.y = 620
        self.player.stats['health'] = PLAYER_HEALTH_SUPER_HERO

        TextMsg.create(f"{IN_GAME_START_MSG}\nTest: {test_name}",
                       self, time_in_secs=5)
        self._init_clock_timer(time_in_secs=4)

        self.player_actions = [
            ['stop', 1],
            ['go_left', 4],
            ['stop', 1],
            ['go_right', 148],
            ['jump', 20],
            ['go_right', 30],
            ]

        self._game_loop()

        self.calc_test_result(
            failed_condition=self.player.stats['apples'] != 2,
            failed_msg="Test FAILED: Player did not fetch 2 apples.",
            test_name=test_name)

    def test_big_jump_and_fetch_1_file_disk(self):
        test_name = 'test_big_jump_and_fetch_1_file_disk'
        log.info(f"Start {test_name}")
        self.player.rect.x = 1420
        self.player.rect.y = 620
        self.player.stats['health'] = PLAYER_HEALTH_SUPER_HERO

        TextMsg.create(f"{IN_GAME_START_MSG}\nTest: {test_name}",
                       self, time_in_secs=5)
        self._init_clock_timer(time_in_secs=4)

        self.player_actions = [
            ['stop', 1],
            ['go_left', 45],
            ['jump', 1],
            ['go_left', 15],
            ]

        self._game_loop()

        self.calc_test_result(
            failed_condition=self.player.stats['files_disks'] != 1,
            failed_msg="Test FAILED: Player did not fetch 1 disk.",
            test_name=test_name)

    def test_big_jump_and_fetch_3_batteries_n_1_disk(self):
        test_name = 'test_big_jump_and_fetch_3_batteries_n_1_disk'
        log.info(f"Start {test_name}")
        self.player.rect.x = 1500
        self.player.rect.y = 50
        self.player.stats['health'] = PLAYER_HEALTH_SUPER_HERO

        TextMsg.create(f"{IN_GAME_START_MSG}\nTest: {test_name}",
                       self, time_in_secs=5)
        self._init_clock_timer(time_in_secs=5)

        self.player_actions = [
            ['stop', 1],
            ['go_right', 192],
            ['jump', 1],
            ['go_right', 18],
            ]

        self._game_loop()

        self.calc_test_result(
            failed_condition=self.player.stats['batteries'] < 3 or self.player.stats['files_disks'] < 1,
            failed_msg="Test FAILED: Player did not fetch at least 3 batteries and 1 disk.",
            test_name=test_name)
