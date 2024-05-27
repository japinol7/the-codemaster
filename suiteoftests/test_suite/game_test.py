"""Module game_test."""
__author__ = 'Joan A. Pinol  (japinol)'

from suiteoftests.config.constants import CLOCK_TIMER_IN_SECS, TestMethodWithSetupLevels


def game_test(*, levels, starting_level=0, timeout=CLOCK_TIMER_IN_SECS, skip=False):
    """Decorates a game test function, so it can be automatically added
    to the suite of tests.
    @param levels: List of level names to load. Each level must be an integer.
    The First level is 1, because it is based on the name of the level.
    @param starting_level: Starting level. It must be an integer. The First level is 0.
    @param timeout: Timeout in seconds for the duration of the test.
    @param skip: Skip test.
    """
    def wrapper(func):
        GameTest.add_test(
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

    _test_names_to_run = {}
    _tests = []

    def __init__(self, test_code_master):
        self.test_code_master = test_code_master
        self.add_tests_to_test_suite()

    def add_tests_to_test_suite(self):
        """Adds tests to the test suite."""

        tests = []
        for test in self.__class__._tests:
            skip = test.skip
            if self.get_test_names_to_run():
                skip = test.test.__name__ not in self.get_test_names_to_run()

            tests.append(
                TestMethodWithSetupLevels(
                    test.test,
                    test.level_name_nums, test.starting_level_n, test.timeout, skip
                    ),
                )

        self.test_code_master.add_tests(tests)

    @classmethod
    def get_test_names_to_run(cls):
        return cls._test_names_to_run

    @classmethod
    def get_test_names(cls):
        return (test.test.__name__ for test in cls._tests)

    @classmethod
    def add_test(cls, test):
        cls._tests.append(test)

    @classmethod
    def set_tests_to_run(cls, test_names):
        if not test_names:
            return

        test_names = {test_name.strip() for test_name in test_names.split(',') if test_name.strip()}
        missing_test_names = test_names - set(cls.get_test_names())

        if missing_test_names:
            if len(missing_test_names) == 1:
                raise ValueError(f"This test does not exist: {missing_test_names.pop()}")
            else:
                raise ValueError(f"These tests do not exist: {missing_test_names}")

        cls._test_names_to_run = test_names
