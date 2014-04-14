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
            'NJ': {2014: 444},
            'district1': {2014: 123},
            'district2': {2014: 20},
            'school1': {2014: 37},
            'school2': {},
            'school3': {2014: 8},
            'school4': {2014: 64}
        }
        expected_data = [
            ['New Jersey', 'ALL', 'ALL', 'Total', 'Total', '444'],
            ['New Jersey', 'Central Regional', 'ALL', 'Total', 'Total', '123'],
            ['New Jersey', 'Capital Regional', 'ALL', 'Total', 'Total', '20'],
            ['New Jersey', 'Central Regional', 'Springfield Elementary', 'Total', 'Total', '37'],
            ['New Jersey', 'Central Regional', 'Springfield Junior High', 'Total', 'Total', '0'],
            ['New Jersey', 'Capital Regional', 'Capital Charter School', 'Total', 'Total', '8'],
            ['New Jersey', 'Capital Regional', 'Capital School Of Interpretive Dance', 'Total', 'Total', '64']
        ]

        data = get_tracker_results(report_map, trackers, 2014)

        index = 0
        for row in data:
            self.assertEquals(expected_data[index], row)
            index += 1
        self.assertEquals(7, index)
