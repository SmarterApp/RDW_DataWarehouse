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

    def test_record(self):
        record = Record(record_id='id1', name='name1')
        self.assertEqual(0, len(record.subjects))
        self.assertEqual('id1', record.id)
        self.assertEqual('name1', record.name)
        subjects = {'hello': 'test'}
        self.subjects = subjects
        self.assertDictEqual(self.subjects, subjects)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
