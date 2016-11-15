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
from unittest.mock import MagicMock
from edextract.student_reg_extract_processors.ed_org_data_processor import EdOrgDataProcessor
from edextract.student_reg_extract_processors.attribute_constants import AttributeFieldConstants
from edextract.trackers.total_tracker import TotalTracker


class TestEdOrgDataProcessor(unittest.TestCase):

    def setUp(self):
        self.tracker = TotalTracker()
        self.tracker.track_academic_year = MagicMock(return_value=None)
        self.tracker.track_matched_ids = MagicMock(return_value=None)
        self.tracker.track_asmt = MagicMock(return_value=None)

        self.category_tracker = [self.tracker]

        EdOrgDataProcessor.__abstractmethods__ = set()  # Make this class instantiable for these tests only.
        self.data_processor = EdOrgDataProcessor(self.category_tracker, {})

        self.data = {AttributeFieldConstants.STATE_NAME: 'North Carolina', AttributeFieldConstants.STATE_CODE: 'NC'}

    def test_call_tracker(self):
        self.data_processor._call_academic_year_trackers('123', self.data)
        self.tracker.track_academic_year.assert_called_with('123', self.data)

        self.data_processor._call_academic_year_trackers('456', self.data)
        self.tracker.track_academic_year.assert_called_with('456', self.data)

        self.data_processor._call_academic_year_trackers('789', self.data)
        self.tracker.track_academic_year.assert_called_with('789', self.data)

    def test_call_matched_trackers(self):
        self.data_processor._call_matched_ids_trackers('123', self.data)
        self.tracker.track_matched_ids.assert_called_with('123', self.data)

        self.data_processor._call_matched_ids_trackers('456', self.data)
        self.tracker.track_matched_ids.assert_called_with('456', self.data)

        self.data_processor._call_matched_ids_trackers('789', self.data)
        self.tracker.track_matched_ids.assert_called_with('789', self.data)

    def test_add_to_and_get_ed_org_hierarchy(self):
        self.data_processor._add_to_edorg_hierarchy('123', 'NC')
        self.data_processor._add_to_edorg_hierarchy('456', 'NC', 'Gilfford')
        self.data_processor._add_to_edorg_hierarchy('789', 'NC', 'Gilfford', 'Daybreak School')

        self.assertEqual(3, len(self.data_processor.get_ed_org_hierarchy()))
        self.assertEqual('123', self.data_processor.get_ed_org_hierarchy()[('NC', '', '')])
        self.assertEqual('456', self.data_processor.get_ed_org_hierarchy()[('NC', 'Gilfford', '')])
        self.assertEqual('789', self.data_processor.get_ed_org_hierarchy()[('NC', 'Gilfford', 'Daybreak School')])

    def test_call_asmt_trackers(self):
        self.data_processor._call_asmt_trackers('123', self.data)
        self.tracker.track_asmt.assert_called_with('123', self.data)

        self.data_processor._call_asmt_trackers('456', self.data)
        self.tracker.track_asmt.assert_called_with('456', self.data)

        self.data_processor._call_asmt_trackers('789', self.data)
        self.tracker.track_asmt.assert_called_with('789', self.data)
