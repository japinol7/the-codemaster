"""Module test_pc_physics."""
__author__ = 'Joan A. Pinol  (japinol)'

from suiteoftests.test_suite.game_test import game_test

PC_FALL_DELTA_2_SECS = 100
PC_MOVE_DELTA_ON_MOV_PLAT = 200


class TestPlayerPhysics:
    """Tests player basic physics."""

    @game_test(levels=[3], timeout=2)
    def test_pc_must_fall_if_no_platform_under_them(self, game):
        player = game.player
        player_orig_y = 554
        player.rect.x, player.rect.y = 450, player_orig_y
        world_shift_top_before = game.level.world_shift_top

        game.game_loop()

        world_shift_top_delta = game.level.world_shift_top - world_shift_top_before

        game.assert_test_passed(
            condition=player.rect.y > player_orig_y + PC_FALL_DELTA_2_SECS + world_shift_top_delta,
            failed_msg="Player must fall if there is no platform under them.")

    @game_test(levels=[3], timeout=2)
    def test_pc_must_not_fall_if_platform_under_them(self, game):
        player = game.player
        player_orig_y = 478
        player.rect.x, player.rect.y = 550, player_orig_y
        world_shift_top_before = game.level.world_shift_top

        game.game_loop()

        world_shift_top_delta = game.level.world_shift_top - world_shift_top_before

        game.assert_test_passed(
            condition=player.rect.y == player_orig_y + world_shift_top_delta,
            failed_msg="Player must not fall if there is a platform under them.")

    @game_test(levels=[6], timeout=2)
    def test_pc_must_not_move_if_not_moving_platform(self, game):
        player = game.player
        player_orig_x = 450
        player.rect.x, player.rect.y = player_orig_x, 665
        world_shift_before = game.level.world_shift

        game.game_loop()

        world_shift_delta = world_shift_before - game.level.world_shift

        game.assert_test_passed(
            condition=player.rect.x == player_orig_x - world_shift_delta,
            failed_msg="Player must not move if there is no moving platform under them.")

    @game_test(levels=[6], timeout=2)
    def test_pc_must_not_move_if_not_moving_platform_scroll(self, game):
        player = game.player
        player_orig_x = 1600
        player.rect.x, player.rect.y = player_orig_x, 665
        world_shift_before = game.level.world_shift

        game.game_loop()

        world_shift_delta = world_shift_before - game.level.world_shift

        game.assert_test_passed(
            condition=player.rect.x == player_orig_x - world_shift_delta,
            failed_msg="Player must not move if there is no moving platform under them. "
                       "Horizontal scroll version.")

    @game_test(levels=[2], timeout=2)
    def test_pc_must_move_if_on_moving_platform_left(self, game):
        player = game.player
        player_orig_x = 450
        player.rect.x, player.rect.y = player_orig_x, 665
        world_shift_before = game.level.world_shift

        game.game_loop()

        world_shift_delta = world_shift_before - game.level.world_shift

        game.assert_test_passed(
            condition=player.rect.x < player_orig_x - PC_MOVE_DELTA_ON_MOV_PLAT - world_shift_delta,
            failed_msg="Player must move left if there is a left moving platform under them.")

    @game_test(levels=[7], timeout=2)
    def test_pc_must_move_if_on_moving_platform_right(self, game):
        player = game.player
        player_orig_x = 360
        player.rect.x, player.rect.y = player_orig_x, 665
        world_shift_before = game.level.world_shift

        game.game_loop()

        world_shift_delta = world_shift_before - game.level.world_shift

        game.assert_test_passed(
            condition=player.rect.x > player_orig_x + PC_MOVE_DELTA_ON_MOV_PLAT + world_shift_delta,
            failed_msg="Player must move right if there is a right moving platform under them.")

    @game_test(levels=[5], timeout=2)
    def test_pc_must_die_when_reaches_bottom_of_screen(self, game):
        player = game.player
        player.rect.x, player.rect.y = 650, 665
        player.lives = 1

        game.add_player_actions((
            ['go_right', 15],
            ['stop', 1],
            ))

        game.game_loop()

        game.assert_test_passed(
            condition=player.lives < 1,
            failed_msg="Player must die when reaches the bottom of the screen.")
