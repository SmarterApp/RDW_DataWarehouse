__author__ = 'tshewchuk'

"""
This module contains the unit tests for the CategoryTracker class, the base class for all category tracker classes.
"""

import unittest

from edextract.trackers.category_tracker import CategoryTracker


class TestCategoryTracker(unittest.TestCase):

    def setUp(self):
        CategoryTracker.__abstractmethods__ = set()  # Make this class instantiable for these tests only.
        self.category_tracker = CategoryTracker()

    def test_track(self):
        db_rows = [
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school1', 'academic_year': 2013},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school1', 'academic_year': 2014},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school2', 'academic_year': 2014},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school3', 'academic_year': 2013},
            {'state_code': 'NJ', 'district_guid': 'district2', 'school_guid': 'school4', 'academic_year': 2013},
            {'state_code': 'NJ', 'district_guid': 'district2', 'school_guid': 'school4', 'academic_year': 2014},
            {'state_code': 'NJ', 'district_guid': 'district2', 'school_guid': 'school5', 'academic_year': 2014},
        ]
        for row in db_rows:
            state_guid = row['state_code']
            district_guid = row['district_guid']
            school_guid = row['school_guid']
            self.category_tracker.track(state_guid, row)
            self.category_tracker.track(district_guid, row)
            self.category_tracker.track(school_guid, row)

        sorted_keys = sorted(self.category_tracker._map.keys())
        self.assertEquals(['NJ', 'district1', 'district2', 'school1', 'school2', 'school3', 'school4', 'school5'], sorted_keys)

        self.assertEquals(2, len(self.category_tracker.get_map_entry('NJ')))
        self.assertEquals(2, len(self.category_tracker.get_map_entry('district1')))
        self.assertEquals(2, len(self.category_tracker.get_map_entry('district2')))
        self.assertEquals(2, len(self.category_tracker.get_map_entry('school1')))
        self.assertEquals(1, len(self.category_tracker.get_map_entry('school2')))
        self.assertEquals(1, len(self.category_tracker.get_map_entry('school3')))
        self.assertEquals(2, len(self.category_tracker.get_map_entry('school4')))
        self.assertEquals(1, len(self.category_tracker.get_map_entry('school5')))

        self.assertEquals(3, self.category_tracker.get_map_entry('NJ')[2013])
        self.assertEquals(4, self.category_tracker.get_map_entry('NJ')[2014])
        self.assertEquals(2, self.category_tracker.get_map_entry('district1')[2013])
        self.assertEquals(2, self.category_tracker.get_map_entry('district1')[2014])
        self.assertEquals(1, self.category_tracker.get_map_entry('district2')[2013])
        self.assertEquals(2, self.category_tracker.get_map_entry('district2')[2014])
        self.assertEquals(1, self.category_tracker.get_map_entry('school1')[2013])
        self.assertEquals(1, self.category_tracker.get_map_entry('school1')[2014])
        self.assertNotIn(2013, self.category_tracker.get_map_entry('school2'))
        self.assertEquals(1, self.category_tracker.get_map_entry('school2')[2014])
        self.assertEquals(1, self.category_tracker.get_map_entry('school3')[2013])
        self.assertNotIn(2014, self.category_tracker.get_map_entry('school3'))
        self.assertEquals(1, self.category_tracker.get_map_entry('school4')[2013])
        self.assertEquals(1, self.category_tracker.get_map_entry('school4')[2014])
        self.assertNotIn(2013, self.category_tracker.get_map_entry('school5'))
        self.assertEquals(1, self.category_tracker.get_map_entry('school5')[2014])

    def test_get_map_entry_no_entry(self):
        self.assertIsNone(self.category_tracker.get_map_entry('non-guid'))
