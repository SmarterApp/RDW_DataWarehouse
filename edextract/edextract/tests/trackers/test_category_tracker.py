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

        ct.track_academic_year('guid2', {'academic_year': 2015})

        self.assertIsNone(ct.get_map_entry('guid1'), 'Tracker returned unexpected entry')

    def test_positive_track(self):
        ct = DummyCategoryTracker()

        self.assertIsNone(ct.get_map_entry('guid1'), 'Tracker returned unexpected entry')

        ct.track_academic_year('guid1', {'academic_year': 2014})

        self.assertIsNotNone(ct.get_map_entry('guid1'), 'Tracker does not have expected entry')
        self.assertEqual(1, len(ct.get_map_entry('guid1')), 'Tracker returned unexpected entry')
        self.assertEqual(1, ct.get_map_entry('guid1')[2014], 'Tracker does not have expected entry')

        ct.track_academic_year('guid1', {'academic_year': 2014})
        self.assertEqual(2, ct.get_map_entry('guid1')[2014], 'Tracker does not have expected entry')

        ct.track_academic_year('guid1', {'academic_year': 2015})
        self.assertEqual(2, len(ct.get_map_entry('guid1')), 'Tracker returned unexpected entry')
        self.assertEqual(2, ct.get_map_entry('guid1')[2014], 'Tracker does not have expected entry')
        self.assertEqual(1, ct.get_map_entry('guid1')[2015], 'Tracker does not have expected entry')

        self.assertIsNone(ct.get_map_entry('guid2'), 'Tracker returned unexpected entry')

        ct.track_academic_year('guid2', {'academic_year': 2016})
        self.assertEqual(1, len(ct.get_map_entry('guid2')), 'Tracker returned unexpected entry')
        self.assertEqual(1, ct.get_map_entry('guid2')[2016], 'Tracker does not have expected entry')
        self.assertEqual(2, len(ct.get_map_entry('guid1')), 'Tracker returned unexpected entry')
        self.assertEqual(2, ct.get_map_entry('guid1')[2014], 'Tracker does not have expected entry')

    def test_positive_matched_track(self):
        ct = DummyCategoryTracker()

        ct.track_matched_ids('guid1', {})
        self.assertEqual(1, len(ct.get_map_entry('guid1')), 'Tracker returned unexpected entry')
        self.assertEqual(1, ct.get_map_entry('guid1')['matched_ids'], 'Tracker does not have expected entry')

        ct.track_matched_ids('guid1', {})
        self.assertEqual(1, len(ct.get_map_entry('guid1')), 'Tracker returned unexpected entry')
        self.assertEqual(2, ct.get_map_entry('guid1')['matched_ids'], 'Tracker does not have expected entry')

        ct.track_matched_ids('guid2', {})
        self.assertEqual(1, len(ct.get_map_entry('guid2')), 'Tracker returned unexpected entry')
        self.assertEqual(1, ct.get_map_entry('guid2')['matched_ids'], 'Tracker does not have expected entry')
        self.assertEqual(1, len(ct.get_map_entry('guid1')), 'Tracker returned unexpected entry')
        self.assertEqual(2, ct.get_map_entry('guid1')['matched_ids'], 'Tracker does not have expected entry')

    def test_matched_should_not_track(self):
        ct = DummyCategoryTracker(False)

        self.assertIsNone(ct.get_map_entry('guid1'), 'Tracker returned unexpected entry')

        ct.track_matched_ids('guid1', {})

        self.assertIsNone(ct.get_map_entry('guid1'), 'Tracker returned unexpected entry')

    def test_asmt_should_track(self):
        ct = DummyCategoryTracker()

        ct.track_asmt('guid1', {'asmt_type': 'SUMMATIVE', 'asmt_subject': 'Math'})
        self.assertEqual(1, len(ct.get_map_entry('guid1')), 'Tracker returned unexpected entry')
        self.assertEqual(1, ct.get_map_entry('guid1')[('summative', 'math')], 'Tracker does not have expected entry')

        ct.track_asmt('guid1', {'asmt_type': 'SUMMATIVE', 'asmt_subject': 'ELA'})
        self.assertEqual(2, len(ct.get_map_entry('guid1')), 'Tracker returned unexpected entry')
        self.assertEqual(1, ct.get_map_entry('guid1')[('summative', 'ela')], 'Tracker does not have expected entry')

        ct.track_asmt('guid1', {'asmt_type': 'INTERIM COMPREHENSIVE', 'asmt_subject': 'ELA'})
        self.assertEqual(3, len(ct.get_map_entry('guid1')), 'Tracker returned unexpected entry')
        self.assertEqual(1, ct.get_map_entry('guid1')[('interim comprehensive', 'ela')], 'Tracker does not have expected entry')

        ct.track_asmt('guid1', {'asmt_type': 'INTERIM COMPREHENSIVE', 'asmt_subject': 'ELA'})
        self.assertEqual(3, len(ct.get_map_entry('guid1')), 'Tracker returned unexpected entry')
        self.assertEqual(2, ct.get_map_entry('guid1')[('interim comprehensive', 'ela')], 'Tracker does not have expected entry')

        ct.track_asmt('guid2', {'asmt_type': 'INTERIM COMPREHENSIVE', 'asmt_subject': 'ELA'})
        self.assertEqual(3, len(ct.get_map_entry('guid1')), 'Tracker returned unexpected entry')
        self.assertEqual(2, ct.get_map_entry('guid1')[('interim comprehensive', 'ela')], 'Tracker does not have expected entry')
        self.assertEqual(1, len(ct.get_map_entry('guid2')), 'Tracker returned unexpected entry')
        self.assertEqual(1, ct.get_map_entry('guid2')[('interim comprehensive', 'ela')], 'Tracker does not have expected entry')

    def test_asmt_should_not_track(self):
        ct = DummyCategoryTracker(False)

        self.assertIsNone(ct.get_map_entry('guid1'), 'Tracker returned unexpected entry')

        ct.track_asmt('guid1', {'asmt_type': 'SUMMATIVE', 'asmt_subject': 'ELA'})

        self.assertIsNone(ct.get_map_entry('guid1'), 'Tracker returned unexpected entry')


class DummyCategoryTracker(CategoryTracker):

    def __init__(self, should_increment_fl=True):
        super().__init__('Category', 'Value')
        self.should_increment_fl = should_increment_fl

    def _should_increment(self, row):
        return self.should_increment_fl

    def _should_increment_matched_ids(self, row):
        return self.should_increment_fl
