'''
Created on Mar 11, 2013

@author: tosako
'''
import unittest
import os
import json
from smarter.reports.compare_pop_report import RecordManager, Constants, \
    Record, ParameterManager, Parameters


class Test(unittest.TestCase):

    def test_RecordManager_calculate_percentage(self):
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

    def test_RecordManager_get_record(self):
        manager = RecordManager(None, None)
        record1 = Record(record_id=1, name='bbb')
        record2 = Record(record_id=2, name='ccc')
        record3 = Record(record_id=3, name='aaa')

        records = {}
        records[record1.id] = record1
        records[record2.id] = record2
        records[record3.id] = record3
        manager._tracking_record = records
        records = manager.get_records()
        self.assertEqual(3, len(records))
        self.assertEqual(records[0][Constants.ID], 3)
        self.assertEqual(records[0][Constants.NAME], 'aaa')
        self.assertEqual(records[1][Constants.ID], 1)
        self.assertEqual(records[1][Constants.NAME], 'bbb')
        self.assertEqual(records[2][Constants.ID], 2)
        self.assertEqual(records[2][Constants.NAME], 'ccc')

    def test_RecordManager_summary(self):
        parameterManager = ParameterManager(Parameters({Constants.STATEID: 'DE'}))
        subjects = {Constants.MATH: Constants.SUBJECT1, Constants.ELA: Constants.SUBJECT2}
        manager = RecordManager(parameterManager, subjects)
        record1 = Record(record_id=1, name='bbb')
        record1.subjects[Constants.SUBJECT1] = {Constants.ASMT_SUBJECT: Constants.MATH, Constants.TOTAL: 150, Constants.INTERVALS: [{Constants.LEVEL: 1, Constants.COUNT: 10}, {Constants.LEVEL: 2, Constants.COUNT: 20}, {Constants.LEVEL: 3, Constants.COUNT: 30}, {Constants.LEVEL: 4, Constants.COUNT: 40}, {Constants.LEVEL: 5, Constants.COUNT: 50}]}
        record1.subjects[Constants.SUBJECT2] = {Constants.ASMT_SUBJECT: Constants.ELA, Constants.TOTAL: 150, Constants.INTERVALS: [{Constants.LEVEL: 1, Constants.COUNT: 10}, {Constants.LEVEL: 2, Constants.COUNT: 20}, {Constants.LEVEL: 3, Constants.COUNT: 30}, {Constants.LEVEL: 4, Constants.COUNT: 40}, {Constants.LEVEL: 5, Constants.COUNT: 50}]}
        record2 = Record(record_id=2, name='ccc')
        record2.subjects[Constants.SUBJECT1] = {Constants.ASMT_SUBJECT: Constants.MATH, Constants.TOTAL: 700, Constants.INTERVALS: [{Constants.LEVEL: 1, Constants.COUNT: 100}, {Constants.LEVEL: 2, Constants.COUNT: 120}, {Constants.LEVEL: 3, Constants.COUNT: 140}, {Constants.LEVEL: 4, Constants.COUNT: 160}, {Constants.LEVEL: 5, Constants.COUNT: 180}]}
        record2.subjects[Constants.SUBJECT2] = {Constants.ASMT_SUBJECT: Constants.ELA, Constants.TOTAL: 1200, Constants.INTERVALS: [{Constants.LEVEL: 1, Constants.COUNT: 200}, {Constants.LEVEL: 2, Constants.COUNT: 220}, {Constants.LEVEL: 3, Constants.COUNT: 240}, {Constants.LEVEL: 4, Constants.COUNT: 260}, {Constants.LEVEL: 5, Constants.COUNT: 280}]}
        record3 = Record(record_id=3, name='aaa')
        record3.subjects[Constants.SUBJECT1] = {Constants.ASMT_SUBJECT: Constants.MATH, Constants.TOTAL: 150, Constants.INTERVALS: [{Constants.LEVEL: 1, Constants.COUNT: 10}, {Constants.LEVEL: 2, Constants.COUNT: 20}, {Constants.LEVEL: 3, Constants.COUNT: 30}, {Constants.LEVEL: 4, Constants.COUNT: 40}, {Constants.LEVEL: 5, Constants.COUNT: 50}]}
        record3.subjects[Constants.SUBJECT2] = {Constants.ASMT_SUBJECT: Constants.ELA, Constants.TOTAL: 150, Constants.INTERVALS: [{Constants.LEVEL: 1, Constants.COUNT: 10}, {Constants.LEVEL: 2, Constants.COUNT: 20}, {Constants.LEVEL: 3, Constants.COUNT: 30}, {Constants.LEVEL: 4, Constants.COUNT: 40}, {Constants.LEVEL: 5, Constants.COUNT: 50}]}
        records = {}
        records[record1.id] = record1
        records[record2.id] = record2
        records[record3.id] = record3
        manager._tracking_record = records

        summary_records = manager.get_summary()

        self.assertEqual(2, len(summary_records))
        subject1 = summary_records.get(Constants.SUBJECT1)
        self.assertIsNotNone(subject1)
        self.assertEqual(1000, subject1[Constants.TOTAL])

        subject2 = summary_records.get(Constants.SUBJECT2)
        self.assertIsNotNone(subject2)
        self.assertEqual(1500, subject2[Constants.TOTAL])

    def test_RecordManager_get_subjects(self):
        parameterManager = ParameterManager(Parameters({Constants.STATEID: 'DE'}))
        subjects = {'a': 'b', 'c': 'd'}
        manager = RecordManager(parameterManager, subjects)
        subjects = manager.get_subjects()
        self.assertEqual('a', subjects['b'])

    def test_RecordManager_update_record(self):
        results = get_results('state_view_results.json')
        parameterManager = ParameterManager(Parameters({Constants.STATEID: 'DE'}))
        subjects = {Constants.MATH: Constants.SUBJECT1, Constants.ELA: Constants.SUBJECT2}
        manager = RecordManager(parameterManager, subjects)
        for result in results:
            manager.update_record(result)
        self.assertEqual(2, len(manager.get_asmt_custom_metadata()))
        self.assertEqual(34, len(manager._tracking_record))


def get_results(file_name):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources', file_name))) as json_data:
        data = json.load(json_data)
    return data


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
