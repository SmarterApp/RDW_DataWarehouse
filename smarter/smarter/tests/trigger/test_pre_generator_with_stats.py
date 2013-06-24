'''
Created on Jun 22, 2013

@author: tosako
'''
import unittest
from smarter.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from smarter.trigger.pre_generator import get_ed_stats, \
    update_ed_stats_for_precached
from smarter.trigger.database.connector import StatsDBConnection
from sqlalchemy.sql.expression import select, and_


class Test(Unittest_with_stats_sqlite):

    def testGet_ed_stats_for_precached(self):
        results = get_ed_stats()
        self.assertEqual(1, len(results))

    def testUpdate_ed_stats_for_precached(self):
        update_ed_stats_for_precached('cat', 'NY')
        with StatsDBConnection() as connector:
            udl_stats = connector.get_table('udl_stats')
            query = select([udl_stats.c.last_pre_cached.label('last_pre_cached'), ],
                           from_obj=[udl_stats])
            query = query.where(udl_stats.c.state_code == 'NY')
            query = query.where(and_(udl_stats.c.tenant == 'cat'))
            results = connector.get_result(query)
        self.assertIsNotNone(results)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
