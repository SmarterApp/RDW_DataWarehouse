'''
Created on Feb 9, 2013

@author: tosako
'''
import unittest
from database.tests.unittest_with_sqlite import Unittest_with_sqlite
from smarter.reports.helpers.list_of_districts import get_districts


class Test(Unittest_with_sqlite):

    def testReport(self):
        params = {}
        params['state_code'] = 'NY'
        results = get_districts(params)
        self.assertEqual(2, len(results), "Number of districts for NY")
        self.assertEqual("Daybreak", results[0]['district_name'], "district_name")


if __name__ == "__main__":
    unittest.main()
