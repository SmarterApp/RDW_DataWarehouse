__author__ = 'npandey'
"""
Test Student Registration School Data Processor
"""

from edextract.student_reg_extract_processors.school_data_processor import SchoolDataProcessor
import unittest
from edextract.student_reg_extract_processors.attribute_constants import AttributeConstants
from unittest.mock import MagicMock


class TestSchoolDataProcessor(unittest.TestCase):

    def setUp(self):
        self.data = {AttributeConstants.STATE_NAME: 'North Carolina', AttributeConstants.DISTRICT_NAME: 'Gilfford County',
                     AttributeConstants.SCHOOL_NAME: 'Daybreak Junior High', AttributeConstants.SCHOOL_GUID: '5f706ksg80hhxs'}
        self.category_trackers = []
        self.ed_rg_heirarchy_map = {}

        self.state_data_processor = SchoolDataProcessor(self.category_trackers, self.ed_rg_heirarchy_map)

    def test_ed_org_map_updates(self):
        self.state_data_processor.process_data(self.data)
        self.assertEquals(len(self.ed_rg_heirarchy_map), 1)
        self.assertDictEqual(self.ed_rg_heirarchy_map, {('North Carolina', 'Gilfford County',
                                                         'Daybreak Junior High'): '5f706ksg80hhxs'})

    def test_call_to_tracker(self):
        self.state_data_processor._call_trackers = MagicMock(return_value=None)

        self.state_data_processor.process_data(self.data)

        self.state_data_processor._call_trackers.assert_called_with('5f706ksg80hhxs', self.data)
