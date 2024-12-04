"""Module screen."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.tools.utils.colors import Color
from codemaster.tools.utils import utils_graphics as libg_jp
from codemaster.resources import Resource
from codemaster.config.constants import APP_NAME_DESC
from codemaster.config.settings import Settings
from codemaster.screen import screen


class ExitCurrentGame(screen.ExitCurrentGame):

    def _draw(self):
        super()._draw()
        self.game.screen.blit(Resource.images['bg_blue_t1'], (0, 0))
        self.game.screen.blit(*Resource.txt_surfaces['exit_current_game_confirm'])
        self.game.screen.blit(*Resource.txt_surfaces['press_intro_to_continue_2'])
        self.game.screen.blit(
            Resource.images['seal_just_a_demo'],
            (Settings.screen_width // 2 - Resource.images['seal_just_a_demo'].get_width() // 2,
             Settings.screen_height // 1.05 - Resource.images['seal_just_a_demo'].get_height() // 1.05
             ))


class GameOver(screen.GameOver):

    def _draw(self):
        super()._draw()
        self.game.screen.blit(self.background_screenshot, (0, 0))
        if self.game.is_over and not self.game.winner:
            self.game.screen.blit(*Resource.txt_surfaces['game_over'])
            self.game.screen.blit(*Resource.txt_surfaces['game_over_2'])
        else:
            self.game.screen.blit(*Resource.txt_surfaces['congrats'])
            self.game.screen.blit(*Resource.txt_surfaces['congrats_2'])
            self.game.screen.blit(*Resource.txt_surfaces['you_have_beaten_the_game'])
            self.game.screen.blit(*Resource.txt_surfaces['you_have_beaten_the_game_2'])
        self.game.screen.blit(*Resource.txt_surfaces['press_intro_to_continue'])
        self.game.screen.blit(*Resource.txt_surfaces['press_intro_to_continue_2'])


class Pause(screen.Pause):

    def _draw(self):
        super()._draw()
        self.game.screen.blit(self.background_screenshot, (0, 0))
        self.game.screen.blit(*Resource.txt_surfaces['game_paused'])


class Help(screen.Help):

    def _draw(self):
        super()._draw()
        self.game.screen.blit(Resource.images['bg_blue_t1'], (0, 0))
        self.game.screen.blit(Resource.images['screen_help'],
                              (Settings.screen_width // 2 - Resource.images['screen_help'].get_width() // 2,
                               Settings.screen_height // 2 - Resource.images['screen_help'].get_height() // 2))


class StartGame(screen.StartGame):

    def __init__(self, game):
        super().__init__(game)

        text_size_multiplier = 38 if self.game.is_persist_data else 42
        text_start_game_pos_factor_y = 1.96 if self.game.is_persist_data else 1.82

        libg_jp.render_text(
            '– Press Ctrl + Alt + Enter to Start –', Settings.screen_width // 2,
                114 * Settings.font_pos_factor_t2 + Settings.screen_height // text_start_game_pos_factor_y,
                Resource.txt_surfaces, 'game_start', color=Color.CYAN,
                size=int(text_size_multiplier*Settings.font_pos_factor_t2), align="center")
        libg_jp.render_text(
            '– Press Ctrl + Alt + Space to Continue Last Game –', Settings.screen_width // 2,
                114 * Settings.font_pos_factor_t2 + Settings.screen_height // 1.7,
                Resource.txt_surfaces, 'game_continue_last', color=Color.CYAN,
                size=int(text_size_multiplier*Settings.font_pos_factor_t2), align="center")
        libg_jp.render_text(
            '– Load Last Game Failed. Maybe last game ended as Game Over or a Win ? –',
                Settings.screen_width // 2,
                114 * Settings.font_pos_factor_t2 + Settings.screen_height // 1.7,
                Resource.txt_surfaces, 'game_continue_last_failed', color=Color.RED_DARK,
                size=int(33*Settings.font_pos_factor_t2), align="center")
        libg_jp.render_text(
                APP_NAME_DESC, Settings.screen_width // 2,
                114 * Settings.font_pos_factor_t2 + Settings.screen_height // 1.38,
                Resource.txt_surfaces, 'game_copyright_desc', color=Color.RED_DARK,
                size=int(19*Settings.font_pos_factor_t2), align="center")

    def _draw(self):
        super()._draw()
        self.game.screen.blit(Resource.images['bg_black_t1'], (0, 0))
        self.game.screen.blit(
            Resource.images['screen_start'],
            (Settings.screen_width // 2 - Resource.images['screen_start'].get_width() // 2, 0))
        self.game.screen.blit(
            Resource.images['help_key'],
            (50 * Settings.font_pos_factor,
             Settings.screen_height - Resource.images['help_key'].get_height()
             - 28 * Settings.font_pos_factor))
        self.game.screen.blit(
            Resource.images['logo_jp'],
            (Settings.screen_width - Resource.images['logo_jp'].get_width()
             - 44 * Settings.font_pos_factor,
             Settings.screen_height - Resource.images['logo_jp'].get_height()
             - 32 * Settings.font_pos_factor))
        self.game.screen.blit(
            Resource.images['seal_just_a_demo'],
            (Settings.screen_width // 2 - Resource.images['seal_just_a_demo'].get_width() // 2,
             Settings.screen_height // 1.05 - Resource.images['seal_just_a_demo'].get_height() // 1.05))
        self.game.screen.blit(*Resource.txt_surfaces['game_copyright_desc'])
        self.game.screen.blit(*Resource.txt_surfaces['game_start'])

        if self.game.is_persist_data:
            if self.game.is_load_last_game_failed:
                self.game.screen.blit(*Resource.txt_surfaces['game_continue_last_failed'])
            else:
                self.game.screen.blit(*Resource.txt_surfaces['game_continue_last'])
