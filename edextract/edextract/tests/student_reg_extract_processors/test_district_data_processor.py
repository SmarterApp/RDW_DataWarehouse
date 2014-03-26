from edextract.student_reg_extract_processors.district_data_processor import DistrictDataProcessor

__author__ = 'ablum'

"""
Test Student Registration District Data Processor
"""

import unittest
from edextract.student_reg_extract_processors.attribute_constants import AttributeConstants
from unittest.mock import MagicMock


class TestDistrictDataProcessor(unittest.TestCase):

    def setUp(self):
        self.results = {AttributeConstants.STATE_NAME: 'North Carolina', AttributeConstants.STATE_CODE: 'NC',
                        AttributeConstants.DISTRICT_GUID: 'GUILFORD_GUID', AttributeConstants.DISTRICT_NAME: 'Guilford County'}
        self.category_trackers = []
        self.ed_rg_hierarchy_map = {}

        self.district_data_processor = DistrictDataProcessor(self.category_trackers, self.ed_rg_hierarchy_map)

    def test_ed_org_map_updates(self):
        self.district_data_processor.process_data(self.results)
        self.assertEquals(len(self.ed_rg_hierarchy_map), 1)
        self.assertDictEqual(self.ed_rg_hierarchy_map, {('North Carolina', 'Guilford County', ''): 'GUILFORD_GUID'})

    def test_call_to_tracker(self):
        self.district_data_processor._call_trackers = MagicMock(return_value=None)

        self.district_data_processor.process_data(self.results)

        self.district_data_processor._call_trackers.assert_called_with('GUILFORD_GUID', self.results)
