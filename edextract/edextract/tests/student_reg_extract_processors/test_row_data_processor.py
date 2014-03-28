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
    @unittest.skip("Skipping till tests are fixed")
    def test_process_row_data(self):
        rows = (
            {'state_name': 'New Jersey', 'state_code': 'NJ', 'district_guid': 'district1', 'district_name': 'Central Regional',
             'school_guid': 'school1', 'school_name': 'Springfield Elementary', 'student_guid': 'student1',
             'student_first_name': 'Bartholomew', 'student_middle_name': 'Jackson', 'student_last_name': 'Simpson',
             'gender': 'male', 'enrl_grade': 5, 'dmg_eth_hsp': 't', 'dmg_eth_ami': 'f', 'dmg_eth_asn': 't', 'dmg_eth_blk': 'f',
             'dmg_eth_pcf': 't', 'dmg_eth_wht': 'f', 'dmg_prg_iep': 't', 'dmg_prg_lep': 'f', 'dmg_prg_504': 't',
             'dmg_sts_ecd': 'f', 'dmg_sts_mig': 't', 'dmg_multi_race': 'f', 'student_reg_guid': 'stu_reg1', 'academic_year': 2014},
            {'state_name': 'New Jersey', 'state_code': 'NJ', 'district_guid': 'district1', 'district_name': 'Central Regional',
             'school_guid': 'school1', 'school_name': 'Springfield Elementary', 'student_guid': 'student1',
             'student_first_name': 'Bartholomew', 'student_middle_name': 'Jackson', 'student_last_name': 'Simpson',
             'gender': 'male', 'enrl_grade': 5, 'dmg_eth_hsp': 't', 'dmg_eth_ami': 'f', 'dmg_eth_asn': 't', 'dmg_eth_blk': 'f',
             'dmg_eth_pcf': 't', 'dmg_eth_wht': 'f', 'dmg_prg_iep': 't', 'dmg_prg_lep': 'f', 'dmg_prg_504': 't',
             'dmg_sts_ecd': 'f', 'dmg_sts_mig': 't', 'dmg_multi_race': 'f', 'student_reg_guid': 'stu_reg1', 'academic_year': 2015},
        )
        trackers = [TotalTracker()]
        data_processors = [StateDataProcessor(trackers), DistrictDataProcessor(trackers), SchoolDataProcessor(trackers)]

        process_row_data(rows, data_processors)

        self.assertEquals({EdOrgNameKey('New Jersey', '', ''): 'NJ'}, data_processors[0].get_ed_org_hierarchy())
        self.assertEquals({EdOrgNameKey('New Jersey', 'Central Regional', ''): 'district1'},
                          data_processors[1].get_ed_org_hierarchy())
        self.assertEquals({EdOrgNameKey('New Jersey', 'Central Regional', 'Springfield Elementary'): 'school1'},
                          data_processors[2].get_ed_org_hierarchy())
        self.assertEquals({2014: 1, 2015: 1}, trackers[0].get_map_entry('NJ'))
        self.assertEquals({2014: 1, 2015: 1}, trackers[0].get_map_entry('district1'))
        self.assertEquals({2014: 1, 2015: 1}, trackers[0].get_map_entry('school1'))

    def test_process_row_data2(self):

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
