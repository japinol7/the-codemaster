"""Module test_suite."""
__author__ = 'Joan A. Pinol  (japinol)'

import gc
import os
import traceback

import pygame as pg

from codemaster.models.actors.items import (
    ClockTimerA,
    InvisibleHolderA,
    )
from codemaster.models.actors.items.files_disks import FilesDisk
from codemaster.models.actors.player import Player
from codemaster.config.constants import (
    APP_TECH_NAME,
    FONT_DEFAULT_NAME,
    FONT_FIXED_DEFAULT_NAME,
    N_LEVELS,
    )
from codemaster.models.actors.selectors import SelectorA
from codemaster.models.actors.text_msgs.text_msgs import TextMsgActorTop
from codemaster.tools.logger.logger import log
from codemaster.tools.utils import utils_graphics as libg_jp
from codemaster.resources import Resource
from codemaster.config.settings import Settings
from codemaster.level_scroll_screen import (
    level_scroll_shift_control,
    change_screen_level,
    )
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
from codemaster.models.actors.player_auto_actions import execute_pc_action
from codemaster.models.actors.text_msgs import TextMsg
from codemaster.persistence import persistence
from codemaster.persistence.persistence_settings import PersistenceSettings
from suiteoftests.test_suite.game_test import validate_game_test_timeout


class GameTestSuite:
    """Represents a test suite framework for the code_master game.
    All the tests added to the test suite using the add_tests
    method will be executed.
    You can skip a test by setting its skip attribute to True.
    """

    is_log_debug = IS_LOG_DEBUG_DEFAULT
    is_load_last_game_failed = False
    screen = None
    size = None
    screen_flags = None
    ui_manager = None
    files_disks_data = None

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
        self.test_load_last_game_failed = False

        self.done = False
        self.aborted = False
        self.aborted_all = False
        self.clock = None
        self.clock_timer = None
        self.start_time = None
        self.level_ids = None
        self.starting_level_n = None
        self.game_loop_exec_times = 0
        self.current_test_timeout = None
        self.active_sprites = None
        self.clock_sprites = None
        self.text_msg_sprites = None
        self.text_msg_pc_sprites = None
        self.player = None
        self.players = None
        self.levels = []
        self.level_cutscene = None
        self.levels_qty = None
        self.level_no = None
        self.level = None
        self.level_tutorial = None
        self.level_init = None
        self.current_time = None
        self.is_music_paused = True
        self.sound_effects = False
        self.mouse_pos = 0, 0
        self.is_magic_on = False
        self.selector_sprites = pg.sprite.Group()
        self.is_settings_initialized_before = False
        self.is_persist_data = False
        self.persistence_path = os.path.join('suiteoftests', 'data', "save_data")
        self.is_continue_game = False
        self.is_load_user_game = False
        self.update_state_counter = 0
        # Auto actor actions for cutscenes, ...
        self.pc_auto_actions = Queue()

    @property
    def tests(self):
        return self._tests

    def add_tests(self, tests):
        for test in tests:
            self._tests.push(test)

    def add_player_actions(self, actions):
        for action in actions:
            self.pc_auto_actions.push(list(action))

    def _print_test_results(self):
        log.info(GROUP_DASHES_LINE)
        log.info(GROUP_DASHES_LINE)
        if self.test_passed_count:
            for test_passed in self.tests_passed:
                log.info(f"OK      {test_passed}")
        if self.test_aborted_count:
            for test_aborted in self.tests_aborted:
                log.info(f"ABORTED {test_aborted}")
        if self.test_passed_count < self.tests_total:
            for test_failed in self.tests_failed:
                log.info(f"FAILED  {test_failed}")
        log.info(DASHES_LINE_SHORT)
        log.info(f"{self.test_passed_count} tests passed of "
                 f"{self.tests_total}{self.tests_skipped_text}")
        log.info(GROUP_DASHES_LINE)
        log.info(GROUP_DASHES_LINE)

    def _mock_player_die_hard(self):
        def player_die_hard_mock():
            if self.player.lives < 1:
                return
            self.player.lives -= 1
            TextMsg.create("Player DIED! RIP", self, time_in_secs=5)

        self.player.die_hard = player_die_hard_mock

    def _set_up(self, is_debug=False, is_full_screen=False,
                is_set_up_actors_and_levels=True):
        log.info("Set Up")
        self.aborted = False
        self.is_persist_data = False
        self.__class__.is_load_last_game_failed = False
        self.test_load_last_game_failed = False
        self.game_loop_exec_times = 0
        self.current_test_timeout = None

        self._init_settings(is_debug=is_debug, is_full_screen=is_full_screen)
        FilesDisk.reset_msgs_loaded_in_disks(self)

        if is_set_up_actors_and_levels:
            self.set_up_actors_and_levels()

    def set_up_actors_and_levels(self):
        levels.Level.clean_entity_ids()

        log.info("Create PC")
        self.player = Player('Pac', self)
        self.active_sprites = pg.sprite.Group()
        self.text_msg_sprites = pg.sprite.Group()
        self.text_msg_pc_sprites = pg.sprite.Group()
        self.selector_sprites = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.players.add(self.player)
        self.player_actions = Queue()
        self.player.sound_effects = self.sound_effects

        self._load_test_levels(
            level_ids=self.level_ids,
            starting_level_n=self.starting_level_n)

        log.info("Set clock")
        self.clock = pg.time.Clock()
        self.start_time = pg.time.get_ticks()
        self.active_sprites.add(self.player)

        log.info("Level start up")
        self.player.level = self.level
        self.player.start_time = self.start_time
        self.player.stats['levels_visited'].add(self.level.id)

        self.selector_sprites.add(
            SelectorA(0, 0, self),
            )

        pg.display.set_caption(f"{APP_TECH_NAME}_test_suite")

        # Add an actor that will hold the test name msg
        self.actor_test_name_holder = InvisibleHolderA(10, 214, self)
        self._mock_player_die_hard()

    def _load_test_levels(self, level_ids=None, starting_level_n=0):
        log.info(f"Load test levels: {level_ids}")
        self.levels = levels.Level.factory_by_nums(
            levels_module=test_levels, game=self,
            level_ids=level_ids, level_name_prefix='LevelTest')
        self.levels_qty = len(self.levels)
        self.level_init = None
        self.level = self.levels[starting_level_n]

    def load_game_levels(self, starting_level_n=0):
        if self.level_ids:
            raise ValueError(
                f"You can load test levels or the game levels, but not both. "
                f"Also, you can load the game levels only once. "
                f"To use load_game_levels, you must leave the test levels empty.")

        gc.collect()

        self.level_ids = list(range(1, N_LEVELS + 1))
        log.info(f"Load all game levels: {self.level_ids}")
        self.levels = levels.Level.factory(levels_module=levels, game=self)
        self.levels_qty = len(self.levels)
        self.level_init = None
        self.level = self.levels[starting_level_n]

    def _tear_down(self):
        log.info("Tear Down")
        levels.Level.clean_entity_ids()
        if self.is_persist_data:
            self.clear_all_persisted_data()

    def _clock_die_hard(self):
        self.clock_timer.die_hard()
        log.info("Exit game loop triggered by the timer clock. "
                 "Test: %s", self.current_test.__name__)
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
        suite.normal_screen_flags = pg.SHOWN | pg.SCALED
        is_full_screen = Settings.is_full_screen
        suite.screen_flags = suite.full_screen_flags if is_full_screen else suite.normal_screen_flags
        suite.screen = pg.display.set_mode(suite.size, suite.screen_flags)

        log.info("Load and render resources")
        Resource.load_and_render_background_images()
        Resource.load_sound_resources()
        # Render characters in some colors to use it as a cache
        libg_jp.chars_render_text_tuple(font_name=FONT_DEFAULT_NAME)
        libg_jp.chars_render_text_tuple(font_name=FONT_FIXED_DEFAULT_NAME)
        GameTestSuite.is_log_debug = self.is_debug = is_debug
        self.is_settings_initialized_before = True

        # Load file disks data
        FilesDisk.load_files_disks_data(self)

    def _init_clock_timer(self, time_in_secs=CLOCK_TIMER_IN_SECS):
        self.clock_timer = ClockTimerA(
            0, -20,
            self, time_in_secs,
            x_centered=False, y_on_top=True,
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

    def _init_persistence_settings(self):
        self.is_persist_data = True
        PersistenceSettings.init_settings(self.persistence_path)

    def persist_game_data(self):
        self._init_persistence_settings()
        persistence.persist_game_data(self)

    def load_game_data(self):
        gc.collect()
        self.set_up_actors_and_levels()
        persistence.load_game_data(self)
        if self.__class__.is_load_last_game_failed:
            self.test_load_last_game_failed = True

    def get_is_load_last_game_failed(self):
        return self.__class__.is_load_last_game_failed

    def clear_all_persisted_data(self):
        persistence.clear_all_persisted_data()

    def _create_test_name_msg_actor(self, timeout):
        TextMsg.create(f"{IN_GAME_START_MSG}\nTest: {self.current_test.__name__}",
                       game=self,
                       owner=self.actor_test_name_holder,
                       delta_x=0, delta_y=-30,
                       time_in_secs=timeout-0.06,
                       msg_class=TextMsgActorTop)

    def assert_test_passed(self, condition, failed_msg):
        if self.aborted:
            self.test_aborted_count += 1
            self.tests_aborted += [self.current_test.__name__]
            return

        if self.test_load_last_game_failed:
            log.warning("Test FAILED: Load last game failed")
            self.tests_failed += [self.current_test.__name__]
            self.test_failed_count += 1
            return

        if not condition:
            log.warning(f"Test FAILED: {failed_msg}")
            self.tests_failed += [self.current_test.__name__]
            self.test_failed_count += 1
            return

        self.tests_passed += [self.current_test.__name__]
        self.test_passed_count += 1

    def game_loop(self, timeout=None):
        if not self.level_ids:
            log.warning("Game loop called, but there are no levels to load! "
                        "Consider to add some levels or remove the game loop call.")
            return
        if self.aborted:
            return
        if timeout is not None:
            validate_game_test_timeout(timeout)
            self.current_test_timeout = timeout
        log.info(f"Start game loop. timeout: {self.current_test_timeout}")

        self._create_test_name_msg_actor(self.current_test_timeout)
        self._init_clock_timer(self.current_test_timeout)

        self.game_loop_exec_times += 1
        self.update_state_counter = -1
        self.done = False
        while not self.done:
            self.current_time = pg.time.get_ticks()

            # Increase and check counter to delay stats x iterations
            self.update_state_counter += 1
            if self.update_state_counter > 20:
                self.update_state_counter = 0

            for event in pg.event.get():
                if event.type == pg.QUIT or \
                        (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    log.warning("Abort test by user request: "
                                "%s", self.current_test.__name__)
                    self.done = True
                    self.aborted = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_a:
                        if pg.key.get_mods() & pg.KMOD_LCTRL and pg.key.get_mods() & pg.KMOD_LALT:
                            log.warning("Abort all remaining tests by user request when testing: "
                                        "%s", self.current_test.__name__)
                            self.done = True
                            self.aborted = True
                            self.aborted_all = True

            level_scroll_shift_control(game=self)

            # Check if we hit any door
            door_hit_list = pg.sprite.spritecollide(
                self.player, self.level.doors, False)
            for door in door_hit_list:
                if not door.is_locked:
                    change_screen_level(game=self, door=door)

            execute_pc_action(self)
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
        self.tests_skipped_text = (". Tests skipped: "
                                   f"{self.test_skipped_count}") if self.test_skipped_count else ''
        self.tests_total = sum(1 for test in self.tests if not test.skip)

        log.info(LOG_START_TEST_APP_MSG)
        log.info("Total tests to pass: "
                 f"{self.tests_total}{self.tests_skipped_text}")
        pg.init()
        count = 0
        try:
            for test in tuple(self.tests):
                test_method_with_setup_levels = self.tests.pop()
                self.current_test = test_method_with_setup_levels.test_func
                if test.skip:
                    continue
                count += 1
                if self.aborted_all:
                    self.aborted = True
                    self.assert_test_passed(condition=False, failed_msg='ABORTED')
                    continue
                log.info(f"------ Test {count:2} / {self.tests_total} ------")
                self.level_ids = test_method_with_setup_levels.level_ids
                self.starting_level_n = test_method_with_setup_levels.starting_level_n
                self._set_up(is_debug=is_debug,
                             is_full_screen=is_full_screen,
                             is_set_up_actors_and_levels=self.level_ids and True or False)
                log.info(f"Start {self.current_test.__name__}")
                self.current_test_timeout = test.timeout
                self.current_test(game=self)
                self._tear_down()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            log.critical(f'Error while testing: {e}')
            self.tests_failed += [self.current_test.__name__]
            self.test_failed_count += 1
        finally:
            pg.quit()
            self._print_test_results()
            log.info(LOG_END_TEST_APP_MSG)
