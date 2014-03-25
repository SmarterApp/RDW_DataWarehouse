__author__ = 'tshewchuk'

"""
This module contains the unit tests for the TotalTracker class, which tracks visitor totals.
"""

import unittest

from edextract.trackers.total_tracker import TotalTracker


class TestTotalTracker(unittest.TestCase):

    def test_track(self):
        total_tracker = TotalTracker()

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
            total_tracker.track(state_guid, row)
            total_tracker.track(district_guid, row)
            total_tracker.track(school_guid, row)

        totals_map = total_tracker.get_map()

        sorted_keys = sorted(totals_map.keys())
        self.assertEquals(['NJ', 'district1', 'district2', 'school1', 'school2', 'school3', 'school4', 'school5'], sorted_keys)

        self.assertEquals(2, len(totals_map['NJ']))
        self.assertEquals(2, len(totals_map['district1']))
        self.assertEquals(2, len(totals_map['district2']))
        self.assertEquals(2, len(totals_map['school1']))
        self.assertEquals(1, len(totals_map['school2']))
        self.assertEquals(1, len(totals_map['school3']))
        self.assertEquals(2, len(totals_map['school4']))
        self.assertEquals(1, len(totals_map['school5']))

        self.assertEquals(3, totals_map['NJ'][2013])
        self.assertEquals(4, totals_map['NJ'][2014])
        self.assertEquals(2, totals_map['district1'][2013])
        self.assertEquals(2, totals_map['district1'][2014])
        self.assertEquals(1, totals_map['district2'][2013])
        self.assertEquals(2, totals_map['district2'][2014])
        self.assertEquals(1, totals_map['school1'][2013])
        self.assertEquals(1, totals_map['school1'][2014])
        self.assertNotIn(2013, totals_map['school2'])
        self.assertEquals(1, totals_map['school2'][2014])
        self.assertEquals(1, totals_map['school3'][2013])
        self.assertNotIn(2014, totals_map['school3'])
        self.assertEquals(1, totals_map['school4'][2013])
        self.assertEquals(1, totals_map['school4'][2014])
        self.assertNotIn(2013, totals_map['school5'])
        self.assertEquals(1, totals_map['school5'][2014])
