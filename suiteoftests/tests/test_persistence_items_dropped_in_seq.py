"""Module test_persistence_items_dropped_in_seq.
Tests persistence of the game state regarding items dropped
by NPCs also dropped, but in a previous load.
Example: When a mage summons an NPC who must drop
another NPC who when dies must drop an item,
the persistence system should persist not only the first
level of dropping, but all of them.
"""
__author__ = 'Joan A. Pinol  (japinol)'

from codemaster.config.constants import DIRECTION_LEFT
from codemaster.models.actors.actor_types import ActorType
from codemaster.models.actors.actors import DropItem
from codemaster.models.actors.items import PotionPower
from codemaster.models.actors.npcs import SquirrelA
from codemaster.models.actors.items.doors import Door
from suiteoftests.test_suite.game_test import game_test


@game_test(levels=[1, 2, 3], starting_level=2, timeout=1.7)
def test_persist_items_dropped_in_seq_2_lev_sq_potion(game):
    """Tests persistence for this scenario:
    * Create a squirrel that would drop a robot when dying.
    * Create a robot that would drop a power potion when dying.
    * The player moves to another level.
    * The game state is persisted and reload.
    * The player goes to the initial level.
    * The player kills the squirrel.
    * The player fetches the power potion.
    """
    player = game.player
    level_orig, level_dest = game.levels[2], game.levels[1]
    left_door = Door.get_level_doors_dest_to_level(
        level_dest=1, game=game, level_orig=2)[0]
    left_door.is_locked = False

    right_door = Door.get_level_doors_dest_to_level(
        level_dest=2, game=game, level_orig=1)[0]
    right_door.is_locked = False

    # Remove annoying demon from level dest
    level_dest.get_npcs_filtered_by_actor_type(ActorType.DEMON_MALE)[0].kill()

    # Add additional items in the levels
    potion_to_drop = DropItem(
        PotionPower, y_delta=15, **{'random_min': 100, 'random_max': 100})
    squirrel1 = SquirrelA(
        560, 685, game, change_x=0, items_to_drop=[potion_to_drop])
    squirrel1.direction = DIRECTION_LEFT
    level_orig.add_actors([squirrel1])

    # Get orig data to assert
    squirrels_lev_3_count_orig = level_orig.count_npcs_filtered_by_actor_type(
        ActorType.SQUIRREL_A)
    squirrels_lev_2_count_orig = level_dest.count_npcs_filtered_by_actor_type(
        ActorType.SQUIRREL_A)

    # Do actions and go to another level
    player.rect.x, player.rect.y = 250, 650
    player.lives = 2
    player.stats['bullets_t04'] = 4
    game.add_player_actions((
        ['go_left', 60],
        ['stop', 1],
        ))
    game.game_loop()

    # Save game and delete old variables
    game.persist_game_data()
    del squirrel1, potion_to_drop
    del player, level_orig, level_dest

    # Load previous game
    game.load_game_data()
    player = game.player
    level_orig, level_dest = game.levels[2], game.levels[1]

    # Do more actions: kill NPC and fetch dropped potion
    game.add_player_actions((
        ['go_right', 60],
        ['shot_bullet_t4_neutronic', 4],
        ['stop', 2],
        ['go_right', 60],
        ['stop', 1],
        ))
    game.game_loop(timeout=3)

    # Get data to assert
    squirrels_lev_3_count = level_orig.count_npcs_filtered_by_actor_type(
        ActorType.SQUIRREL_A)
    squirrels_lev_2_count = level_dest.count_npcs_filtered_by_actor_type(
        ActorType.SQUIRREL_A)

    game.assert_test_passed(
        condition=game.level.id == 3
                  and squirrels_lev_3_count_orig == 1 and squirrels_lev_3_count == 0
                  and squirrels_lev_2_count_orig == squirrels_lev_2_count == 0
                  and player.stats[ActorType.POTION_POWER.name] == 1
                  and len(player.stats['potions_power']) == 1,
        failed_msg="Game loaded did not set the correct state for "
                   "NPCs that can drop other NPCs that can drop items in the game.")


@game_test(levels=[1, 2, 3, 4, 5, 6, 7, 8, 9], starting_level=8, timeout=1.7)
def test_persist_items_dropped_in_seq_2_lev_robot(game):
    """Tests persistence for this scenario:
    * The starting level must have a squirrel that would drop a robot when dying.
    * The starting level must also have a dropping robot
      that would drop a power potion and a health potion when dying.
    * The player moves to another level.
    * The game state is persisted and reload.
    * The player goes to the initial level.
    * The player kills the squirrel.
    * The player kills the robot.
    * The player fetches the power potion and the health potion.
    """
    player = game.player
    level_orig, level_dest = game.levels[8], game.levels[7]
    left_door = Door.get_level_doors_dest_to_level(
        level_dest=7, game=game, level_orig=8)[0]
    left_door.is_locked = False

    right_door = Door.get_level_doors_dest_to_level(
        level_dest=8, game=game, level_orig=7)[0]
    right_door.is_locked = False

    # In the level_orig level must be a squirrel that can drop
    #  a robot that itself can drop a health potion and a power potion.

    # Get orig data to assert
    squirrels_lev_3_count_orig = level_orig.count_npcs_filtered_by_actor_type(
        ActorType.SQUIRREL_A)
    robots_lev_3_count_orig = level_orig.count_npcs_filtered_by_actor_type(
        ActorType.ROBOT_B)
    squirrels_lev_2_count_orig = level_dest.count_npcs_filtered_by_actor_type(
        ActorType.SQUIRREL_A)
    robots_lev_2_count_orig = level_dest.count_npcs_filtered_by_actor_type(
        ActorType.ROBOT_B)

    # Do actions and go to another level
    player.rect.x, player.rect.y = 250, 650
    player.lives = 2
    player.stats['bullets_t04'] = 9
    game.add_player_actions((
        ['shot_bullet_t4_neutronic', 2],
        ['stop', 30],
        ['go_left', 60],
        ['stop', 1],
        ))
    game.game_loop()

    # Get data to assert that must apply before persisting the data
    squirrels_lev_3_count_before_persist = level_orig.count_npcs_filtered_by_actor_type(
        ActorType.SQUIRREL_A)

    # Save game and delete old variables
    game.persist_game_data()
    del player, level_orig, level_dest

    # Load previous game
    game.load_game_data()
    player = game.player
    level_orig, level_dest = game.levels[8], game.levels[7]

    game.add_player_actions((
        ['go_right', 60],
        ['shot_bullet_t4_neutronic', 7],
        ['stop', 2],
        ['go_right', 60],
        ['stop', 1],
        ))
    game.game_loop(timeout=3.5)

    # Get data to assert
    squirrels_lev_3_count = level_orig.count_npcs_filtered_by_actor_type(
        ActorType.SQUIRREL_A)
    robots_lev_3_count = level_orig.count_npcs_filtered_by_actor_type(
        ActorType.ROBOT_B)
    squirrels_lev_2_count = level_dest.count_npcs_filtered_by_actor_type(
        ActorType.SQUIRREL_A)
    robots_lev_2_count = level_dest.count_npcs_filtered_by_actor_type(
        ActorType.ROBOT_B)

    game.assert_test_passed(
        condition=game.level.id == 9
                  and squirrels_lev_3_count_before_persist == 0
                  and robots_lev_3_count_orig == robots_lev_3_count == 0
                  and robots_lev_2_count_orig == robots_lev_2_count == 0
                  and squirrels_lev_3_count_orig == 1 and squirrels_lev_3_count == 0
                  and squirrels_lev_2_count_orig == squirrels_lev_2_count == 0
                  and player.stats[ActorType.POTION_POWER.name] == 1
                  and len(player.stats['potions_power']) == 1
                  and player.stats[ActorType.POTION_HEALTH.name] == 1
                  and len(player.stats['potions_health']) == 1,
        failed_msg="Game loaded did not set the correct state for "
                   "NPCs that can drop other NPCs that can drop items in the game.")
