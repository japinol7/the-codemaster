"""Module test_code_master."""

__author__ = 'Joan A. Pinol  (japinol)'

import traceback
from collections import namedtuple

import pygame as pg

from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.items import ClockTimerA
from codemaster.models.actors.items.bullets import BulletType
from codemaster.models.actors.player import Player
from codemaster.config.constants import (
    APP_TECH_NAME,
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
from codemaster.tools.utils.queue import Queue
from suiteoftests import levels as test_levels

PLAYER_HEALTH_SUPER_HERO = 90_000
CLOCK_TIMER_IN_SECS = 10

LOG_START_TEST_APP_MSG = f"Test app {APP_TECH_NAME} version: {version.get_version()}"
LOG_END_TEST_APP_MSG = f"End Testing {APP_TECH_NAME}"

IN_GAME_START_MSG = f"Let's test app {APP_TECH_NAME}\nversion: {version.get_version()}"

GROUP_DASHES_LINE = f"{'-' * 62}"
DASHES_LINE_SHORT = f"{'-' * 20}"


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
        self.test_skipped_count = 0
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
        self.is_log_debug = True
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

    def main(self):
        pg.init()
        tests = Queue((
            TestMethodWithSetupLevels(
                self.test_fetch_two_apples,
                level_name_nums=[1], starting_level_n=0, skip=False,
                ),
            TestMethodWithSetupLevels(
                self.test_big_jump_and_fetch_1_file_disk,
                level_name_nums=[1], starting_level_n=0, skip=False,
                ),
            TestMethodWithSetupLevels(
                self.test_big_jump_and_fetch_3_batteries_n_1_disk,
                level_name_nums=[1], starting_level_n=0, skip=False,
                ),
            TestMethodWithSetupLevels(
                self.test_big_jump_and_fetch_1_life_n_7_potions_power,
                level_name_nums=[2], starting_level_n=0, skip=False,
                ),
            TestMethodWithSetupLevels(
                self.test_bat_hit_with_enough_bullets_must_die_and_give_xp,
                level_name_nums=[3], starting_level_n=0, skip=False,
                ),
            ))
        self.tests_skipped = [test.test.__name__ for test in tests if test.skip]
        self.test_skipped_count = len(self.tests_skipped)
        self.tests_skipped_text = f". Tests skipped: {self.test_skipped_count}" if self.test_skipped_count else ''

        self.tests_total = sum(1 for test in tests if not test.skip)

        log.info(LOG_START_TEST_APP_MSG)
        log.info(f"Total tests to pass: {self.tests_total}{self.tests_skipped_text}")
        try:
            for test in tuple(tests):
                test_method_with_setup_levels = tests.pop()
                if test.skip:
                    continue
                self.set_up(
                    level_name_nums=test_method_with_setup_levels.level_name_nums,
                    starting_level_n=test_method_with_setup_levels.starting_level_n)
                test_method_with_setup_levels.test()
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
        log.info(f"{self.test_passed_count} tests passed of {self.tests_total}{self.tests_skipped_text}")
        log.info(GROUP_DASHES_LINE)
        log.info(GROUP_DASHES_LINE)

    def set_up(self, level_name_nums=None, starting_level_n=0):
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

        self.load_test_levels(level_name_nums=level_name_nums, starting_level_n=starting_level_n)

        log.info("Set clock")
        self.clock = pg.time.Clock()
        self.start_time = pg.time.get_ticks()
        self.active_sprites.add(self.player)

        log.info("Level start up")
        self.level.start_up()
        self.player.level = self.level
        self.player.start_time = self.start_time
        self.player.stats['levels_visited'].add(self.level.id)

        pg.display.set_caption(f"{APP_TECH_NAME}_test_suite")

    def load_test_levels(self, level_name_nums=None, starting_level_n=0):
        log.info(f"Load test levels: {level_name_nums}")
        self.levels = levels.Level.factory_by_nums(
            levels_module=test_levels, game=self,
            level_name_nums=level_name_nums, level_name_prefix='LevelTest')
        self.levels_qty = len(self.levels)
        self.level = self.levels[starting_level_n]

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

        if self.player_actions.peek()[1] > 1:
            player_action = self.player_actions.peek()[0]
            self.player_actions.peek()[1] -= 1
        else:
            player_action = self.player_actions.pop()[0]

        player_action_methods_map = PLAYER_ACTION_METHODS_MAP[player_action]
        getattr(self.player, player_action_methods_map.method_name)(**player_action_methods_map.kwargs)

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
                    log.warning("Warning! Abort test by user request")
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

        self.player_actions = Queue((
            ['go_right', 34],
            ['jump', 5],
            ['go_right', 148],
            ['stop', 1],
            ['go_left', 4],
            ['stop', 1],
            ))

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

        self.player_actions = Queue((
            ['go_left', 15],
            ['jump', 5],
            ['go_left', 45],
            ['stop', 1],
            ))

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

        self.player_actions = Queue((
            ['go_right', 22],
            ['jump', 5],
            ['go_right', 192],
            ['stop', 1],
            ))

        self._game_loop()

        self.calc_test_result(
            failed_condition=self.player.stats['batteries'] < 3 or self.player.stats['files_disks'] < 1,
            failed_msg="Test FAILED: Player did not fetch at least 3 batteries and 1 disk.",
            test_name=test_name)

    def test_big_jump_and_fetch_1_life_n_7_potions_power(self):
        test_name = 'test_big_jump_and_fetch_1_life_n_7_potions_power'
        log.info(f"Start {test_name}")

        def player_die_hard_mock():
            self.player.stats['lives'] -= 1
            self.player.stop()
            self.player_actions = []

        self.player.rect.x = 3000
        self.player.rect.y = 500
        self.player.stats['health'] = PLAYER_HEALTH_SUPER_HERO
        self.player.stats['lives'] = 3

        self.player.die_hard = player_die_hard_mock

        TextMsg.create(f"{IN_GAME_START_MSG}\nTest: {test_name}",
                       self, time_in_secs=5)
        self._init_clock_timer(time_in_secs=4)

        self.player_actions = Queue((
            ['go_left', 22],
            ['jump', 5],
            ['go_left', 64],
            ['go_right', 12],
            ['jump', 5],
            ['go_right', 78],
            ['stop', 1],
            ))

        self._game_loop()

        self.calc_test_result(
            failed_condition=self.player.stats['lives'] < 4 or len(self.player.stats['potions_power']) < 7,
            failed_msg="Test FAILED: Player did not fetch at least 1 life recovery and 7 potions_power.",
            test_name=test_name)

    def test_bat_hit_with_enough_bullets_must_die_and_give_xp(self):
        test_name = 'test_bat_hit_with_enough_bullets_must_die_and_give_xp'
        log.info(f"Start {test_name}")
        self.player.rect.x = 240
        self.player.rect.y = 620
        self.player.stats['health'] = PLAYER_HEALTH_SUPER_HERO

        TextMsg.create(f"{IN_GAME_START_MSG}\nTest: {test_name}",
                       self, time_in_secs=5)
        self._init_clock_timer(time_in_secs=3)

        self.player_actions = Queue((
            ['shot_bullet_t3_photonic', 15],
            ))

        bat_black = [npc for npc in self.level.npcs if npc.type == ActorType.BAT_BLACK][0]

        self._game_loop()

        self.calc_test_result(
            failed_condition=bat_black.alive(),
            failed_msg="Test FAILED: Player did not kill bat.",
            test_name=test_name)
