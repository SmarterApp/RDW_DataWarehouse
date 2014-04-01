__author__ = 'tshewchuk'

"""
This module contains the unit tests for the CategoryTracker class, the base class for all category tracker classes.
"""

import unittest

from edextract.trackers.category_tracker import CategoryTracker


class TestCategoryTracker(unittest.TestCase):

    def test_get_category_and_value(self):
        ct = DummyCategoryTracker()
        category, value = ct.get_category_and_value()

        self.assertEquals('Category', category)
        self.assertEquals('Value', value)

    def test_should_not_track(self):
        ct = DummyCategoryTracker(False)

        self.assertIsNone(ct.get_map_entry('guid1'), 'Tracker returned unexpected entry')

        ct.track('guid2', {'academic_year': 2015})

        self.assertIsNone(ct.get_map_entry('guid1'), 'Tracker returned unexpected entry')

    def test_positive_track(self):
        ct = DummyCategoryTracker()

        self.assertIsNone(ct.get_map_entry('guid1'), 'Tracker returned unexpected entry')

        ct.track('guid1', {'academic_year': 2014})

        self.assertIsNotNone(ct.get_map_entry('guid1'), 'Tracker does not have expected entry')
        self.assertEqual(1, len(ct.get_map_entry('guid1')), 'Tracker returned unexpected entry')
        self.assertEqual(1, ct.get_map_entry('guid1')[2014], 'Tracker does not have expected entry')

        ct.track('guid1', {'academic_year': 2014})
        self.assertEqual(2, ct.get_map_entry('guid1')[2014], 'Tracker does not have expected entry')

        ct.track('guid1', {'academic_year': 2015})
        self.assertEqual(2, len(ct.get_map_entry('guid1')), 'Tracker returned unexpected entry')
        self.assertEqual(2, ct.get_map_entry('guid1')[2014], 'Tracker does not have expected entry')
        self.assertEqual(1, ct.get_map_entry('guid1')[2015], 'Tracker does not have expected entry')

        self.assertIsNone(ct.get_map_entry('guid2'), 'Tracker returned unexpected entry')

        ct.track('guid2', {'academic_year': 2016})
        self.assertEqual(1, len(ct.get_map_entry('guid2')), 'Tracker returned unexpected entry')
        self.assertEqual(1, ct.get_map_entry('guid2')[2016], 'Tracker does not have expected entry')
        self.assertEqual(2, len(ct.get_map_entry('guid1')), 'Tracker returned unexpected entry')
        self.assertEqual(2, ct.get_map_entry('guid1')[2014], 'Tracker does not have expected entry')

    def test_positive_matched_track(self):
        ct = DummyCategoryTracker()

        ct.track('guid1', {}, 'matched_ids')
        self.assertEqual(1, len(ct.get_map_entry('guid1')), 'Tracker returned unexpected entry')
        self.assertEqual(1, ct.get_map_entry('guid1')['matched_ids'], 'Tracker does not have expected entry')

        ct.track('guid1', {}, 'matched_ids')
        self.assertEqual(1, len(ct.get_map_entry('guid1')), 'Tracker returned unexpected entry')
        self.assertEqual(2, ct.get_map_entry('guid1')['matched_ids'], 'Tracker does not have expected entry')

        ct.track('guid2', {}, 'matched_ids')
        self.assertEqual(1, len(ct.get_map_entry('guid2')), 'Tracker returned unexpected entry')
        self.assertEqual(1, ct.get_map_entry('guid2')['matched_ids'], 'Tracker does not have expected entry')
        self.assertEqual(1, len(ct.get_map_entry('guid1')), 'Tracker returned unexpected entry')
        self.assertEqual(2, ct.get_map_entry('guid1')['matched_ids'], 'Tracker does not have expected entry')

    def test_matched_should_not_track(self):
        ct = DummyCategoryTracker(False)

        self.assertIsNone(ct.get_map_entry('guid1'), 'Tracker returned unexpected entry')

        ct.track('guid1', {}, 'matched_ids')

        self.assertIsNone(ct.get_map_entry('guid1'), 'Tracker returned unexpected entry')


class DummyCategoryTracker(CategoryTracker):

    def __init__(self, should_increment_fl=True):
        super().__init__('Category', 'Value')
        self.should_increment_fl = should_increment_fl

    def should_increment_year(self, row):
        return self.should_increment_fl

    def should_increment_matched_ids(self, row):
        return self.should_increment_fl
