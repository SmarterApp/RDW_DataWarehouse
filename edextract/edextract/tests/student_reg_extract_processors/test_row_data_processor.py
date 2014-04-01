__author__ = 'tshewchuk'

"""
This module contains unit tests for the functions in the row_data_processor module.
"""

import unittest

from edextract.trackers.total_tracker import TotalTracker
from edextract.student_reg_extract_processors.ed_org_data_processor import EdOrgNameKey
from edextract.student_reg_extract_processors.row_data_processor import process_row_data
from edextract.student_reg_extract_processors.state_data_processor import StateDataProcessor
from edextract.student_reg_extract_processors.district_data_processor import DistrictDataProcessor
from edextract.student_reg_extract_processors.school_data_processor import SchoolDataProcessor


class TestRowDataProcessor(unittest.TestCase):

    def test_process_row_data(self):

        class _DataProcessor:

            def __init__(self, dp_id, expected_call_stack):
                self.expected_call_stack = expected_call_stack
                self.dp_id = dp_id

            def process_data(self, data):
                expected_id, expected_data = self.expected_call_stack.pop()
                if expected_id != self.dp_id or expected_data != data:
                    raise IndexError()

        expected_calls_stack = [(2, 2), (1, 2), (2, 1), (1, 1)]  # reversed order, tuples of id and expected value
        dp1 = _DataProcessor(1, expected_calls_stack)
        dp2 = _DataProcessor(2, expected_calls_stack)

        process_row_data([1, 2], [dp1, dp2])
