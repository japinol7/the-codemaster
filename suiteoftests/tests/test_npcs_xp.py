"""Module test_npcs_xp.
NPCs must have no negative XP assigned to them.
"""
__author__ = 'Joan A. Pinol  (japinol)'

import inspect
import sys

from codemaster.models.actors import npcs as npcs_module
from codemaster.models.experience_points import ExperiencePoints
from suiteoftests.test_suite.game_test import game_test


@game_test(levels=[])
def test_npcs_must_have_xp_assigned_to_them(game):
    error_msgs = []
    for name, cls in inspect.getmembers(sys.modules[npcs_module.__name__]):
        if inspect.isclass(cls):
            npc = cls(1, 1, game)
            xp = ExperiencePoints.xp_points.get(npc.type.name, None)
            if xp is None:
                error_msgs += [f"KeyError('{npc.type.name}')"]
            elif xp < 0:
                error_msgs += [f"XP lower than 0: {npc.type.name}"]

    game.assert_test_passed(
        condition=not error_msgs,
        failed_msg=f"NPCs must have no negative XP assigned to them: {error_msgs}")
