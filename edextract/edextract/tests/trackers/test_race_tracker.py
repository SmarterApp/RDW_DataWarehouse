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

__author__ = 'npandey'

import unittest
from edextract.student_reg_extract_processors.attribute_constants import AttributeFieldConstants
from edextract.trackers.race_tracker import HispanicLatinoTracker, AmericanIndianTracker, AsianTracker, \
    AfricanAmericanTracker, PacificIslanderTracker, WhiteTracker, MultiRaceTracker


class TestRaceTracker(unittest.TestCase):
    def setUp(self):
        self.hispanic_tracker = HispanicLatinoTracker()
        self.ami_tracker = AmericanIndianTracker()
        self.asn_tracker = AsianTracker()
        self.afm_tracker = AfricanAmericanTracker()
        self.pac_tracker = PacificIslanderTracker()
        self.wht_tracker = WhiteTracker()
        self.mul_tracker = MultiRaceTracker()

        self.race_trackers = [self.hispanic_tracker, self.ami_tracker, self.asn_tracker, self.afm_tracker, self.pac_tracker,
                              self.wht_tracker, self.mul_tracker]

        self.hsp_db_rows = [
            {'state_code': 'NJ', 'district_id': 'district1', 'school_id': 'school1', 'academic_year': 2013,
             'dmg_eth_hsp': True},
            {'state_code': 'NJ', 'district_id': 'district1', 'school_id': 'school1', 'academic_year': 2014,
             'dmg_eth_hsp': True},
            {'state_code': 'NJ', 'district_id': 'district1', 'school_id': 'school2', 'academic_year': 2013,
             'dmg_eth_hsp': False},
            {'state_code': 'NJ', 'district_id': 'district1', 'school_id': 'school2', 'academic_year': 2014,
             'dmg_eth_hsp': True},
            {'state_code': 'NJ', 'district_id': 'district1', 'school_id': 'school1', 'academic_year': 2013,
             'dmg_eth_hsp': False},
            {'state_code': 'NJ', 'district_id': 'district1', 'school_id': 'school1', 'academic_year': 2014,
             'dmg_eth_hsp': False},
            {'state_code': 'NJ', 'district_id': 'district1', 'school_id': 'school2', 'academic_year': 2013,
             'dmg_eth_hsp': False},
            {'state_code': 'NJ', 'district_id': 'district1', 'school_id': 'school2', 'academic_year': 2014,
             'dmg_eth_hsp': True}
        ]

        self.race_db_rows = [
            {'state_code': 'NJ', 'district_id': 'district1', 'school_id': 'school1', 'academic_year': 2013,
             'dmg_eth_hsp': True,
             'dmg_eth_ami': True,
             'dmg_eth_asn': True,
             'dmg_eth_blk': True,
             'dmg_eth_pcf': True,
             'dmg_eth_wht': True,
             'dmg_multi_race': True},
            {'state_code': 'NJ', 'district_id': 'district1', 'school_id': 'school1', 'academic_year': 2014,
             'dmg_eth_hsp': False,
             'dmg_eth_ami': True,
             'dmg_eth_asn': False,
             'dmg_eth_blk': True,
             'dmg_eth_pcf': True,
             'dmg_eth_wht': False,
             'dmg_multi_race': False}
        ]

    def test_tracker_map_counts(self):
        for row in self.hsp_db_rows:
            self.hispanic_tracker.track_academic_year(row['state_code'], row)
            self.hispanic_tracker.track_academic_year(row['district_id'], row)
            self.hispanic_tracker.track_academic_year(row['school_id'], row)

        self.assertEqual(2, len(self.hispanic_tracker.get_map_entry('NJ')))
        self.assertEqual(2, len(self.hispanic_tracker.get_map_entry('district1')))
        self.assertEqual(2, len(self.hispanic_tracker.get_map_entry('school1')))
        self.assertEqual(1, len(self.hispanic_tracker.get_map_entry('school2')))

        self.assertEqual(1, self.hispanic_tracker.get_map_entry('NJ')[2013])
        self.assertEqual(3, self.hispanic_tracker.get_map_entry('NJ')[2014])

        self.assertEqual(1, self.hispanic_tracker.get_map_entry('district1')[2013])
        self.assertEqual(3, self.hispanic_tracker.get_map_entry('district1')[2014])

        self.assertEqual(1, self.hispanic_tracker.get_map_entry('school1')[2013])
        self.assertEqual(1, self.hispanic_tracker.get_map_entry('school1')[2014])

        self.assertEqual(2, self.hispanic_tracker.get_map_entry('school2')[2014])

    def test_race_trackers(self):
        for tracker in self.race_trackers:
            for row in self.race_db_rows:
                tracker.track_academic_year(row['state_code'], row)
                tracker.track_academic_year(row['district_id'], row)
                tracker.track_academic_year(row['school_id'], row)

        self.validate_two_years_data([self.ami_tracker, self.afm_tracker, self.pac_tracker])
        self.validate_single_year_data([self.hispanic_tracker, self.asn_tracker, self.wht_tracker, self.mul_tracker])

    def validate_two_years_data(self, trackers):
        for tracker in trackers:
            self.assertEqual(2, len(tracker.get_map_entry('NJ')))
            self.assertEqual(2, len(tracker.get_map_entry('district1')))
            self.assertEqual(2, len(tracker.get_map_entry('school1')))

            self.assertEqual(1, tracker.get_map_entry('NJ')[2013])
            self.assertEqual(1, tracker.get_map_entry('NJ')[2014])

    def validate_single_year_data(self, trackers):
        for tracker in trackers:
            self.assertEqual(1, len(tracker.get_map_entry('NJ')))
            self.assertEqual(1, len(tracker.get_map_entry('district1')))
            self.assertEqual(1, len(tracker.get_map_entry('school1')))

            self.assertEqual(1, tracker.get_map_entry('NJ')[2013])
