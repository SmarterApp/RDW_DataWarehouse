__author__ = 'tshewchuk'

"""
Module containing completion_generator unit tests.
"""

import unittest

from collections import OrderedDict

from edextract.data_extract_generation.completion_generator import get_tracker_results
from edextract.trackers.total_tracker import TotalTracker
from edextract.student_reg_extract_processors.ed_org_data_processor import EdOrgNameKey


class TestStatisticsGenerator(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_tracker_results(self):
        report_map = OrderedDict([
            (EdOrgNameKey('New Jersey', '', ''), 'NJ'),
            (EdOrgNameKey('New Jersey', 'Central Regional', ''), 'district1'),
            (EdOrgNameKey('New Jersey', 'Capital Regional', ''), 'district2'),
            (EdOrgNameKey('New Jersey', 'Central Regional', 'Springfield Elementary'), 'school1'),
            (EdOrgNameKey('New Jersey', 'Central Regional', 'Springfield Junior High'), 'school2'),
            (EdOrgNameKey('New Jersey', 'Capital Regional', 'Capital Charter School'), 'school3'),
            (EdOrgNameKey('New Jersey', 'Capital Regional', 'Capital School Of Interpretive Dance'), 'school4')
        ])
        total_tracker = TotalTracker()
        trackers = [total_tracker]
        total_tracker._data_counter.map = {
            'NJ': {2014: 444, 'summative': {'math': 115, 'ela': 105}, 'interim_comprehensive': {'math': 114, 'ela': 108}},
            'district1': {2014: 123, 'summative': {'math': 44, 'ela': 47}, 'interim_comprehensive': {'math': 39, 'ela': 42}},
            'district2': {2014: 20, 'summative': {'math': 5, 'ela': 4}, 'interim_comprehensive': {'math': 3, 'ela': 7}},
            'school1': {},
            'school2': {2014: 37, 'summative': {'math': 9, 'ela': 10}},
            'school3': {2014: 8, 'summative': {'math': 4, 'ela': 2}, 'interim_comprehensive': {'ela': 1}},
            'school4': {2014: 64, 'summative': {'ela': 55}, 'interim_comprehensive': {'math': 58}}
        }
        expected_data = [
            ['New Jersey', 'ALL', 'ALL', 'Total', 'Total', '444', '115', '25.9', '105', '23.65', '114', '25.68', '108', '24.32'],
            ['New Jersey', 'Central Regional', 'ALL', 'Total', 'Total', '123', '44', '35.77', '47', '38.21', '39', '31.71', '42', '34.15'],
            ['New Jersey', 'Capital Regional', 'ALL', 'Total', 'Total', '20', '5', '25', '4', '20', '3', '15', '7', '35'],
            ['New Jersey', 'Central Regional', 'Springfield Elementary', 'Total', 'Total', '0', '0', '', '0', '', '0', '', '0', ''],
            ['New Jersey', 'Central Regional', 'Springfield Junior High', 'Total', 'Total', '37', '9', '24.32', '10', '27.03', '0', '0', '0', '0'],
            ['New Jersey', 'Capital Regional', 'Capital Charter School', 'Total', 'Total', '8', '4', '50', '2', '25', '0', '0', '1', '12.5'],
            ['New Jersey', 'Capital Regional', 'Capital School Of Interpretive Dance', 'Total', 'Total', '64', '0', '0', '55', '85.94', '58', '90.62', '0', '0']
        ]

        data = get_tracker_results(report_map, trackers, 2014)

        index = 0
        for row in data:
            self.assertEquals(expected_data[index], row)
            index += 1
        self.assertEquals(7, index)
