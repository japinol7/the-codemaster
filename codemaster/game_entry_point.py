"""Module game entry point."""
__author__ = 'Joan A. Pinol  (japinol)'
__all__ = ['Game']

from datetime import datetime
import logging

import pygame as pg

from codemaster.tools.logger.logger import log
from codemaster.models.actors.items.bullets import BulletType
from codemaster.tools.utils.colors import Color
from codemaster.debug_info import DebugInfo
from codemaster.help_info import HelpInfo
from codemaster import levels
from codemaster.tools.utils import utils_graphics as libg_jp, utils
from codemaster.tools.utils.utils import file_read_list
from codemaster.resources import Resource
from codemaster.score_bars import ScoreBar
from codemaster import screen
from codemaster.config.settings import Settings, DEFAULT_MUSIC_VOLUME
from codemaster.config.constants import (
    APP_NAME,
    APP_NAME_SHORT,
    APP_NAME_LONG,
    APP_NAME_DESC,
    DIRECTION_RIP,
    FONT_DEFAULT_NAME,
    FONT_FIXED_DEFAULT_NAME,
    INIT_OPTIONS_FILE,
    NEAR_BOTTOM,
    )
from codemaster.models.actors.player import Player, PL_SELF_DESTRUCTION_COUNT_DEF
from codemaster.models.actors.text_msgs import TextMsg
from codemaster.models.experience_points import ExperiencePoints
from codemaster.models.actors.actors import NPC
from codemaster.models.actors.selectors import SelectorA
from codemaster.level_scroll_screen import level_scroll_shift_control, change_screen_level


START_LEVEL = 0


class Game:
    """Represents a 'The CodeMaster' game."""
    is_exit_game = False
    is_over = False
    is_first_game = True
    current_game = 0
    current_time = None
    K_b_keydown_seconds = False
    size = None
    screen = None
    screen_flags = None
    normal_screen_flags = None
    full_screen_flags = None

    def __init__(self, is_debug=None, is_full_screen=None, is_no_display_scaled=None):
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
        self.level = None
        self.levels = []
        self.levels_qty = 0
        self.is_paused = False
        self.is_start_screen = True
        self.is_full_screen_switch = False
        self.is_help_screen = False
        self.is_exit_curr_game_confirm = False
        self.is_music_paused = False
        self.sound_effects = True
        self.show_fps = False
        self.show_grid = False
        self.current_position = False
        self.clock = False
        self.active_sprites = None
        self.clock_sprites = None
        self.text_msg_sprites = None
        self.text_msg_pc_sprites = None
        self.selector_sprites = None
        self.level_cheat = False
        self.level_cheat_to_no = False
        self.score_bars = None
        self.help_info = None
        self.debug_info = None
        self.is_log_debug = False
        self.current_song = 0
        self.writen_info_game_over_to_file = False
        self.level_no = 0
        self.level_no_old = None
        self.screen_exit_current_game = None
        self.screen_game_over = None
        self.screen_pause = None
        self.super_cheat = False
        self.screen_help = None
        self.mouse_pos = (0, 0)
        self.is_magic_on = False

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
            Game.size = [Settings.screen_width, Settings.screen_height]
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
        else:
            # Clear entity ids
            levels.Level.clean_entity_ids()

        # Initialize screens
        self.screen_exit_current_game = screen.ExitCurrentGame(self)
        self.screen_help = screen.Help(self)
        self.screen_pause = screen.Pause(self)
        self.screen_game_over = screen.GameOver(self)

    @staticmethod
    def set_is_exit_game(is_exit_game):
        Game.is_exit_game = is_exit_game

    def write_game_over_info_to_file(self):
        self.debug_info.print_debug_info(to_log_file=True)
        # TODO: scores
        # Scores.write_scores_to_file(self)
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

        init_options = file_read_list(INIT_OPTIONS_FILE, 1)
        self.super_cheat = init_options and len(init_options) > 0 and 'supercheat' in init_options[0] or False

        if self.super_cheat:
            log.info("Super cheat mode activated!")
            DebugInfo.super_cheat_superhero(self)

        self.level_no = START_LEVEL

        self.level = self.levels[self.level_no]
        self.player.level = self.level

        self.player.rect.x = self.level.player_start_pos_left[0]
        self.player.rect.y = self.level.player_start_pos_left[1]
        self.active_sprites.add(self.player)

        self.selector_sprites.add(
            SelectorA(0, 0, self),
            )

        # Start first level
        self.level.start_up()
        self.player.start_time = self.start_time
        self.player.stats['levels_visited'].add(self.level.id)

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
        elif Game.is_over:
            self.screen_game_over.start_up()
            if not self.writen_info_game_over_to_file:
                self.write_game_over_info_to_file()
        else:
            if not Game.is_over:
                Game.screen.blit(Resource.images['background'], (0, 0))
            else:
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

        self.show_fps and pg.display.set_caption(f"{self.clock.get_fps():.2f}")

    def start(self):
        Game.is_exit_game = False
        Game.is_over = False
        Game.current_game += 1
        pg.display.set_caption(self.name_short)
        self.clock = pg.time.Clock()
        self.start_time = pg.time.get_ticks()

        self.put_initial_actors_on_the_board()

        # Initialize score bars
        self.score_bars = ScoreBar(self, Game.screen)

        # Render text frequently used only if it is the first game
        if Game.is_first_game:
            Resource.render_text_frequently_used(self)

        self.help_info = HelpInfo()
        self.debug_info = DebugInfo(self.player, self)

        TextMsg.create("Ok. Let's go.\n"
                       "- Are you ready?\n- I'm not ready!\n- Are you ready?\n- I'm not ready!",
                       self, time_in_secs=4)

        # Current game loop
        self.done = False
        while not self.done:
            self.current_time = pg.time.get_ticks()
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.is_exit_curr_game_confirm = True
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        self.is_paused = True
                    if event.key == pg.K_LEFT:
                        self.player.go_left()
                    elif event.key == pg.K_RIGHT:
                        self.player.go_right()
                    elif event.key == pg.K_UP:
                        self.player.jump()
                    elif event.key == pg.K_DOWN:
                        pass
                    elif event.key == pg.K_KP4:
                        self.player.shot_bullet(bullet_type=BulletType.T1_LASER1)
                    elif event.key == pg.K_KP5:
                        self.player.shot_bullet(bullet_type=BulletType.T2_LASER2)
                    elif event.key == pg.K_KP1:
                        self.player.shot_bullet(bullet_type=BulletType.T3_PHOTONIC)
                    elif event.key == pg.K_KP2:
                        self.player.shot_bullet(bullet_type=BulletType.T4_NEUTRONIC)
                    elif event.key == pg.K_a:
                        self.player.go_left()
                    elif event.key == pg.K_d:
                        if self.is_debug and pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.debug_info.print_debug_info()
                        else:
                            self.player.go_right()
                    elif event.key == pg.K_w:
                        self.player.jump()
                    elif event.key == pg.K_s:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.sound_effects = not self.sound_effects
                            self.player.sound_effects = self.sound_effects
                    elif event.key == pg.K_u:
                        self.player.shot_bullet(bullet_type=BulletType.T1_LASER1)
                    elif event.key == pg.K_i:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            if self.super_cheat and self.player.direction != DIRECTION_RIP:
                                self.player.rect.bottom = NEAR_BOTTOM - 450
                        else:
                            self.player.shot_bullet(bullet_type=BulletType.T2_LASER2)
                    elif event.key == pg.K_j:
                        self.player.shot_bullet(bullet_type=BulletType.T3_PHOTONIC)
                    elif event.key == pg.K_k:
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
                    elif event.key == pg.K_m:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.is_music_paused = not self.is_music_paused
                            if self.is_music_paused:
                                pg.mixer.music.pause()
                            else:
                                pg.mixer.music.unpause()
                        else:
                            self.is_magic_on = not self.is_magic_on
                    elif event.key == pg.K_n:
                        if self.is_debug and pg.key.get_mods() & pg.KMOD_LCTRL and pg.key.get_mods() & pg.KMOD_LSHIFT:
                            log.info("NPCs health from all levels, ordered by NPC name:")
                            self.is_log_debug and log.debug(
                                utils.pretty_dict_to_string(NPC.get_npcs_health(self, sorted_by_level=False)))
                        elif self.is_debug and pg.key.get_mods() & pg.KMOD_LCTRL:
                            log.info("NPCs health from all levels, ordered by level:")
                            self.is_log_debug and log.debug(
                                utils.pretty_dict_to_string(NPC.get_npcs_health(self)))
                    elif event.key == pg.K_h:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.help_info.print_help_keys()
                            self.is_debug and self.debug_info.print_help_keys()
                            self.super_cheat and self.debug_info.print_supercheat_keys()
                        else:
                            self.player.switch_energy_shield()
                    elif event.key == pg.K_l:
                        if self.is_debug and pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.debug_info.print_debug_info(to_log_file=True)
                    elif event.key == pg.K_F1:
                        if not self.is_exit_curr_game_confirm:
                            self.is_help_screen = not self.is_help_screen
                    elif event.key == pg.K_g:
                        if self.is_debug and pg.key.get_mods() & pg.KMOD_LCTRL \
                                and pg.key.get_mods() & pg.KMOD_RALT:
                            self.show_grid = not self.show_grid
                    elif event.key in (pg.K_KP_ENTER, pg.K_RETURN):
                        if pg.key.get_mods() & pg.KMOD_LALT:
                            self.is_paused = True
                            self.is_full_screen_switch = True
                    elif event.key == pg.K_KP_DIVIDE:
                        if self.is_debug and pg.key.get_mods() & pg.KMOD_LCTRL \
                                and pg.key.get_mods() & pg.KMOD_LALT:
                            if log.level != logging.DEBUG:
                                log.setLevel(logging.DEBUG)
                                self.is_log_debug = True
                                log.info("Set logger level to: Debug")
                            else:
                                log.setLevel(logging.INFO)
                                self.is_log_debug = False
                                log.info("Set logger level to: Info")
                    elif event.key == pg.K_KP_MINUS:
                        if self.super_cheat and pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.debug_info.super_cheat_superhero()
                            log.info(f"Replenish stats to superhero maximum (cheat).")
                    elif event.key == pg.K_KP_MULTIPLY:
                        if self.super_cheat and pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.player.invulnerable = not self.player.invulnerable
                            log.info(f"Set player invulnerability state to: {self.player.invulnerable} (cheat)")
                    elif event.key == pg.K_b:
                        if not self.K_b_keydown_seconds:
                            t = datetime.now().time()
                            self.K_b_keydown_seconds = (t.hour * 60 + t.minute) * 60 + t.second
                elif event.type == pg.KEYUP:
                    if event.key in (pg.K_LEFT, pg.K_a) and self.player.change_x < 0:
                        self.player.stop()
                    if event.key in (pg.K_RIGHT, pg.K_d) and self.player.change_x > 0:
                        self.player.stop()
                    if event.key == pg.K_INSERT:
                        self.player.drink_potion_health()
                    if event.key == pg.K_HOME:
                        self.player.eat_apple()
                    if event.key == pg.K_DELETE:
                        self.player.drink_potion_power()
                    if event.key == pg.K_t:
                        self.player.use_door_key()
                    if event.key == pg.K_b:
                        t = datetime.now().time()
                        if ((t.hour * 60 + t.minute) * 60 + t.second) - self.K_b_keydown_seconds >= PL_SELF_DESTRUCTION_COUNT_DEF:
                            self.player.self_destruction()
                            self.K_b_keydown_seconds = 0
                    if event.key == pg.K_F5:
                        self.show_fps = not self.show_fps
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if self.is_magic_on:
                        self.mouse_pos = pg.mouse.get_pos()
                        for selector in self.selector_sprites:
                            selector.get_pointed_sprites()
                self.mouse_pos = pg.mouse.get_pos()

            level_scroll_shift_control(game=self)

            # If the player gets all the batteries and files, level completed
            if not self.level.completed and not (
                    self.level.batteries or self.level.files_disks):
                self.player.stats['score'] += ExperiencePoints.xp_points['level']
                self.level.completed = True
                log.info(f"All batteries and disks from level {self.level_no + 1} recovered.")

            # Check if we hit any door
            door_hit_list = pg.sprite.spritecollide(self.player, self.level.doors, False)
            for door in door_hit_list:
                if not door.is_locked:
                    change_screen_level(game=self, door=door)

            # update sprites and level
            if not self.is_paused:
                self.active_sprites.update()
                self.level.update()

            # Check if the player has beaten the game, that is, if he has completed all levels
            if len(levels.Level.levels_completed(self)) >= self.levels_qty:
                self.winner = self.player
            if not self.player.is_alive:
                Game.is_over = True
                if len(levels.Level.levels_completed(self)) >= self.levels_qty:
                    self.winner = self.player
            if self.winner or Game.is_over:
                Game.is_over = True

            self.update_screen()
            if Settings.screen_scale != 1:
                libg_jp.screen_change_scale(self)
            self.is_paused and self.clock.tick(Settings.fps_paused) or self.clock.tick(Settings.fps)
            pg.display.flip()
