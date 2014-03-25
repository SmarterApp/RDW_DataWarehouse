__author__ = 'npandey'
"""
Test Student Registration State Data Processor
"""

from edextract.student_reg_extract_processors.state_data_processor import StateDataProcessor
import unittest
from edextract.student_reg_extract_processors.attribute_constants import AttributeConstants
from unittest.mock import MagicMock


class TestSRStateVisitor(unittest.TestCase):

    def setUp(self):
        self.results = {AttributeConstants.STATE_NAME: 'North Carolina', AttributeConstants.STATE_CODE: 'NC'}
        self.category_trackers = []
        self.ed_rg_heirarchy_map = {}

        self.state_data_processor = StateDataProcessor(self.category_trackers, self.ed_rg_heirarchy_map)

    def test_ed_org_map_updates(self):
        self.state_data_processor.process_data(self.results)
        self.assertEquals(len(self.ed_rg_heirarchy_map), 1)
        self.assertDictEqual(self.ed_rg_heirarchy_map, {('North Carolina', '', ''): 'NC'})

    def test_call_to_tracker(self):
        self.state_data_processor._call_trackers = MagicMock(return_value=None)

        self.state_data_processor.process_data(self.results)

        self.state_data_processor._call_trackers.assert_called_with('NC', self.results)
