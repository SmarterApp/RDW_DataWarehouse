'''
Unittest for benchmarks

Created on Feb 25, 2013

@author: swimberly
'''

from mock import MagicMock
import unittest

from compare_populations_grades_within_school import school_statistics
from compare_populations_schools_within_district import district_statistics
from compare_populations_districts_within_state import state_statistics


class Test(unittest.TestCase):

    def setUp(self):
        self.connection = Connection()
        conn_result = ConnResult()
        conn_result.fetchall = MagicMock(return_value=(([10], [12]), []))
        self.connection.execute = MagicMock(return_value=(conn_result))

    def test_school_statistics(self):
        res = school_statistics(1, self.connection, 'schema_name')
        self.assertEquals(len(res), 4)
        benchmarks = res.get('benchmarks')
        stats = res.get('stats')
        self.assertIsNotNone(benchmarks)
        self.assertIsNotNone(stats)
        self.assertIsNotNone(benchmarks['data'][0])

    def test_district_statistics(self):
        res = district_statistics(1, self.connection, 'schema_name')
        self.assertEquals(len(res), 4)
        benchmarks = res.get('benchmarks')
        stats = res.get('stats')
        self.assertIsNotNone(benchmarks)
        self.assertIsNotNone(stats)
        self.assertIsNotNone(benchmarks['data'][0])

    def test_state_statistics(self):
        res = state_statistics(1, self.connection, 'schema_name')
        self.assertEquals(len(res), 4)
        benchmarks = res.get('benchmarks')
        stats = res.get('stats')
        self.assertIsNotNone(benchmarks)
        self.assertIsNotNone(stats)
        self.assertIsNotNone(benchmarks['data'][0])


class Connection(object):
    pass


class ConnResult(object):
    pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
