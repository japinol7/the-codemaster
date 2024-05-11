"""Module game_test."""
__author__ = 'Joan A. Pinol  (japinol)'


class GameTest:
    """Represents a game related grouping of tests.
    Its purpose is to group game tests related to each other.
    These tests should be added to the test suite using the add_tests method.
    """

    def __init__(self, test_code_master):
        self.test_code_master = test_code_master
        self.add_tests(tests=None)

    def add_tests(self, tests):
        """Adds tests to the test suite."""
        self.test_code_master.add_tests(tests)
