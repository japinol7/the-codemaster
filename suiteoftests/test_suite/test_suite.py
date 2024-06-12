"""Module test_suite."""
__author__ = 'Joan A. Pinol  (japinol)'

import traceback

import pygame as pg

from codemaster.models.actors.items import ClockTimerA, RadioA
from codemaster.models.actors.player import Player
from codemaster.config.constants import (
    APP_TECH_NAME,
    FONT_DEFAULT_NAME,
    FONT_FIXED_DEFAULT_NAME
    )
from codemaster.models.actors.selectors import SelectorA
from codemaster.tools.logger.logger import log
from codemaster.tools.utils import utils_graphics as libg_jp

from codemaster.resources import Resource
from codemaster.config.settings import Settings
from codemaster.level_scroll_screen import level_scroll_shift_control, change_screen_level
from codemaster.tools.utils.queue import Queue
from codemaster import levels
from suiteoftests import levels as test_levels
from suiteoftests.config.constants import (
    CLOCK_TIMER_IN_SECS,
    DASHES_LINE_SHORT,
    GROUP_DASHES_LINE,
    IN_GAME_START_MSG,
    IS_LOG_DEBUG_DEFAULT,
    LOG_START_TEST_APP_MSG,
    LOG_END_TEST_APP_MSG,
    )
from suiteoftests.test_suite.actor_actions import (
    CAST_SPELL_ON_TARGET_CLASSES_MAP,
    PLAYER_ACTION_METHODS_MAP,
    )
from codemaster.models.actors.text_msgs import TextMsg


class GameTestSuite:
    """Represents a test suite framework for the code_master game.
    All the tests added to the test suite using the add_tests method will be executed.
    You can skip a test by setting its skip attribute to True.
    """

    screen = None
    size = None
    screen_flags = None

    def __init__(self):
        self._tests = Queue()
        self.test_num = 0
        self.test_aborted_count = 0
        self.test_failed_count = 0
        self.test_passed_count = 0
        self.test_skipped_count = 0
        self.current_test = None
        self.tests_total = 0
        self.tests_aborted = []
        self.tests_failed = []
        self.tests_passed = []
        self.tests_skipped = []
        self.tests_skipped_text = ''

        self.done = False
        self.aborted = False
        self.clock = None
        self.clock_timer = None
        self.start_time = None
        self.is_log_debug = IS_LOG_DEBUG_DEFAULT
        self.active_sprites = None
        self.clock_sprites = None
        self.text_msg_sprites = None
        self.text_msg_pc_sprites = None
        self.player = None
        self.players = None
        self.player_actions = Queue()
        self.levels = []
        self.levels_qty = None
        self.level_no = None
        self.level = None
        self.current_time = None
        self.sound_effects = False
        self.mouse_pos = 0, 0
        self.is_magic_on = False
        self.selector_sprites = pg.sprite.Group()
        self.test_spell_target = None
        self.is_settings_initialized_before = False

    @property
    def tests(self):
        return self._tests

    def add_tests(self, tests):
        for test in tests:
            self._tests.push(test)

    def add_player_actions(self, actions):
        """Adds player actions for the current test."""
        self.player_actions.extend(actions)

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
        log.info(f"{self.test_passed_count} tests passed of {self.tests_total}{self.tests_skipped_text}")
        log.info(GROUP_DASHES_LINE)
        log.info(GROUP_DASHES_LINE)

    def _mock_player_die_hard(self):
        def player_die_hard_mock():
            if self.player.lives < 1:
                return
            self.player.lives -= 1
            TextMsg.create("Player DIED! RIP", self, time_in_secs=5)

        self.player.die_hard = player_die_hard_mock

    def _set_up(self, level_name_nums=None, starting_level_n=0, is_debug=False, is_full_screen=False):
        log.info("Set Up")
        self.aborted = False
        self._init_settings(is_debug=is_debug, is_full_screen=is_full_screen)

        log.info("Create PC")
        self.player = Player('Pac', self)
        self.active_sprites = pg.sprite.Group()
        self.text_msg_sprites = pg.sprite.Group()
        self.text_msg_pc_sprites = pg.sprite.Group()
        self.selector_sprites = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.players.add(self.player)
        self.player_actions = Queue()

        self._load_test_levels(level_name_nums=level_name_nums, starting_level_n=starting_level_n)

        log.info("Set clock")
        self.clock = pg.time.Clock()
        self.start_time = pg.time.get_ticks()
        self.active_sprites.add(self.player)

        log.info("Level start up")
        self.level.start_up()
        self.player.level = self.level
        self.player.start_time = self.start_time
        self.player.stats['levels_visited'].add(self.level.id)

        self.selector_sprites.add(
            SelectorA(0, 0, self),
            )

        pg.display.set_caption(f"{APP_TECH_NAME}_test_suite")

        # Add an actor that will hold the test name msg
        self.actor_test_name_holder = RadioA(5, 390, self)
        self.level.add_actors([self.actor_test_name_holder])

        self._mock_player_die_hard()

    def _load_test_levels(self, level_name_nums=None, starting_level_n=0):
        log.info(f"Load test levels: {level_name_nums}")
        self.levels = levels.Level.factory_by_nums(
            levels_module=test_levels, game=self,
            level_name_nums=level_name_nums, level_name_prefix='LevelTest')
        self.levels_qty = len(self.levels)
        self.level = self.levels[starting_level_n]

    def _tear_down(self):
        log.info("Tear Down")
        levels.Level.clean_entity_ids()

    def _clock_die_hard(self):
        self.clock_timer.die_hard()
        log.info("Exit game loop triggered by the timer clock. Test: %s", self.current_test.__name__)
        self.done = True

    def _init_settings(self, is_debug=False, is_full_screen=False):
        log.info("Calculate settings")
        if self.is_settings_initialized_before:
            Settings.calculate_settings(speed_pct=None, full_screen=is_full_screen)
            return

        suite = GameTestSuite
        pg_display_info = pg.display.Info()
        Settings.display_start_width = pg_display_info.current_w
        Settings.display_start_height = pg_display_info.current_h
        Settings.calculate_settings(speed_pct=None, full_screen=is_full_screen)
        # Set screen to the settings configuration
        suite.size = [Settings.screen_width, Settings.screen_height]
        suite.full_screen_flags = pg.FULLSCREEN | pg.SCALED
        suite.normal_screen_flags = pg.SHOWN
        suite.screen_flags = suite.full_screen_flags if Settings.is_full_screen else suite.normal_screen_flags
        suite.screen = pg.display.set_mode(suite.size, suite.screen_flags)

        log.info("Load and render resources")
        Resource.load_and_render_background_images()
        Resource.load_sound_resources()
        # Render characters in some colors to use it as a cache
        libg_jp.chars_render_text_tuple(font_name=FONT_DEFAULT_NAME)
        libg_jp.chars_render_text_tuple(font_name=FONT_FIXED_DEFAULT_NAME)
        self.is_log_debug = is_debug
        self.is_settings_initialized_before = True

    def _init_clock_timer(self, time_in_secs=CLOCK_TIMER_IN_SECS):
        self.clock_timer = ClockTimerA(
            52, 32,
            self, time_in_secs,
            owner=self.actor_test_name_holder)
        self.clock_timer.clock.trigger_method = self._clock_die_hard
        self.active_sprites.add(self.clock_timer)
        self.clock_sprites = pg.sprite.Group()
        self.clock_sprites.add(self.clock_timer)

    def _update_screen(self):
        GameTestSuite.screen.blit(Resource.images['background'], (0, 0))
        self.level.draw()
        self.active_sprites.draw(GameTestSuite.screen)

        for text_msg in self.text_msg_sprites:
            text_msg.draw_text()
        for clock in self.clock_sprites:
            clock.draw_text()

        for sprite in self.level.particle_tuple_sprites:
            sprite.update_particle_sprites()
        for sprite in self.level.particle_sprites:
            sprite.update_particle_sprites()

        if self.is_magic_on:
            for selector in self.selector_sprites:
                selector.update()
            self.selector_sprites.draw(GameTestSuite.screen)

        self.level.magic_sprites.draw(GameTestSuite.screen)

    def _player_move(self):
        if not self.player_actions:
            return

        if self.player_actions.peek()[1] > 1:
            player_action = self.player_actions.peek()[0]
            self.player_actions.peek()[1] -= 1
        else:
            player_action = self.player_actions.pop()[0]

        player_action_methods_map = PLAYER_ACTION_METHODS_MAP[player_action]

        if player_action_methods_map.method_name == 'cast_spell_on_target':
            spell = player_action_methods_map.kwargs.get('spell')
            self.player.stats['magic_attack'] = CAST_SPELL_ON_TARGET_CLASSES_MAP.get(spell)
            if not self.player.stats['magic_attack']:
                raise ValueError("Magic attack missing. Cannot cast spell!")
            for selector in self.selector_sprites:
                selector.rect.x = self.test_spell_target.rect.centerx
                selector.rect.y = self.test_spell_target.rect.centery
                selector.get_pointed_sprites()
            return

        getattr(self.player, player_action_methods_map.method_name)(**player_action_methods_map.kwargs)

    def _create_test_name_msg_actor(self, test_method_with_setup_levels):
        TextMsg.create(f"{IN_GAME_START_MSG}\nTest: {self.current_test.__name__}",
                       game=self, owner=self.actor_test_name_holder,
                       delta_x=0, delta_y=3,
                       time_in_secs=test_method_with_setup_levels.timeout-0.06)

    def assert_test_passed(self, condition, failed_msg):
        if self.aborted:
            self.test_aborted_count += 1
            self.tests_aborted += [self.current_test.__name__]
            return

        if not condition:
            log.warning(f"Test FAILED: {failed_msg}")
            self.tests_failed += [self.current_test.__name__]
            self.test_failed_count += 1
            return

        self.tests_passed += [self.current_test.__name__]
        self.test_passed_count += 1

    def game_loop(self):
        log.info("Start game loop")
        self.done = False
        while not self.done:
            self.current_time = pg.time.get_ticks()
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    log.warning("Abort test by user request: %s", self.current_test.__name__)
                    self.done = True
                    self.aborted = True
                    self.test_aborted_count += 1

            level_scroll_shift_control(game=self)

            # Check if we hit any door
            door_hit_list = pg.sprite.spritecollide(self.player, self.level.doors, False)
            for door in door_hit_list:
                if not door.is_locked:
                    change_screen_level(game=self, door=door)

            self._player_move()
            self.active_sprites.update()
            self.level.update()

            self._update_screen()
            self.clock.tick(Settings.fps)
            pg.display.flip()

    def run(self, is_debug=False, is_full_screen=False):
        if not self.tests:
            return

        self.tests_skipped = [test.test_func.__name__ for test in self.tests if test.skip]
        self.test_skipped_count = len(self.tests_skipped)
        self.tests_skipped_text = f". Tests skipped: {self.test_skipped_count}" if self.test_skipped_count else ''
        self.tests_total = sum(1 for test in self.tests if not test.skip)

        log.info(LOG_START_TEST_APP_MSG)
        log.info(f"Total tests to pass: {self.tests_total}{self.tests_skipped_text}")
        pg.init()
        try:
            for test in tuple(self.tests):
                test_method_with_setup_levels = self.tests.pop()
                self.current_test = test_method_with_setup_levels.test_func
                if test.skip:
                    continue
                self._set_up(
                    level_name_nums=test_method_with_setup_levels.level_name_nums,
                    starting_level_n=test_method_with_setup_levels.starting_level_n,
                    is_debug=is_debug, is_full_screen=is_full_screen)
                log.info(f"Start {self.current_test.__name__}")
                self._create_test_name_msg_actor(test_method_with_setup_levels)
                self._init_clock_timer(test.timeout)
                test_method_with_setup_levels.test_func(
                    self=test_method_with_setup_levels.__class__,
                    game=self)
                self._tear_down()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            log.critical(f'Error while testing: {e}')
        finally:
            pg.quit()
            self._print_test_results()
            log.info(LOG_END_TEST_APP_MSG)
