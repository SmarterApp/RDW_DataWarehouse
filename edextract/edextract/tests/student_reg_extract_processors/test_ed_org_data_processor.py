__author__ = 'npandey'


import unittest
from unittest.mock import MagicMock
from edextract.student_reg_extract_processors.ed_org_data_processor import EdOrgDataProcessor
from edextract.student_reg_extract_processors.attribute_constants import AttributeConstants
from edextract.trackers.total_tracker import TotalTracker


class TestEdOrgDataProcessor(unittest.TestCase):

    def setUp(self):
        self.tracker = TotalTracker()
        self.tracker.track = MagicMock(return_value=None)

        self.category_tracker = [self.tracker]
        self.ed_rg_heirarchy_map = {}

        EdOrgDataProcessor.__abstractmethods__ = set()  # Make this class instantiable for these tests only.
        self.data_processor = EdOrgDataProcessor(self.category_tracker, self.ed_rg_heirarchy_map)

        self.data = {AttributeConstants.STATE_NAME: 'North Carolina', AttributeConstants.STATE_CODE: 'NC'}

    def test_add_to_ed_org_heirarchy(self):
        self.data_processor._add_to_edorg_hierarchy('123', 'NC')
        self.data_processor._add_to_edorg_hierarchy('456', 'NC', 'Gilfford')
        self.data_processor._add_to_edorg_hierarchy('789', 'NC', 'Gilfford', 'Daybreak School')

    def test_call_tracker(self):
        self.data_processor._call_trackers('123', self.data)

        self.tracker.track.assert_called_with('123', self.data)
