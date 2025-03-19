"""Module game entry point."""
__author__ = 'Joan A. Pinol  (japinol)'
__all__ = ['Game']

import pygame as pg

from codemaster.tools.logger.logger import log
from codemaster.models.actors.items.bullets import BulletType
from codemaster.models.actors.items.files_disks import FilesDisk
from codemaster.tools.utils.colors import Color
from codemaster.help_info.debug_info import DebugInfo
from codemaster.help_info.help_info import HelpInfo
from codemaster import levels
from codemaster.tools.utils import utils_graphics as libg_jp
from codemaster.resources import Resource
from codemaster.score_bars import ScoreBar
from codemaster import screens
from codemaster.config.settings import Settings, DEFAULT_MUSIC_VOLUME
from codemaster.config.constants import (
    APP_NAME,
    APP_NAME_SHORT,
    APP_NAME_LONG,
    APP_NAME_DESC,
    DIRECTION_RIP,
    FONT_DEFAULT_NAME,
    FONT_FIXED_DEFAULT_NAME,
    GAME_INFO_DATA_FILE,
    MIN_TICKS_ALLOWED_TO_PAUSE_GAME,
    NEAR_BOTTOM,
    LOG_GAME_BEATEN,
    LOG_GAME_OVER,
    N_LEVELS,
    )
from codemaster.models.actors.player import Player
from codemaster.models.experience_points import ExperiencePoints
from codemaster.models.actors.selectors import SelectorA
from codemaster.level_scroll_screen import (
    level_scroll_shift_control,
    change_screen_level,
    )
from codemaster.persistence.persistence_settings import (
    PERSISTENCE_PATH_DEFAULT,
    PersistenceSettings,
    )
from codemaster.tools.utils.queue import Queue
from codemaster.persistence import persistence
from codemaster.persistence.persistence_utils import load_data_from_file
from codemaster.ui.ui_manager.ui_manager import UIManager


class Game:
    """Represents a 'The CodeMaster' game."""
    game_info_data_body_txt = ''
    is_exit_game = False
    is_over = False
    is_first_game = True
    is_load_last_game_failed = False
    is_log_debug = False
    current_game = 0
    current_time = None
    size = None
    screen = None
    screen_flags = None
    normal_screen_flags = None
    full_screen_flags = None
    ui_manager = None
    new_game = False
    files_disks_data = None

    def __init__(self, is_debug=None, is_full_screen=None,
                 is_persist_data=None, is_no_display_scaled=None):
        self.name = APP_NAME
        self.name_short = APP_NAME_SHORT
        self.name_long = APP_NAME_LONG
        self.name_desc = APP_NAME_DESC
        self.start_time = None
        self.done = None
        self.player = None
        self.players = None
        self.winner = None
        self.is_debug = is_debug
        self.is_persist_data = is_persist_data
        self.persistence_path = PERSISTENCE_PATH_DEFAULT if is_persist_data else ''
        self.persistence_path_from_user = ''
        self.is_continue_game = False
        self.is_load_user_game = False
        self.level = None
        self.level_tutorial = None
        self.levels = []
        self.level_cutscene = None
        self.cutscene_levels = []
        self.levels_qty = 0
        self.level_init = None
        self.is_paused = False
        self.is_allowed_to_pause = False
        self.is_start_screen = True
        self.is_full_screen_switch = False
        self.is_help_screen = False
        self.is_cutscene_screen = False
        self.is_exit_curr_game_confirm = False
        self.is_music_paused = False
        self.sound_effects = True
        self.show_fps = False
        self.show_grid = False
        self.current_position = False
        self.clock = None
        self.active_sprites = None
        self.clock_sprites = None
        self.text_msg_sprites = None
        self.text_msg_pc_sprites = None
        self.selector_sprites = None
        self.score_bars = None
        self.help_info = None
        self.debug_info = None
        self.current_song = 0
        self.writen_info_game_over_to_file = False
        self.level_no = 0
        self.level_no_old = None
        self.screen_start_game = None
        self.screen_exit_current_game = None
        self.screen_game_over = None
        self.screen_pause = None
        self.super_cheat = False
        self.screen_help = None
        self.mouse_pos = 0, 0
        self.is_magic_on = False
        self.update_state_counter = 0
        # Auto actor actions for cutscenes, ...
        self.pc_auto_actions = Queue()

        Game.is_exit_game = False
        if Game.current_game > 0:
            Game.is_first_game = False

        if Game.is_first_game:
            # Calculate settings
            pg_display_info = pg.display.Info()
            Settings.display_start_width = pg_display_info.current_w
            Settings.display_start_height = pg_display_info.current_h
            Settings.calculate_settings(full_screen=is_full_screen)
            # Set screen to the settings configuration
            Game.size = Settings.screen_width, Settings.screen_height
            Game.full_screen_flags = pg.FULLSCREEN if is_no_display_scaled else pg.FULLSCREEN | pg.SCALED
            Game.normal_screen_flags = pg.SHOWN if is_no_display_scaled else pg.SHOWN | pg.SCALED
            Game.screen_flags = Game.full_screen_flags if Settings.is_full_screen else Game.normal_screen_flags
            Game.screen = pg.display.set_mode(Game.size, Game.screen_flags)
            # Load and render resources
            Resource.load_and_render_background_images()
            Resource.load_and_render_scorebar_images_and_txt()
            Resource.load_sound_resources()
            Resource.load_music_song(self.current_song)

            # Render characters in some colors to use it as a cache
            libg_jp.chars_render_text_tuple(font_name=FONT_DEFAULT_NAME)
            libg_jp.chars_render_text_tuple(font_name=FONT_FIXED_DEFAULT_NAME)

            # Initialize music
            pg.mixer.music.set_volume(DEFAULT_MUSIC_VOLUME)
            pg.mixer.music.play(loops=-1)
            if self.is_music_paused:
                pg.mixer.music.pause()

            # Initialize persistence settings if necessary
            if self.is_persist_data:
                PersistenceSettings.init_settings(self.persistence_path)

            # Load file disks data
            FilesDisk.load_files_disks_data(self)

            # Load game info data body txt
            Game.game_info_data_body_txt = load_data_from_file(GAME_INFO_DATA_FILE)

            # Initialize UI
            Game.ui_manager = UIManager(self)

        FilesDisk.reset_msgs_loaded_in_disks(self)
        self.current_time_delta = pg.time.get_ticks() / 1000.0

        # Initialize screens
        self.screen_exit_current_game = screens.ScreenExitCurrentGame(self)
        self.screen_help = screens.ScreenHelp(self)
        self.screen_pause = screens.ScreenPause(self)
        self.screen_cutscene = screens.ScreenCutScene(self)
        self.screen_game_over = screens.ScreenGameOver(self)

    @staticmethod
    def set_is_exit_game(is_exit_game):
        Game.is_exit_game = is_exit_game

    def clean_game_data(self):
        self.__class__.ui_manager.clean_game_data()
        levels.Level.clean_entity_ids()
        if self.level_cutscene:
            self.level_cutscene.clean_game_data()

    def write_game_over_info_to_file(self):
        self.debug_info.print_debug_info(to_log_file=True)
        self.writen_info_game_over_to_file = True

    def put_initial_actors_on_the_board(self):
        self.player = Player('Pac', self)
        self.players = pg.sprite.Group()
        self.players.add(self.player)
        self.active_sprites = pg.sprite.Group()
        self.clock_sprites = pg.sprite.Group()
        self.text_msg_sprites = pg.sprite.Group()
        self.text_msg_pc_sprites = pg.sprite.Group()
        self.selector_sprites = pg.sprite.Group()

        # Initialize levels
        self.levels = levels.Level.factory(levels_module=levels, game=self)
        self.levels_qty = len(self.levels)
        self.level_init = None

        # Initialize cutscene levels
        self.cutscene_levels = levels.Level.factory_by_nums(
            levels_module=levels, game=self,
            level_ids=[111, 112] if self.is_debug else [111])

        if not self.is_continue_game:
            self.level_tutorial = levels.Level.factory_by_nums(
                levels_module=levels, game=self, level_ids=[101])[0]
            self.player.level = self.level_tutorial
            self.level_no = self.level_tutorial.id

        self.player.rect.x = self.level.player_start_pos_left[0]
        self.player.rect.y = self.level.player_start_pos_left[1] + 258
        self.active_sprites.add(self.player)

        self.selector_sprites.add(
            SelectorA(0, 0, self),
            )

        # Initialize persistence settings if necessary
        if self.is_persist_data:
            PersistenceSettings.init_settings(self.persistence_path_from_user or self.persistence_path)
            if self.is_continue_game:
                persistence.load_game_data(self)
            if self.is_load_user_game:
                PersistenceSettings.init_settings(self.persistence_path)

        FilesDisk.set_random_msg_to_disks_without_msg(self)

        # Start first level
        self.player.start_time = self.start_time
        if not self.level.is_tutorial:
            self.player.stats['levels_visited'].add(self.level.id)

    def clean_actors_actions(self):
        """Clean actors and player auto actions for cutscenes, ..."""
        self.pc_auto_actions = Queue()

    def add_player_actions(self, actions):
        for action in actions:
            self.pc_auto_actions.push(list(action))

    def update_screen(self):
        # Handle game screens
        if self.is_paused or self.is_full_screen_switch:
            self.player.stop()
            self.screen_pause.start_up(is_full_screen_switch=self.is_full_screen_switch)
        if self.is_help_screen:
            self.player.stop()
            self.screen_help.start_up()
        elif self.is_exit_curr_game_confirm:
            self.player.stop()
            self.screen_exit_current_game.start_up()
            if self.done:
                self.is_persist_data and not self.level.is_cutscene and persistence.persist_game_data(self)
                self.clean_game_data()
        elif self.is_cutscene_screen:
            self.player.stop()
            self.screen_cutscene.start_up(is_full_screen_switch=self.is_full_screen_switch)
        elif Game.is_over:
            self.screen_game_over.start_up()
            if not self.writen_info_game_over_to_file:
                self.write_game_over_info_to_file()
            if self.done:
                self.is_persist_data and persistence.clear_all_persisted_data()
                self.clean_game_data()
        else:
            if Game.is_over:
                Game.screen.blit(Resource.images['bg_blue_t2'], (0, 0))
            # Draw level sprites
            self.level.draw()
            if self.show_grid:
                libg_jp.draw_grid(Game.screen, Settings.cell_size, Settings.screen_width, Settings.screen_height,
                                  Settings.screen_near_top, Color.GRAY10)
            # Update score bars
            self.score_bars.update(self.level_no, self.level_no_old)

            if self.level_no != self.level_no_old:
                self.level_no_old = self.level_no
            if not Game.is_over:
                # Draw active sprites
                self.active_sprites.draw(Game.screen)
                for dragon in self.level.dragons:
                    dragon.draw()
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
                    self.selector_sprites.draw(Game.screen)

                self.level.magic_sprites.draw(Game.screen)

    def _game_loop(self):
        self.update_state_counter = -1
        while not self.done:
            self.current_time = pg.time.get_ticks()
            self.current_time_delta = pg.time.get_ticks() / 1000.0

            # Increase and check counter to delay stats x iterations
            self.update_state_counter += 1
            if self.update_state_counter > 34:
                self.update_state_counter = 0

            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.is_exit_curr_game_confirm = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_a:
                        self.player.go_left()
                    elif event.key == pg.K_d:
                        self.player.go_right()
                    elif event.key == pg.K_w:
                        self.player.jump()
                    elif event.key == pg.K_u:
                        self.player.shot_bullet(bullet_type=BulletType.T1_LASER1)
                    elif event.key == pg.K_i:
                        if pg.key.get_mods() & pg.KMOD_LCTRL \
                            and self.super_cheat and self.player.direction != DIRECTION_RIP:
                                self.player.rect.bottom = NEAR_BOTTOM - 450
                        else:
                            self.player.shot_bullet(bullet_type=BulletType.T2_LASER2)
                    elif event.key == pg.K_j:
                        self.player.shot_bullet(bullet_type=BulletType.T3_PHOTONIC)
                    elif event.key == pg.K_k:
                        self.player.shot_bullet(bullet_type=BulletType.T4_NEUTRONIC)
                    elif event.key == pg.K_LEFT:
                        self.player.go_left()
                    elif event.key == pg.K_RIGHT:
                        self.player.go_right()
                    elif event.key == pg.K_UP:
                        self.player.jump()
                    elif event.key == pg.K_KP4:
                        self.player.shot_bullet(bullet_type=BulletType.T1_LASER1)
                    elif event.key == pg.K_KP5:
                        self.player.shot_bullet(bullet_type=BulletType.T2_LASER2)
                    elif event.key == pg.K_KP1:
                        self.player.shot_bullet(bullet_type=BulletType.T3_PHOTONIC)
                    elif event.key == pg.K_KP2:
                        self.player.shot_bullet(bullet_type=BulletType.T4_NEUTRONIC)
                    elif event.key == pg.K_1:
                        self.player.choose_spell(1)
                    elif event.key == pg.K_2:
                        self.player.choose_spell(2)
                    elif event.key == pg.K_3:
                        self.player.choose_spell(3)
                    elif event.key == pg.K_4:
                        self.player.choose_spell(4)
                    elif event.key == pg.K_5:
                        self.player.choose_spell(5)
                    elif event.key == pg.K_0:
                        self.player.choose_spell(0)
                    elif event.key == pg.K_h:
                        self.player.switch_energy_shield()
                    elif event.key == pg.K_p and pg.key.get_mods() & pg.KMOD_LCTRL:
                        if (self.is_allowed_to_pause or
                                self.current_time - self.start_time > MIN_TICKS_ALLOWED_TO_PAUSE_GAME):
                            self.is_allowed_to_pause = True
                            self.is_paused = True
                    elif event.key == pg.K_m and pg.key.get_mods() & pg.KMOD_LALT:
                        self.is_music_paused = not self.is_music_paused
                        if self.is_music_paused:
                            pg.mixer.music.pause()
                        else:
                            pg.mixer.music.unpause()
                    elif event.key == pg.K_m:
                        self.is_magic_on = not self.is_magic_on
                    elif event.key == pg.K_s and pg.key.get_mods() & pg.KMOD_LALT:
                        self.sound_effects = not self.sound_effects
                        self.player.sound_effects = self.sound_effects
                    elif event.key == pg.K_F1:
                        if not self.is_exit_curr_game_confirm:
                            self.is_help_screen = not self.is_help_screen
                    elif event.key in (pg.K_KP_ENTER, pg.K_RETURN):
                        if pg.key.get_mods() & pg.KMOD_ALT and not pg.key.get_mods() & pg.KMOD_LCTRL:
                            if (self.is_allowed_to_pause or
                                    self.current_time - self.start_time > MIN_TICKS_ALLOWED_TO_PAUSE_GAME):
                                self.is_paused = True
                                self.is_full_screen_switch = True
                elif event.type == pg.KEYUP:
                    if (event.key == pg.K_a or event.key ==  pg.K_LEFT) \
                            and self.player.change_x < 0:
                        self.player.stop()
                    if (event.key == pg.K_d or event.key ==  pg.K_RIGHT) \
                            and self.player.change_x > 0:
                        self.player.stop()
                    if event.key == pg.K_INSERT:
                        self.player.drink_potion_health()
                    if event.key == pg.K_HOME:
                        self.player.eat_apple()
                    if event.key == pg.K_DELETE:
                        self.player.drink_potion_power()
                    if event.key == pg.K_r:
                        self.player.use_computer()
                        self.player.use_door_key()
                elif event.type == pg.MOUSEBUTTONDOWN \
                        and pg.mouse.get_pressed(num_buttons=3)[0]:
                    if self.is_magic_on:
                        self.mouse_pos = pg.mouse.get_pos()
                        for selector in self.selector_sprites:
                            selector.get_pointed_sprites()
                    if self.is_debug:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.mouse_pos = pg.mouse.get_pos()
                            for selector in self.selector_sprites:
                                selector.selector_copy_actor(group=self.level.npcs)
                        elif pg.key.get_mods() & pg.KMOD_LALT:
                            self.mouse_pos = pg.mouse.get_pos()
                            for selector in self.selector_sprites:
                                selector.selector_copy_actor(group=self.level.items)
                        elif pg.key.get_mods() & pg.KMOD_LSHIFT:
                            self.mouse_pos = pg.mouse.get_pos()
                            for selector in self.selector_sprites:
                                selector.selector_paste_actor()

                self.mouse_pos = pg.mouse.get_pos()

            level_scroll_shift_control(game=self)

            # Determine if the current level has been beaten
            if not self.level.completed \
                    and not (self.level.batteries or self.level.files_disks) \
                    and self.level_no < N_LEVELS:
                self.player.stats['score'] += ExperiencePoints.xp_points['level']
                self.level.completed = True
                self.is_log_debug and log.debug(
                    f"All batteries and disks from level {self.level_no + 1} recovered.")

            # Check if we hit any door
            door_hit_list = pg.sprite.spritecollide(self.player, self.level.doors, False)
            for door in door_hit_list:
                if not door.is_locked:
                    change_screen_level(game=self, door=door)

            # update sprites and level
            if not self.is_paused:
                self.active_sprites.update()
                self.level.update()

            # Check if the player has beaten or lost the game, but skip the first four iterations
            if self.update_state_counter == 4:
                if levels.Level.levels_completed_count(self) >= self.levels_qty \
                        and self.player.count_files_disks_not_read() < 1:
                    self.winner = self.player
                    log.info(LOG_GAME_BEATEN)
                if not self.player.is_alive:
                    Game.is_over = True
                    if levels.Level.levels_completed_count(self) >= self.levels_qty \
                            and self.player.count_files_disks_not_read() < 1:
                        self.winner = self.player
                        log.info(LOG_GAME_BEATEN)
                    else:
                        log.info(LOG_GAME_OVER)
                if self.winner:
                    self.player.stats['score'] += ExperiencePoints.xp_points['beat_the_game']
                    # Force updating the game screen to update the score
                    self.update_state_counter = 0
                    self.update_screen()
                if self.winner or Game.is_over:
                    Game.is_over = True

            self.update_screen()
            self.is_paused and self.clock.tick(Settings.fps_paused) or self.clock.tick(Settings.fps)
            pg.display.flip()

    def start(self):
        pg.mouse.set_visible(False)
        Game.is_exit_game = False
        Game.is_over = False
        Game.current_game += 1
        pg.display.set_caption(self.name_short)
        self.clock = pg.time.Clock()
        self.start_time = pg.time.get_ticks()
        self.done = False

        self.put_initial_actors_on_the_board()

        # Initialize score bars
        self.score_bars = ScoreBar(self)

        # Render text frequently used only if it is the first game
        if Game.is_first_game:
            Resource.render_text_frequently_used(self)

        self.help_info = HelpInfo()
        self.debug_info = DebugInfo(self.player, self)

        if not self.is_continue_game:
            self.level.update_pc_enter_level()
        else:
            self.debug_info.init_super_cheat()

        not self.done and log.info("Start game")
        self._game_loop()
