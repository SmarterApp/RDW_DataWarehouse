'''
Created on Feb 11, 2013

@author: tosako
'''
import unittest
from database.tests.unittest_with_sqlite import Unittest_with_sqlite
from smarter.reports.helpers.list_of_subjects import get_subjects


class Test(Unittest_with_sqlite):

    def testName(self):
        params = {}
        results = get_subjects(params)
        self.assertEqual(2, len(results), 'Number of available subjects')
        self.assertEqual("ELA", results[0], 'First Subject')
        self.assertEqual("MATH", results[1], 'Second Subject')


if __name__ == "__main__":
    unittest.main()
