"""Module game_test."""
__author__ = 'Joan A. Pinol  (japinol)'

from collections.abc import Iterable

from suiteoftests.config.constants import (
    CLOCK_TIMER_IN_SECS,
    TEST_GAME_LOOP_TIMEOUT_MIN,
    TEST_GAME_LOOP_TIMEOUT_MAX,
    TestFuncWithSetupLevels,
    )


def game_test(*, levels, starting_level=0, timeout=CLOCK_TIMER_IN_SECS, skip=False):
    """Decorates a game test function, so it can be automatically added
    to the suite of tests.
    This decorator should not be used with methods, only with functions.
    @param levels: List of level ids to load.
    Each level must be an integer.
    If you leave the iterable empty, no level will be loaded.
    The First level is 1, because it is based on the id of the level.
    @param starting_level: Starting level. It must be an integer.
    The First level is 0, because it is based on the position of the level
    in the iterable argument 'levels'.
    @param timeout: Timeout in seconds for the duration of the game loop.
    @param skip: Skip this test if true.
    """
    _validate_game_test_arguments(levels, starting_level, timeout, skip)

    def wrapper(func):
        GameTest.add_test(
            TestFuncWithSetupLevels(
                func,
                levels, starting_level, timeout, skip
                ),
            )
    return wrapper


def _validate_game_test_arguments(levels, starting_level, timeout, skip):
    if not isinstance(levels, Iterable):
        raise TypeError("Argument must be an empty iterable or an iterable of integers: levels.")
    if any(not isinstance(level, int) for level in levels):
        raise TypeError("Argument must be an empty iterable or an iterable of integers: levels.")
    if not isinstance(starting_level, int):
        raise TypeError("Argument must be an int: starting_level.")
    if not isinstance(skip, bool):
        raise TypeError("Argument must be a bool: skip.")
    validate_game_test_timeout(timeout)


def validate_game_test_timeout(timeout):
    if (not isinstance(timeout, (int, float))
            or timeout < TEST_GAME_LOOP_TIMEOUT_MIN
            or timeout > TEST_GAME_LOOP_TIMEOUT_MAX):
        raise TypeError(
            "Argument must be an int or float between "
            f"{TEST_GAME_LOOP_TIMEOUT_MIN} and "
            f"{TEST_GAME_LOOP_TIMEOUT_MAX} seconds: timeout.")


class GameTest:
    """Represents a game related collection of tests.
    Its purpose is to manage the addition of the game tests
    to the test suite framework.
    """

    _test_names_to_run = {}
    _tests = []

    def __init__(self, test_code_master):
        self.test_code_master = test_code_master
        self._add_tests_to_test_suite()

    @classmethod
    def add_test(cls, test):
        if test.test_func.__name__ in cls.get_test_names():
            raise ValueError("This test function name has been used more than once: "
                             f"{test.test_func.__name__}")
        cls._tests.append(test)

    @classmethod
    def get_test_names_to_run(cls):
        return cls._test_names_to_run

    @classmethod
    def get_test_names(cls):
        return (test.test_func.__name__ for test in cls._tests)

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

    def _add_tests_to_test_suite(self):
        """Adds tests to the test suite."""

        tests = []
        for test in self.__class__._tests:
            skip = test.skip
            if self.get_test_names_to_run():
                skip = test.test_func.__name__ not in self.get_test_names_to_run()

            tests.append(
                TestFuncWithSetupLevels(
                    test.test_func,
                    test.level_ids, test.starting_level_n, test.timeout, skip
                    ),
                )

        self.test_code_master.add_tests(tests)
