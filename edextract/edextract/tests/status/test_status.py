'''
Created on Nov 5, 2013

@author: dip
'''
import unittest
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edextract.status.status import insert_extract_stats, ExtractStatus,\
    update_extract_stats
from edextract.status.constants import Constants
from edcore.database.stats_connector import StatsDBConnection
from sqlalchemy.sql.expression import select
from datetime import datetime


class TestStatus(Unittest_with_stats_sqlite):

    def test_insert_status(self):
        values = {Constants.TASK_ID: 'abc',
                  Constants.REQUEST_GUID: 'requestId',
                  Constants.TENANT: 'dummy',
                  Constants.USER_GUID: '1234',
                  Constants.EXTRACT_PARAMS: '{}',
                  Constants.EXTRACT_START: datetime.now(),
                  Constants.EXTRACT_STATUS: ExtractStatus.QUEUED}
        insert_extract_stats(values)
        with StatsDBConnection() as connector:
            extract_stats = connector.get_table(Constants.EXTRACT_STATS)
            query = select([extract_stats.c.user_guid.label(Constants.USER_GUID), ],
                           from_obj=[extract_stats])
            query = query.where(extract_stats.c.task_id == 'abc')
            results = connector.get_result(query)
        self.assertIsNotNone(results)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][Constants.USER_GUID], values[Constants.USER_GUID])

    def test_update_status(self):
        values = {Constants.TASK_ID: 'abcd',
                  Constants.REQUEST_GUID: 'requestId2',
                  Constants.TENANT: 'dummy',
                  Constants.USER_GUID: '1234',
                  Constants.EXTRACT_PARAMS: '{}',
                  Constants.EXTRACT_START: datetime.now(),
                  Constants.EXTRACT_STATUS: ExtractStatus.COPIED}
        with StatsDBConnection() as connector:
            extract_stats = connector.get_table(Constants.EXTRACT_STATS)
            stmt = extract_stats.insert(values=values)
            connector.execute(stmt)
            # Test update
            update = {Constants.EXTRACT_STATUS: ExtractStatus.COMPLETED}
            update_extract_stats(values[Constants.TASK_ID], update)
            # Check db
            query = select([extract_stats.c.extract_status.label(Constants.EXTRACT_STATUS), ],
                           from_obj=[extract_stats])
            query = query.where(extract_stats.c.task_id == 'abcd')
            results = connector.get_result(query)
            self.assertIsNotNone(results)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][Constants.EXTRACT_STATUS], update[Constants.EXTRACT_STATUS])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
