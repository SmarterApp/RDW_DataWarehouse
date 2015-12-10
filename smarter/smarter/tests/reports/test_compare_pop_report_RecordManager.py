'''
Created on Mar 11, 2013

@author: tosako
'''
import unittest
import os
import json
from smarter.reports.helpers.constants import Constants
import collections
from smarter.reports.compare_pop_report import RecordManager, Record


class Test(unittest.TestCase):

    def test_RecordManager_calculate_percentage(self):
        percentage = RecordManager.calculate_percentage(100, 0)
        self.assertEqual(0, percentage)

        percentage = RecordManager.calculate_percentage(0, 100)
        self.assertEqual(0, percentage)

        percentage = RecordManager.calculate_percentage(1, 300)
        self.assertEqual('0.33', '%.2f' % percentage)

        percentage = RecordManager.calculate_percentage(1, 100)
        self.assertEqual(1, percentage)

    def test_RecordManager_get_record(self):
        param = {Constants.STATECODE: 'DE'}
        manager = RecordManager(None, {}, **param)
        record3 = Record(inst_id=3, name='aaa')
        record1 = Record(inst_id=1, name='bbb')
        record2 = Record(inst_id=2, name='ccc')

        records = collections.OrderedDict()
        records[record3.id] = record3
        records[record1.id] = record1
        records[record2.id] = record2
        manager._tracking_record = records
        records = manager.get_records()
        self.assertEqual(3, len(records))
        for index in range(len(records)):
            if index == 0:
                self.assertEqual(records[0][Constants.ID], 3)
                self.assertEqual(records[0][Constants.NAME], 'aaa')
                self.assertEqual(2, len(records[0][Constants.PARAMS]))
                self.assertEqual(records[0][Constants.PARAMS][Constants.STATECODE], param.get(Constants.STATECODE))
                self.assertEqual(records[0][Constants.PARAMS][Constants.ID], 3)
                self.assertIsNone(records[0][Constants.PARAMS].get(Constants.SCHOOLGUID))
                self.assertIsNone(records[0][Constants.PARAMS].get(Constants.ASMT_GRADE))
            elif index == 1:
                self.assertEqual(records[1][Constants.ID], 1)
                self.assertEqual(records[1][Constants.NAME], 'bbb')
                self.assertEqual(2, len(records[1][Constants.PARAMS]))
                self.assertEqual(records[1][Constants.PARAMS][Constants.STATECODE], param.get(Constants.STATECODE))
                self.assertEqual(records[1][Constants.PARAMS][Constants.ID], 1)
            elif index == 2:
                self.assertEqual(records[2][Constants.ID], 2)
                self.assertEqual(records[2][Constants.NAME], 'ccc')
                self.assertEqual(2, len(records[1][Constants.PARAMS]))
                self.assertEqual(records[2][Constants.PARAMS][Constants.STATECODE], param.get(Constants.STATECODE))
                self.assertEqual(records[2][Constants.PARAMS][Constants.ID], 2)

    def test_RecordManager_summary(self):
        param = {Constants.STATECODE: 'DE'}
        subjects = {Constants.MATH: Constants.SUBJECT1, Constants.ELA: Constants.SUBJECT2}
        asmt_levels = {Constants.MATH: 5, Constants.ELA: 5}
        manager = RecordManager(subjects, asmt_levels, **param)
        manager._summary = {Constants.SUBJECT1: {1: 10, 2: 20, 3: 30, 4: 40, 5: 50}, Constants.SUBJECT2: {5: 50}}
        summary_records = manager.get_summary()

        self.assertEqual(1, len(summary_records))
        results = summary_records[0][Constants.RESULTS]
        self.assertEqual(2, len(results))
        subject1 = results.get(Constants.SUBJECT1)
        self.assertIsNotNone(subject1)
        self.assertEqual(150, subject1[Constants.TOTAL])

        subject2 = results.get(Constants.SUBJECT2)
        self.assertIsNotNone(subject2)
        self.assertEqual(50, subject2[Constants.TOTAL])

    def test_RecordManager_get_subjects(self):
        param = {Constants.STATECODE: 'DE'}
        subjects = {'a': 'b', 'c': 'd'}
        manager = RecordManager(subjects, {}, **param)
        subjects = manager.get_subjects()
        self.assertEqual('a', subjects['b'])

    def test_RecordManager_update_record(self):
        results = get_results('school_view_results.json')
        param = {Constants.STATECODE: 'DE', Constants.DISTRICTGUID: '245', Constants.SCHOOLGUID: '92499'}
        subjects = {Constants.MATH: Constants.SUBJECT1, Constants.ELA: Constants.SUBJECT2}
        asmt_levels = {Constants.SUBJECT1: 3, Constants.SUBJECT2: 5}
        manager = RecordManager(subjects, asmt_levels, **param)
        for result in results:
            manager.update_record(result)
        self.assertEqual(1, len(manager._tracking_record))
        summary = manager.get_summary()
        self.assertEqual(3, len(summary[0]['results']['subject1']))

    def test_RecordManager_format_data_insufficent_case(self):
        data = {'subject2': {1: 1, 2: 2, 3: 1}, 'subject1': {2: 2}}
        subjects = {Constants.MATH: Constants.SUBJECT1, Constants.ELA: Constants.SUBJECT2}
        asmt_levels = {Constants.SUBJECT1: 4, Constants.SUBJECT2: 2}
        manager = RecordManager(subjects, asmt_levels)
        formatted_data = manager.format_results(data)
        self.assertEqual(len(formatted_data['subject1']['intervals']), 4)
        self.assertEqual(formatted_data['subject1']['intervals'][0]['percentage'], -1)
        self.assertEqual(formatted_data['subject1']['intervals'][0]['level'], 1)
        self.assertEqual(formatted_data['subject1']['intervals'][1]['percentage'], -1)
        self.assertEqual(formatted_data['subject1']['intervals'][1]['level'], 2)
        self.assertEqual(formatted_data['subject1']['intervals'][3]['percentage'], -1)
        self.assertEqual(formatted_data['subject1']['intervals'][3]['level'], 4)

    def test_RecordManager_format_data(self):
        data = {'subject2': {1: 1, 2: 2, 3: 1}, 'subject1': {1: 1, 2: 2, 3: 3, 4: 4}}
        subjects = {Constants.MATH: Constants.SUBJECT1, Constants.ELA: Constants.SUBJECT2}
        asmt_levels = {Constants.SUBJECT1: 4, Constants.SUBJECT2: 2}
        manager = RecordManager(subjects, asmt_levels)
        formatted_data = manager.format_results(data)
        self.assertEqual(len(formatted_data['subject1']['intervals']), 4)
        self.assertEqual(formatted_data['subject1']['intervals'][0]['count'], 1)
        self.assertEqual(formatted_data['subject1']['intervals'][0]['level'], 1)
        self.assertEqual(formatted_data['subject1']['intervals'][0]['percentage'], 10)
        self.assertEqual(formatted_data['subject1']['intervals'][1]['count'], 2)
        self.assertEqual(formatted_data['subject1']['intervals'][1]['level'], 2)
        self.assertEqual(formatted_data['subject1']['intervals'][1]['percentage'], 20)
        self.assertEqual(formatted_data['subject1']['intervals'][3]['count'], 4)
        self.assertEqual(formatted_data['subject1']['intervals'][3]['level'], 4)
        self.assertEqual(formatted_data['subject1']['intervals'][3]['percentage'], 40)


def get_results(file_name):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'resources', file_name))) as json_data:
        data = json.load(json_data)
    return data


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
