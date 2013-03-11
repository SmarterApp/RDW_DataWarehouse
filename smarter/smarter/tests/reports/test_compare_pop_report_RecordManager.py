'''
Created on Mar 11, 2013

@author: tosako
'''
import unittest
import os
import json
from smarter.reports.compare_pop_report import RecordManager, Constants,\
    ParameterManager, Parameters


class Test(unittest.TestCase):

    def test_calculate_percentage(self):
        percentage = RecordManager.calculate_percentage(100, 0)
        self.assertEqual(0, percentage)

        percentage = RecordManager.calculate_percentage(0, 100)
        self.assertEqual(0, percentage)

        percentage = RecordManager.calculate_percentage(1, 300)
        self.assertEqual(0, percentage)

        percentage = RecordManager.calculate_percentage(1, 100)
        self.assertEqual(1, percentage)

    def test_RecordManager_create_interval(self):
        results = get_results('state_view_results.json')
        manager = RecordManager(None, None)
        interval_level1 = manager.create_interval(results[0], Constants.LEVEL1)
        self.assertEqual(1, interval_level1[Constants.COUNT])
        self.assertEqual(1, interval_level1[Constants.LEVEL])
        self.assertEqual(0, interval_level1[Constants.PERCENTAGE])
        interval_level2 = manager.create_interval(results[0], Constants.LEVEL2)
        self.assertEqual(2883, interval_level2[Constants.COUNT])
        self.assertEqual(2, interval_level2[Constants.LEVEL])
        self.assertEqual(80, interval_level2[Constants.PERCENTAGE])
        interval_level3 = manager.create_interval(results[0], Constants.LEVEL3)
        self.assertEqual(693, interval_level3[Constants.COUNT])
        self.assertEqual(3, interval_level3[Constants.LEVEL])
        self.assertEqual(19, interval_level3[Constants.PERCENTAGE])
        interval_level4 = manager.create_interval(results[0], Constants.LEVEL4)
        self.assertEqual(13, interval_level4[Constants.COUNT])
        self.assertEqual(4, interval_level4[Constants.LEVEL])
        self.assertEqual(0, interval_level4[Constants.PERCENTAGE])
        interval_level5 = manager.create_interval(results[0], Constants.LEVEL5)
        self.assertEqual(0, interval_level5[Constants.COUNT])
        self.assertEqual(5, interval_level5[Constants.LEVEL])
        self.assertEqual(0, interval_level5[Constants.PERCENTAGE])

    def test_get_record(self):
        #results = get_results('state_view_results.json')
        #subjects = {Constants.MATH: Constants.SUBJECT1, Constants.ELA: Constants.SUBJECT2}
        #parameterManager = ParameterManager(Parameters({Constants.STATEID: 'DE'}))
        manager = RecordManagerUT(None, None)
        #__record = {}
        #    __record[Constants.ID] = record.id
        #    __record[Constants.NAME] = record.name
        #    __record[Constants.RESULTS] = record.subjects
        #    records.append(__record)


def get_results(file_name):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources', file_name))) as json_data:
        data = json.load(json_data)
    return data


class RecordManagerUT(RecordManager):

    def set_tracking_record(self, value):
        '''
        the purpose of this setter is for Unit Test
        '''
        super()._tracking_record = value

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
