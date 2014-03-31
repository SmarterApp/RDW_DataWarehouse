__author__ = 'tshewchuk'

"""
This module contains the unit tests for the CategoryTracker class, the base class for all category tracker classes.
"""

import unittest

from edextract.trackers.category_tracker import CategoryTracker


class TestCategoryTracker(unittest.TestCase):

    def setUp(self):
        CategoryTracker.__abstractmethods__ = set()  # Make this class instantiable for these tests only.
        self.category_tracker = CategoryTracker('Category', 'Value')
        self.category_tracker_test_impl = CategoryTrackerTestImpl()

    def test_get_category_and_value(self):
        category, value = self.category_tracker.get_category_and_value()

        self.assertEquals('Category', category)
        self.assertEquals('Value', value)

    def test_track_should_not_increment(self):
        row = {'should_imcrement': False, 'academic_year': 2014}
        self.category_tracker_test_impl._map = {}

        self.category_tracker_test_impl.track('guid1', row)

        self.assertEquals(self.category_tracker_test_impl._map, {})

    def test_track_empty_map(self):
        row = {'should_imcrement': True, 'academic_year': 2014}
        self.category_tracker_test_impl._map = {}

        self.category_tracker_test_impl.track('guid1', row)

        self.assertEquals(self.category_tracker_test_impl._map, {'guid1': {2014: 1}})

    def test_track_map_with_other_guid(self):
        row = {'should_imcrement': True, 'academic_year': 2014}
        self.category_tracker_test_impl._map = {'guid0': {2014: 1}}

        self.category_tracker_test_impl.track('guid1', row)

        self.assertEquals(self.category_tracker_test_impl._map, {'guid0': {2014: 1}, 'guid1': {2014: 1}})

    def test_track_map_with_guid_with_other_year(self):
        row = {'should_imcrement': True, 'academic_year': 2014}
        self.category_tracker_test_impl._map = {'guid1': {2013: 10}}

        self.category_tracker_test_impl.track('guid1', row)

        self.assertEquals(self.category_tracker_test_impl._map, {'guid1': {2013: 10, 2014: 1}})

    def test_track_map_with_guid_with_year(self):
        row = {'should_imcrement': True, 'academic_year': 2014}
        self.category_tracker_test_impl._map = {'guid1': {2013: 10, 2014: 10}}

        self.category_tracker_test_impl.track('guid1', row)

        self.assertEquals(self.category_tracker_test_impl._map, {'guid1': {2013: 10, 2014: 11}})

    def test_get_map_entry_no_entry(self):
        self.assertIsNone(self.category_tracker.get_map_entry('non-guid'))


class CategoryTrackerTestImpl(CategoryTracker):

    def __init__(self):
        super().__init__('Category', 'Value')

    def should_increment(self, row):
        return row['should_imcrement']
