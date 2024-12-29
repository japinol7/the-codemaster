"""Module player_auto_actions."""
__author__ = 'Joan A. Pinol  (japinol)'

from collections import namedtuple

from codemaster.config.constants import MSG_PC_DURATION
from codemaster.models.actors.items.bullets import BulletType
from codemaster.models.actors.spells import (
    LightningBoltA,
    DoomBoltA,
    DoomBoltB,
    VortexOfDoomA,
    VortexOfDoomB,
    )


PlayerActionMethodArgs = namedtuple('PlayerActionsArgs', ['method_name', 'kwargs'])
PLAYER_ACTION_METHODS_MAP = {
    'cast_lightning_bolt': PlayerActionMethodArgs(
        'cast_spell_on_target', kwargs={'spell': 'cast_lightning_bolt'}),
    'cast_doom_bolt_a': PlayerActionMethodArgs(
        'cast_spell_on_target', kwargs={'spell': 'cast_doom_bolt_a'}),
    'cast_doom_bolt_b': PlayerActionMethodArgs(
        'cast_spell_on_target', kwargs={'spell': 'cast_doom_bolt_b'}),
    'cast_vortex_of_doom_a': PlayerActionMethodArgs(
        'cast_spell_on_target', kwargs={'spell': 'cast_vortex_of_doom_a'}),
    'cast_vortex_of_doom_b': PlayerActionMethodArgs(
        'cast_spell_on_target', kwargs={'spell': 'cast_vortex_of_doom_b'}),
    'acquire_energy_shield': PlayerActionMethodArgs('acquire_energy_shield', kwargs={}),
    'switch_energy_shield': PlayerActionMethodArgs('switch_energy_shield', kwargs={}),
    'drink_potion_health': PlayerActionMethodArgs('drink_potion_health', kwargs={}),
    'drink_potion_power': PlayerActionMethodArgs('drink_potion_power', kwargs={}),
    'eat_apple': PlayerActionMethodArgs('eat_apple', kwargs={}),
    'go_right': PlayerActionMethodArgs('go_right', kwargs={}),
    'go_left': PlayerActionMethodArgs('go_left', kwargs={}),
    'go_right_slow': PlayerActionMethodArgs('go_right_slow', kwargs={}),
    'go_left_slow': PlayerActionMethodArgs('go_left_slow', kwargs={}),
    'go_right_very_slow': PlayerActionMethodArgs('go_right_very_slow', kwargs={}),
    'go_left_very_slow': PlayerActionMethodArgs('go_left_very_slow', kwargs={}),
    'jump': PlayerActionMethodArgs('jump', kwargs={}),
    'shot_bullet_t1_laser1': PlayerActionMethodArgs(
        'shot_bullet', kwargs={'bullet_type': BulletType.T1_LASER1}),
    'shot_bullet_t2_laser2': PlayerActionMethodArgs(
        'shot_bullet', kwargs={'bullet_type': BulletType.T2_LASER2}),
    'shot_bullet_t3_photonic': PlayerActionMethodArgs(
        'shot_bullet', kwargs={'bullet_type': BulletType.T3_PHOTONIC}),
    'shot_bullet_t4_neutronic': PlayerActionMethodArgs(
        'shot_bullet', kwargs={'bullet_type': BulletType.T4_NEUTRONIC}),
    'stop': PlayerActionMethodArgs('stop', kwargs={}),
    'set_magic_on': PlayerActionMethodArgs('', kwargs={}),
    'set_magic_off': PlayerActionMethodArgs('', kwargs={}),
    'leave_cutscene': PlayerActionMethodArgs('', kwargs={}),
    ':set_magic_target': PlayerActionMethodArgs(
        'set_magic_target', kwargs={'target_id': ''}),
    ':talk': PlayerActionMethodArgs(
        'talk_msg', kwargs={'msg': '', 'time_in_secs':MSG_PC_DURATION}),
    }


CAST_SPELL_ON_TARGET_CLASSES_MAP = {
    'cast_lightning_bolt': LightningBoltA,
    'cast_doom_bolt_a': DoomBoltA,
    'cast_doom_bolt_b': DoomBoltB,
    'cast_vortex_of_doom_a': VortexOfDoomA,
    'cast_vortex_of_doom_b': VortexOfDoomB,
    }


def execute_pc_action(game):
    if not game.pc_auto_actions:
        return

    if game.pc_auto_actions.peek()[1] > 1:
        player_action = game.pc_auto_actions.peek()[0]
        game.pc_auto_actions.peek()[1] -= 1
    else:
        player_action = game.pc_auto_actions.pop()[0]

    if player_action == 'set_magic_on':
        game.is_magic_on = True
        return
    elif player_action == 'set_magic_off':
        game.is_magic_on = False
        return

    # Manage actions with arguments
    if player_action[0] == ':':
        player_args = player_action[1:].split('::')
        player_action = f":{player_args[0]}"
        player_args.pop(0)
        player_action_methods_map = PLAYER_ACTION_METHODS_MAP[player_action]
        if not player_args:
            raise ValueError("Arguments missing for player action starting with ':' !")

        for player_arg in player_args:
            arg_components = player_arg.split(':=')
            arg_default_val = player_action_methods_map.kwargs[arg_components[0]]
            arg_val = arg_components[1]
            if isinstance(arg_default_val, int):
                arg_val = int(arg_val)
            elif isinstance(arg_default_val, float):
                arg_val = float(arg_val)
            player_action_methods_map.kwargs[arg_components[0]] = arg_val

        getattr(
            game.player,
            player_action_methods_map.method_name)(**player_action_methods_map.kwargs)
        return

    player_action_methods_map = PLAYER_ACTION_METHODS_MAP[player_action]

    # Manage actions that cast spells
    if player_action_methods_map.method_name == 'cast_spell_on_target':
        game.is_magic_on = True
        spell = player_action_methods_map.kwargs.get('spell')
        game.player.stats['magic_attack'] = CAST_SPELL_ON_TARGET_CLASSES_MAP.get(spell)
        if not game.player.stats['magic_attack']:
            raise ValueError("Magic attack missing. Cannot cast spell!")
        if not game.player.auto_spell_target:
            raise ValueError("Target not set. Cannot cast spell!")
        for selector in game.selector_sprites:
            selector.rect.x = game.player.auto_spell_target.rect.centerx
            selector.rect.y = game.player.auto_spell_target.rect.centery
            selector.get_pointed_sprites()
        return

    if player_action == 'leave_cutscene':
        if not game.level_cutscene:
            raise ValueError(
                f"Player action only available for cutscenes: {player_action}")
        game.level_cutscene.cutscene.update_pc_leave_level()
        return

    # Manage actions that map directly to methods
    getattr(
        game.player,
        player_action_methods_map.method_name)(**player_action_methods_map.kwargs)
