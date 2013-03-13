'''
Created on Mar 9, 2013

@author: tosako
'''
import unittest
from smarter.reports.compare_pop_report import Record


class Test(unittest.TestCase):

    def test_empty_record(self):
        record = Record()
        self.assertEqual(0, len(record.subjects))
        self.assertIsNone(record.id)
        self.assertIsNone(record.name)
        self.assertIsNone(record.state_id)
        self.assertIsNone(record.district_id)
        self.assertIsNone(record.school_id)

    def test_record(self):
        record = Record(record_id='id1', name='name1', state_id='state1', district_id='district1', school_id='school1')
        self.assertEqual(0, len(record.subjects))
        self.assertEqual('id1', record.id)
        self.assertEqual('name1', record.name)
        self.assertEqual('state1', record.state_id)
        self.assertEqual('district1', record.district_id)
        self.assertEqual('school1', record.school_id)
        subjects = {'hello': 'test'}
        self.subjects = subjects
        self.assertDictEqual(self.subjects, subjects)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
