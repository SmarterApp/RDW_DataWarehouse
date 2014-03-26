__author__ = 'tshewchuk'

"""
This module contains the unit tests for the TotalTracker class, which tracks visitor totals.
"""

import unittest

from edextract.trackers.total_tracker import TotalTracker


class TestTotalTracker(unittest.TestCase):

    def test_get_category_and_value(self):
        total_tracker = TotalTracker()
        category, value = total_tracker.get_category_and_value()

        self.assertEquals('Total', category)
        self.assertEquals('Total', value)
