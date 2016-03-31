# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

__author__ = 'tshewchuk'

"""
This module contains the unit tests for the TotalTracker class, which tracks visitor totals.
"""

import unittest

from edextract.trackers.total_tracker import TotalTracker


class TestTotalTracker(unittest.TestCase):

    def setUp(self):
        self.total_tracker = TotalTracker()

    def test_track(self):
        db_rows = [
            {'state_code': 'NJ', 'district_id': 'district1', 'school_id': 'school1', 'academic_year': 2013},
            {'state_code': 'NJ', 'district_id': 'district1', 'school_id': 'school1', 'academic_year': 2014},
            {'state_code': 'NJ', 'district_id': 'district1', 'school_id': 'school2', 'academic_year': 2014},
            {'state_code': 'NJ', 'district_id': 'district1', 'school_id': 'school3', 'academic_year': 2013},
            {'state_code': 'NJ', 'district_id': 'district2', 'school_id': 'school4', 'academic_year': 2013},
            {'state_code': 'NJ', 'district_id': 'district2', 'school_id': 'school4', 'academic_year': 2014},
            {'state_code': 'NJ', 'district_id': 'district2', 'school_id': 'school5', 'academic_year': 2014},
        ]
        for row in db_rows:
            state_guid = row['state_code']
            district_id = row['district_id']
            school_id = row['school_id']
            self.total_tracker.track_academic_year(state_guid, row)
            self.total_tracker.track_academic_year(district_id, row)
            self.total_tracker.track_academic_year(school_id, row)

        sorted_keys = sorted(self.total_tracker._data_counter.map.keys())
        self.assertEquals(['NJ', 'district1', 'district2', 'school1', 'school2', 'school3', 'school4', 'school5'], sorted_keys)

        self.assertEquals(2, len(self.total_tracker.get_map_entry('NJ')))
        self.assertEquals(2, len(self.total_tracker.get_map_entry('district1')))
        self.assertEquals(2, len(self.total_tracker.get_map_entry('district2')))
        self.assertEquals(2, len(self.total_tracker.get_map_entry('school1')))
        self.assertEquals(1, len(self.total_tracker.get_map_entry('school2')))
        self.assertEquals(1, len(self.total_tracker.get_map_entry('school3')))
        self.assertEquals(2, len(self.total_tracker.get_map_entry('school4')))
        self.assertEquals(1, len(self.total_tracker.get_map_entry('school5')))

        self.assertEquals(3, self.total_tracker.get_map_entry('NJ')[2013])
        self.assertEquals(4, self.total_tracker.get_map_entry('NJ')[2014])
        self.assertEquals(2, self.total_tracker.get_map_entry('district1')[2013])
        self.assertEquals(2, self.total_tracker.get_map_entry('district1')[2014])
        self.assertEquals(1, self.total_tracker.get_map_entry('district2')[2013])
        self.assertEquals(2, self.total_tracker.get_map_entry('district2')[2014])
        self.assertEquals(1, self.total_tracker.get_map_entry('school1')[2013])
        self.assertEquals(1, self.total_tracker.get_map_entry('school1')[2014])
        self.assertNotIn(2013, self.total_tracker.get_map_entry('school2'))
        self.assertEquals(1, self.total_tracker.get_map_entry('school2')[2014])
        self.assertEquals(1, self.total_tracker.get_map_entry('school3')[2013])
        self.assertNotIn(2014, self.total_tracker.get_map_entry('school3'))
        self.assertEquals(1, self.total_tracker.get_map_entry('school4')[2013])
        self.assertEquals(1, self.total_tracker.get_map_entry('school4')[2014])
        self.assertNotIn(2013, self.total_tracker.get_map_entry('school5'))
        self.assertEquals(1, self.total_tracker.get_map_entry('school5')[2014])
