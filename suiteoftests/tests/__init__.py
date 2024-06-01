"""Package tests.
Import here the test classes which you want to run.
They will be executed by importation order.
"""
__author__ = 'Joan A. Pinol  (japinol)'

from suiteoftests.tests.test_player_fetches_items import TestPlayerFetchesItems
from suiteoftests.tests.test_player_big_jump import TestPlayerBigJump
from suiteoftests.tests.test_player_shoots_npcs import TestPlayerShootsNPCs
from suiteoftests.tests.test_player_casts_co_spells_on_npcs import TestPlayerCastsCoSpellsOnNPCs
from suiteoftests.tests.test_npcs_shoot_player import TestNPCsShootPlayer
from suiteoftests.tests.test_npcs_cast_spells_on_player import TestNPCsCastSpellsOnPlayer
from suiteoftests.tests.test_mines_and_explosions import TestMinesAndExplosions
from suiteoftests.tests.test_energy_shield import TestEnergyShield
from suiteoftests.tests.test_player_enters_door_level import TestPlayerEntersDoorLevel
from suiteoftests.tests.test_player_consumes_stuff import TestPlayerConsumesStuff
