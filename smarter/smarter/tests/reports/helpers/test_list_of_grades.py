'''
Created on Feb 11, 2013

@author: tosako
'''
import unittest
from smarter.reports.helpers.list_of_grades import get_grades
from database.tests.unittest_with_sqlite import Unittest_with_sqlite


class Test(Unittest_with_sqlite):

    def testReport(self):
        params = {}
        results = get_grades(params)
        self.assertEqual(2, len(results), "Number of available grades")
        self.assertEqual('1', results[0]['grade_code'], 'first grade_code')
        self.assertEqual('Grade 2', results[1]['grade_desc'], 'second grade_desc')


if __name__ == "__main__":
    unittest.main()
