'''
Created on Feb 11, 2013

@author: tosako
'''
import unittest
from database.tests.unittest_with_sqlite import Unittest_with_sqlite
from smarter.reports.helpers.list_of_schools import get_schools


class Test(Unittest_with_sqlite):

    def testReport(self):
        params = {}
        params['district_id'] = 1
        results = get_schools(params)
        self.assertEqual(1, len(results), "Number of schoos for the district")
        self.assertEqual('Daybreak Elementary School', results[0]['school_name'], 'school_name: Daybreak Elementary School')
        self.assertEqual(1, results[0]['school_id'], 'school_id: 1')


if __name__ == "__main__":
    unittest.main()
