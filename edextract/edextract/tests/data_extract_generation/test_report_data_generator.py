__author__ = 'tshewchuk'

"""
This module contains unit tests for the functions in the report_data_generator module.
"""

import unittest
from collections import OrderedDict

from edextract.trackers.total_tracker import TotalTracker
from edextract.student_reg_extract_processors.ed_org_data_processor import EdOrgNameKey
from edextract.data_extract_generation.report_data_generator import get_tracker_results


class TestReportDataGenerator(unittest.TestCase):

    def test_get_tracker_results(self):
        report_map = OrderedDict([
            (EdOrgNameKey('New Jersey', '', ''), 'NJ'),
            (EdOrgNameKey('New Jersey', 'Central Regional', ''), 'district1'),
            (EdOrgNameKey('New Jersey', 'Central Regional', 'Springfield Elementary'), 'school1'),
            (EdOrgNameKey('New Jersey', 'Central Regional', 'Springfield Junior High'), 'school2'),
            (EdOrgNameKey('New Jersey', 'Capital Regional', ''), 'district2'),
            (EdOrgNameKey('New Jersey', 'Capital Regional', 'Capital Charter School'), 'school3'),
            (EdOrgNameKey('New Jersey', 'Capital Regional', 'Capital School Of Interpretive Dance'), 'school3')
        ])
        total_tracker = TotalTracker()
        trackers = [total_tracker]
        total_tracker._map = {
            'NJ': {2014: 444, 2015: 555},
            'district1': {2014: 123, 2015: 90},
            'school1': {2014: 37, 2015: 73},
            'school2': {2015: 8},
            'district2': {2014: 20, 2015: 20},
            'school3': {2014: 8},
            'school4': {2014: 64, 2015: 46}
        }
        expected_data = [
            ['New Jersey', 'ALL', 'ALL', 'Total', 'Total', '444', '100.0', '555', '100.0', '111', '25.0', '0.0'],
            ['New Jersey', 'Central Regional', 'ALL', 'Total', 'Total', '123', '100.0', '90', '100.0', '-33', '-26.83', '0.0'],
            ['New Jersey', 'Central Regional', 'Springfield Elementary', 'Total', 'Total', '37', '100.0', '73', '100.0', '36', '97.30', '0.0'],
            ['New Jersey', 'Central Regional', 'Springfield Junior High', 'Total', 'Total', '', '', '8', '100.0', '', '', ''],
            ['New Jersey', 'Capital Regional', 'ALL', 'Total', 'Total', '20', '100.0', '20', '100.0', '0', '0.0', '0.0'],
            ['New Jersey', 'Capital Regional', 'Capital Charter School', 'Total', 'Total', '8', '100.0', '', '', '', '', ''],
            ['New Jersey', 'Capital Regional', 'Capital School Of Interpretive Dance', 'Total', 'Total', '64', '100.0', '46', '100.0', '-18', '-28.13', '0.0']
        ]

        data = get_tracker_results(report_map, total_tracker, trackers, 2015)

        index = 0
        for row in data:
            print('row[{index}] = {row}'.format(index=index, row=str(row)))
            #self.assertEquals(expected_data[index], row)
            index += 1
