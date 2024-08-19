"""Module magic."""
__author__ = 'Joan A. Pinol  (japinol)'

from random import randint

from codemaster.models.actors.actor_types import ActorType
from codemaster.config.constants import DIRECTION_LEFT
from codemaster.models.actors.spells import (
    DoomBoltA,
    DoomBoltB,
    DrainLifeA,
    DrainLifeB,
    FireBreathA,
    FireBreathB,
    LightningBoltA,
    MutentrinosBoltA,
    MutentrinosBoltB,
    NeutrinosBoltA,
    NeutrinosBoltB,
    SamutrinosBoltA,
    SamutrinosBoltB,
    VortexOfDoomA,
    VortexOfDoomB,
    )
from codemaster.tools.logger.logger import log

SPELL_ACTOR_TYPE_MAPPING = {
    ActorType.DOOM_BOLT_A.name: DoomBoltA,
    ActorType.DOOM_BOLT_B.name: DoomBoltB,
    ActorType.DRAIN_LIFE_A.name: DrainLifeA,
    ActorType.DRAIN_LIFE_B.name: DrainLifeB,
    ActorType.FIRE_BREATH_A.name: FireBreathA,
    ActorType.FIRE_BREATH_B.name: FireBreathB,
    ActorType.LIGHTNING_BOLT_A.name: LightningBoltA,
    ActorType.MUTENTRINOS_BOLT_A.name: MutentrinosBoltA,
    ActorType.MUTENTRINOS_BOLT_B.name: MutentrinosBoltB,
    ActorType.NEUTRINOS_BOLT_A.name: NeutrinosBoltA,
    ActorType.NEUTRINOS_BOLT_B.name: NeutrinosBoltB,
    ActorType.SAMUTRINOS_BOLT_A.name: SamutrinosBoltA,
    ActorType.SAMUTRINOS_BOLT_B.name: SamutrinosBoltB,
    ActorType.VORTEX_OF_DOOM_A.name: VortexOfDoomA,
    ActorType.VORTEX_OF_DOOM_B.name: VortexOfDoomB,
    }

MAX_SPELLS_ON_TARGET = 15
MAX_SPELLS_ON_LEVEL = 200


def create_spell(spell_type_name, x, y, game, is_from_player_shot, owner, target):
    spell_class = SPELL_ACTOR_TYPE_MAPPING.get(spell_type_name)

    if not owner.can_cast_spells:
        raise ValueError("Cannot create spell. Owner cannot cast spells: "
                         f"{owner.id}")
    if not spell_class:
        raise ValueError("Cannot create spell. Missing spell actor type mapping: "
                         f"{spell_type_name}")
    if game.player.target_of_spells_count[spell_class.__name__] > MAX_SPELLS_ON_TARGET:
        log.warning("Cannot create spell. Max spells on target: "
                    f"{target.id}. Spell: {spell_type_name}")
        return
    if game.level.spells_on_level_count[spell_class.__base__.__name__] > MAX_SPELLS_ON_LEVEL:
        log.warning(f"Cannot create spell. Max spells on level: {spell_type_name}")
        return

    magic_attack = spell_class(
        x, y, game,
        is_from_player_shot=is_from_player_shot, owner=owner,
        target=target)

    game.level.magic_sprites.add(magic_attack)
    game.player.target_of_spells_count[spell_class.__name__] += 1
    game.level.spells_on_level_count[spell_class.__base__.__name__] += 1


def update_cast_spell_cast_actions(actor, delta_x=0, delta_y=0):
    dice_shot = randint(1, 100)
    if all((
            dice_shot + actor.probability_to_cast_spell_1 > 100,
            sum(1 for x in actor.game.level.magic_sprites
                if x.target == actor.player and x.type.name == actor.spell_1_name) < actor.max_multi_spell_1,
    )):
        spell_name = actor.spell_1_name
    elif all((
            dice_shot + actor.probability_to_cast_spell_2 > 100,
            sum(1 for x in actor.game.level.magic_sprites
                if x.target == actor.player and x.type.name == actor.spell_2_name) < actor.max_multi_spell_2,
    )):
        spell_name = actor.spell_2_name
    else:
        return

    dx = -10 - delta_x if actor.direction == DIRECTION_LEFT else 20 + delta_x
    create_spell(
        spell_name,
        actor.rect.x+dx, actor.rect.y+22+delta_y, actor.game,
        is_from_player_shot=False, owner=actor,
        target=actor.player)


def update_cast_spell_cast_actions_3_spells(actor, delta_x=0, delta_y=0):
    dice_shot = randint(1, 100)
    if all((
            dice_shot + actor.probability_to_cast_spell_1 > 100,
            sum(1 for x in actor.game.level.magic_sprites
                if x.target == actor.player and x.type.name == actor.spell_1_name) < actor.max_multi_spell_1,
    )):
        spell_name = actor.spell_1_name
    elif all((
            dice_shot + actor.probability_to_cast_spell_2 > 100,
            sum(1 for x in actor.game.level.magic_sprites
                if x.target == actor.player and x.type.name == actor.spell_2_name) < actor.max_multi_spell_2,
    )):
        spell_name = actor.spell_2_name
    elif all((
        dice_shot + actor.probability_to_cast_spell_3 > 100,
        sum(1 for x in actor.game.level.magic_sprites
            if x.target == actor.player and x.type.name == actor.spell_3_name) < actor.max_multi_spell_3,
    )):
        spell_name = actor.spell_3_name
    else:
        return

    dx = -10 - delta_x if actor.direction == DIRECTION_LEFT else 20 + delta_x
    create_spell(
        spell_name,
        actor.rect.x+dx, actor.rect.y+22+delta_y, actor.game,
        is_from_player_shot=False, owner=actor,
        target=actor.player)
