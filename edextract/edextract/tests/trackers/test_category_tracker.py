__author__ = 'tshewchuk'

"""
This module contains the unit tests for the CategoryTracker class, the base class for all category tracker classes.
"""

import unittest

from edextract.trackers.category_tracker import CategoryTracker


class TestCategoryTracker(unittest.TestCase):

    def setUp(self):
        CategoryTracker.__abstractmethods__ = set()  # Make this class instantiable for these tests only.
        self.category_tracker = CategoryTracker(None, None)

    def test_get_map_entry_no_entry(self):
        self.assertIsNone(self.category_tracker.get_map_entry('non-guid'))
