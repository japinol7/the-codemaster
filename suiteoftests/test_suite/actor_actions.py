"""Module actor_actions."""
__author__ = 'Joan A. Pinol  (japinol)'

from collections import namedtuple

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
    'go_right': PlayerActionMethodArgs('go_right', kwargs={}),
    'go_left': PlayerActionMethodArgs('go_left', kwargs={}),
    'jump': PlayerActionMethodArgs('jump', kwargs={}),
    'shot_bullet_t3_photonic': PlayerActionMethodArgs(
        'shot_bullet', kwargs={'bullet_type': BulletType.T3_PHOTONIC}),
    'stop': PlayerActionMethodArgs('stop', kwargs={}),
    }


CAST_SPELL_ON_TARGET_CLASSES_MAP = {
    'cast_lightning_bolt': LightningBoltA,
    'cast_doom_bolt_a': DoomBoltA,
    'cast_doom_bolt_b': DoomBoltB,
    'cast_vortex_of_doom_a': VortexOfDoomA,
    'cast_vortex_of_doom_b': VortexOfDoomB,
    }
