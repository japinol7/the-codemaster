"""Module game level_scroll_shift_control."""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import (
    SCROLL_NEAR_RIGHT_SIDE,
    SCROLL_NEAR_LEFT_SIDE,
    SCROLL_NEAR_TOP,
    SCROLL_NEAR_BOTTOM,
    NEAR_TOP,
    NEAR_BOTTOM,
    NEAR_LEFT_SIDE,
    DOOR_DEST_NL, DOOR_DEST_TL, DOOR_DEST_TR,
    DOOR_POSITION_L, DOOR_POSITION_R,
    )


def level_scroll_shift_control(game):
    # If the player gets near the right side, shift the world left (-x)
    if game.player.rect.right >= SCROLL_NEAR_RIGHT_SIDE:
        if game.level.world_shift > game.level.level_limit:
            diff = game.player.rect.right - SCROLL_NEAR_RIGHT_SIDE
            game.player.rect.right = SCROLL_NEAR_RIGHT_SIDE
            diff and game.level.shift_world(-diff)
        else:
            if game.player.rect.right > game.level.level_limit - game.player.rect.width:
                game.player.rect.right = SCROLL_NEAR_RIGHT_SIDE

    # If the player gets near the left side, shift the world right (+x)
    if game.player.rect.left <= SCROLL_NEAR_LEFT_SIDE:
        if game.level.world_shift < 0:
            diff = SCROLL_NEAR_LEFT_SIDE - game.player.rect.left
            game.player.rect.left = SCROLL_NEAR_LEFT_SIDE
            diff and game.level.shift_world(diff)
        else:
            if game.player.rect.left < NEAR_LEFT_SIDE:
                game.player.rect.left = NEAR_LEFT_SIDE

    # If the player gets near the top, shift the world to the bottom
    if game.player.rect.top <= SCROLL_NEAR_TOP:
        if game.level.world_shift_top < 0:
            diff = game.player.rect.top - SCROLL_NEAR_TOP
            game.player.rect.top = SCROLL_NEAR_TOP
            diff and game.level.shift_world_top(-diff)
        else:
            if game.player.rect.top < NEAR_TOP:
                game.player.rect.top = NEAR_TOP

    # If the player gets near the bottom, shift the world to the top
    if game.player.rect.bottom >= SCROLL_NEAR_BOTTOM:
        if game.level.world_shift_top < 1200 and game.level.world_shift_top > -900:
            diff = SCROLL_NEAR_BOTTOM - game.player.rect.bottom
            game.player.rect.bottom = SCROLL_NEAR_BOTTOM
            diff and game.level.shift_world_top(diff)
        else:
            if game.player.rect.bottom > NEAR_BOTTOM:
                game.player.rect.bottom = NEAR_BOTTOM


def change_screen_level(game, door):
    game.level_no_old = game.level_no
    game.level_no = door.level_dest
    game.level = game.levels[game.level_no]
    game.player.level = game.level

    if door.door_dest_pos == DOOR_DEST_NL and door.door_type == DOOR_POSITION_R:
        game.level.door_previous_position = DOOR_POSITION_L
        game.level.door_previous_pos_world = (
            game.level.world_start_pos_left[0], game.level.world_start_pos_left[1])
        game.level.door_previous_pos_player = (
            game.level.player_start_pos_left[0], game.level.player_start_pos_left[1])
    elif door.door_dest_pos == DOOR_DEST_NL and door.door_type == DOOR_POSITION_L:
        game.level.door_previous_position = DOOR_POSITION_R
        game.level.door_previous_pos_world = (
            game.level.world_start_pos_right[0], game.level.world_start_pos_right[1])
        game.level.door_previous_pos_player = (
        game.level.player_start_pos_right[0], game.level.player_start_pos_right[1])
    elif door.door_dest_pos == DOOR_DEST_TR:
        game.level.door_previous_position = DOOR_POSITION_L
        game.level.door_previous_pos_world = (
            game.level.world_start_pos_rtop[0], game.level.world_start_pos_rtop[1])
        game.level.door_previous_pos_player = (
            game.level.player_start_pos_rtop[0], game.level.player_start_pos_rtop[1])
    elif door.door_dest_pos == DOOR_DEST_TL:
        game.level.door_previous_position = DOOR_POSITION_L
        game.level.door_previous_pos_world = (
            game.level.world_start_pos_ltop[0], game.level.world_start_pos_ltop[1])
        game.level.door_previous_pos_player = (
            game.level.player_start_pos_ltop[0], game.level.player_start_pos_ltop[1])

    game.level.shift_world(game.level.door_previous_pos_world[0] - game.level.world_shift)
    game.level.shift_world_top(
        game.level.door_previous_pos_world[1] - game.level.world_shift_top)
    game.player.rect.x = game.level.door_previous_pos_player[0]
    game.player.rect.y = game.level.door_previous_pos_player[1]
    game.player.change_y = 0

    if game.level_no not in game.player.stats['levels_visited']:
        game.level.update_pc_enter_level()
