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
This module contains the unit tests for various program tracker classes,
which track the totals for their respective program types.
"""

import unittest

from edextract.trackers.program_tracker import (IDEAIndicatorTracker, LEPStatusTracker, Sec504StatusTracker,
                                                EconDisadvStatusTracker, MigrantStatusTracker)


class TestProgramTrackers(unittest.TestCase):

    def setUp(self):
        self.idea_tracker = IDEAIndicatorTracker()
        self.lep_tracker = LEPStatusTracker()
        self.s504_tracker = Sec504StatusTracker()
        self.econ_tracker = EconDisadvStatusTracker()
        self.migr_tracker = MigrantStatusTracker()

    def test_track(self):
        db_rows = [
            {'state_code': 'NJ', 'district_id': 'district1', 'school_id': 'school1', 'academic_year': 2013,
             'dmg_prg_iep': True, 'dmg_prg_lep': True, 'dmg_prg_504': True, 'dmg_sts_ecd': False, 'dmg_sts_mig': True},
            {'state_code': 'NJ', 'district_id': 'district1', 'school_id': 'school2', 'academic_year': 2013,
             'dmg_prg_iep': True, 'dmg_prg_lep': False, 'dmg_prg_504': True, 'dmg_sts_ecd': False, 'dmg_sts_mig': False},
            {'state_code': 'NJ', 'district_id': 'district1', 'school_id': 'school1', 'academic_year': 2014,
             'dmg_prg_iep': True, 'dmg_prg_lep': False, 'dmg_prg_504': False, 'dmg_sts_ecd': False, 'dmg_sts_mig': True},
            {'state_code': 'NJ', 'district_id': 'district1', 'school_id': 'school2', 'academic_year': 2014,
             'dmg_prg_iep': True, 'dmg_prg_lep': True, 'dmg_prg_504': False, 'dmg_sts_ecd': False, 'dmg_sts_mig': False},
        ]
        for row in db_rows:
            school_id = row['school_id']
            self.idea_tracker.track_academic_year(school_id, row)
            self.lep_tracker.track_academic_year(school_id, row)
            self.s504_tracker.track_academic_year(school_id, row)
            self.econ_tracker.track_academic_year(school_id, row)
            self.migr_tracker.track_academic_year(school_id, row)

        self.assertEquals(2, len(self.idea_tracker.get_map_entry('school1')))
        self.assertEquals(2, len(self.idea_tracker.get_map_entry('school2')))
        self.assertEquals(1, len(self.lep_tracker.get_map_entry('school1')))
        self.assertEquals(1, len(self.lep_tracker.get_map_entry('school2')))
        self.assertEquals(1, len(self.s504_tracker.get_map_entry('school1')))
        self.assertEquals(1, len(self.s504_tracker.get_map_entry('school2')))
        self.assertEquals(None, self.econ_tracker.get_map_entry('school1'))
        self.assertEquals(None, self.econ_tracker.get_map_entry('school2'))
        self.assertEquals(2, len(self.migr_tracker.get_map_entry('school1')))
        self.assertEquals(None, self.migr_tracker.get_map_entry('school2'))

        self.assertEquals(1, self.idea_tracker.get_map_entry('school1')[2013])
        self.assertEquals(1, self.idea_tracker.get_map_entry('school2')[2013])
        self.assertEquals(1, self.idea_tracker.get_map_entry('school1')[2014])
        self.assertEquals(1, self.idea_tracker.get_map_entry('school2')[2014])
        self.assertEquals(1, self.lep_tracker.get_map_entry('school1')[2013])
        self.assertNotIn(2013, self.lep_tracker.get_map_entry('school2'))
        self.assertNotIn(2014, self.lep_tracker.get_map_entry('school1'))
        self.assertEquals(1, self.lep_tracker.get_map_entry('school2')[2014])
        self.assertEquals(1, self.s504_tracker.get_map_entry('school1')[2013])
        self.assertEquals(1, self.s504_tracker.get_map_entry('school2')[2013])
        self.assertNotIn(2014, self.s504_tracker.get_map_entry('school1'))
        self.assertNotIn(2014, self.s504_tracker.get_map_entry('school2'))
        self.assertEquals(1, self.migr_tracker.get_map_entry('school1')[2013])
        self.assertEquals(1, self.migr_tracker.get_map_entry('school1')[2014])

    def test_track_blanks(self):
        db_row = {'state_code': 'NJ', 'district_id': 'district1', 'school_id': 'school1', 'academic_year': 2013,
                  'dmg_prg_504': None, 'dmg_sts_mig': None}
        self.s504_tracker.track_academic_year('NJ', db_row)
        self.migr_tracker.track_academic_year('NJ', db_row)
        self.s504_tracker.track_academic_year('district1', db_row)
        self.migr_tracker.track_academic_year('district1', db_row)
        self.s504_tracker.track_academic_year('school1', db_row)
        self.migr_tracker.track_academic_year('school1', db_row)

        self.assertEquals(None, self.s504_tracker.get_map_entry('NJ'))
        self.assertEquals(None, self.migr_tracker.get_map_entry('NJ'))
        self.assertEquals(None, self.s504_tracker.get_map_entry('district1'))
        self.assertEquals(None, self.migr_tracker.get_map_entry('district1'))
        self.assertEquals(None, self.s504_tracker.get_map_entry('school1'))
        self.assertEquals(None, self.migr_tracker.get_map_entry('school1'))
