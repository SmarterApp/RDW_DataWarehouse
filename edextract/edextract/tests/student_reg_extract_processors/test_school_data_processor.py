__author__ = 'npandey'
"""
Test Student Registration School Data Processor
"""

from edextract.student_reg_extract_processors.school_data_processor import SchoolDataProcessor
import unittest
from edextract.student_reg_extract_processors.attribute_constants import AttributeFieldConstants
from unittest.mock import MagicMock


class TestSchoolDataProcessor(unittest.TestCase):

    def setUp(self):
        self.data = {AttributeFieldConstants.STATE_NAME: 'North Carolina', AttributeFieldConstants.DISTRICT_NAME: 'Gilfford County',
                     AttributeFieldConstants.SCHOOL_NAME: 'Daybreak Junior High', AttributeFieldConstants.SCHOOL_ID: '5f706ksg80hhxs'}
        self.matched_ids_results = {'prev_school_id': '5f706ksg80hhxs', AttributeFieldConstants.STATE_NAME: 'North Carolina',
                                    AttributeFieldConstants.DISTRICT_NAME: 'Gilfford County',
                                    AttributeFieldConstants.SCHOOL_NAME: 'Daybreak Junior High', AttributeFieldConstants.SCHOOL_ID: '5f706ksg80hhxs'}
        self.category_trackers = []

        self.school_data_processor = SchoolDataProcessor(self.category_trackers)

    def test_ed_org_map_updates(self):
        self.school_data_processor.process_yearly_data(self.data)
        self.assertEquals(len(self.school_data_processor.get_ed_org_hierarchy()), 1)
        self.assertDictEqual(self.school_data_processor.get_ed_org_hierarchy(), {('North Carolina', 'Gilfford County',
                                                                                  'Daybreak Junior High'): '5f706ksg80hhxs'})

    def test_call_to_tracker(self):
        self.school_data_processor._call_academic_year_trackers = MagicMock(return_value=None)

        self.school_data_processor.process_yearly_data(self.data)

        self.school_data_processor._call_academic_year_trackers.assert_called_with('5f706ksg80hhxs', self.data)

    def test_call_to_matched_ids_tracker(self):
        self.school_data_processor._call_matched_ids_trackers = MagicMock(return_value=None)

        self.school_data_processor.process_matched_ids_data(self.matched_ids_results)

        self.school_data_processor._call_matched_ids_trackers.assert_called_with('5f706ksg80hhxs', self.matched_ids_results)

    def test__should_call_trackers(self):
        same_school = {AttributeFieldConstants.SCHOOL_ID: '5f706ksg80hhxs', 'prev_school_id': '5f706ksg80hhxs'}
        result = self.school_data_processor._is_matched_school(same_school)
        self.assertTrue(result)

    def test__should_not_call_trackers(self):
        different_school = {AttributeFieldConstants.SCHOOL_ID: '5f706ksg80hhxs', 'prev_school_id': '6g817lsg80hhxs'}
        result = self.school_data_processor._is_matched_school(different_school)
        self.assertFalse(result)

    def test_process_asmt_outcome_data(self):
        self.school_data_processor._call_asmt_trackers = MagicMock(return_value=None)

        self.school_data_processor.process_asmt_outcome_data(self.data)

        self.school_data_processor._call_asmt_trackers.assert_called_with('5f706ksg80hhxs', self.data)
