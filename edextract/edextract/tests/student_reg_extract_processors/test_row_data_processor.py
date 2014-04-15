__author__ = 'tshewchuk'

"""
This module contains unit tests for the functions in the row_data_processor module.
"""

import unittest
from unittest.mock import MagicMock, call

from edextract.student_reg_extract_processors.row_data_processor import RowDataProcessor


class TestRowDataProcessor(unittest.TestCase):

    def setUp(self):
        self.mock_processor1 = MagicMock()
        self.mock_processor1.process_yearly_data = MagicMock(return_value=None)
        self.mock_processor1.process_matched_ids_data = MagicMock(return_value=None)
        self.mock_processor1.process_asmt_outcome_row_data = MagicMock(return_value=None)

        self.mock_processor2 = MagicMock()
        self.mock_processor2.process_yearly_data = MagicMock(return_value=None)
        self.mock_processor2.process_matched_ids_data = MagicMock(return_value=None)
        self.mock_processor2.process_asmt_outcome_row_data = MagicMock(return_value=None)

        self.data = [{'first': 'first'}, {'second': 'second'}]

    def test_process_row_data(self):

        class _DataProcessor:

            def __init__(self, dp_id, expected_call_stack):
                self.expected_call_stack = expected_call_stack
                self.dp_id = dp_id

            def process_yearly_data(self, data):
                expected_id, expected_data = self.expected_call_stack.pop()
                if expected_id != self.dp_id or expected_data != data:
                    raise IndexError()

        expected_calls_stack = [(2, 2), (1, 2), (2, 1), (1, 1)]  # reversed order, tuples of id and expected value
        dp1 = _DataProcessor(1, expected_calls_stack)
        dp2 = _DataProcessor(2, expected_calls_stack)

        row_data_processor = RowDataProcessor()
        row_data_processor.data_processors = [dp1, dp2]
        row_data_processor.process_yearly_row_data([1, 2])

    def test_process_matched_row_data(self):
        row_data_processor = RowDataProcessor()
        row_data_processor.data_processors = [self.mock_processor1, self.mock_processor2]

        row_data_processor.process_matched_ids_row_data(self.data)

        self.assertEquals([call({'first': 'first'}), call({'second': 'second'})], self.mock_processor1.process_matched_ids_data.call_args_list)
        self.assertEquals([call({'first': 'first'}), call({'second': 'second'})], self.mock_processor2.process_matched_ids_data.call_args_list)

    def test_process_asmt_outcome_row_data(self):
        row_data_processor = RowDataProcessor()
        row_data_processor.data_processors = [self.mock_processor1, self.mock_processor2]

        row_data_processor.process_asmt_outcome_row_data(self.data)

        self.assertEquals([call({'first': 'first'}), call({'second': 'second'})], self.mock_processor1.process_asmt_outcome_data.call_args_list)
        self.assertEquals([call({'first': 'first'}), call({'second': 'second'})], self.mock_processor2.process_asmt_outcome_data.call_args_list)
