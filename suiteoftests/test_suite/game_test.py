"""Module game_test."""
__author__ = 'Joan A. Pinol  (japinol)'

from suiteoftests.config.constants import TestMethodWithSetupLevels


def game_test(levels, starting_level=0, timeout=6, skip=False):
    """Decorates a game test function, so it can be automatically added
    to the suite of tests.
    @param levels: List of levels to load. Each level must be an integer.
    The First level is 1, because it is based on the name of the level.
    @param starting_level: Starting level. It must be an integer. The First level is 0.
    @param timeout: Timeout in seconds for the duration of the test.
    @param skip: Skip test.
    """
    def wrapper(func):
        GameTest.tests.append(
            TestMethodWithSetupLevels(
                func,
                levels, starting_level, timeout, skip
            ),
        )
    return wrapper


class GameTest:
    """Represents a game related grouping of tests.
    Its purpose is to group game tests related to each other.
    """

    tests = []

    def __init__(self, test_code_master):
        self.test_code_master = test_code_master
        self.add_tests()

    def add_tests(self):
        """Adds tests to the test suite."""
        self.test_code_master.add_tests([test for test in self.__class__.tests])
