'''
Created on Nov 5, 2013

@author: dip
'''
import unittest
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edextract.status.status import insert_extract_stats, ExtractStatus,\
    update_extract_stats, create_new_entry
from edextract.status.constants import Constants
from edcore.database.stats_connector import StatsDBConnection
from sqlalchemy.sql.expression import select
from datetime import datetime


class DummyUser():

    def get_tenant(self):
        return "myTenant"

    def get_guid(self):
        return "myGuid"


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

    def test_create_new_entry(self):
        values = {Constants.TENANT: 'dummy',
                  Constants.USER_GUID: '1234',
                  Constants.EXTRACT_PARAMS: '{}'}
        request_id = 'request_id_1'
        task_id = create_new_entry(DummyUser(), request_id, values)
        self.assertIsNotNone(task_id)
        with StatsDBConnection() as connector:
            extract_stats = connector.get_table(Constants.EXTRACT_STATS)
            query = select([extract_stats.c.task_id.label(Constants.TASK_ID),
                            extract_stats.c.extract_status.label(Constants.EXTRACT_STATUS),
                            extract_stats.c.request_guid.label(Constants.REQUEST_GUID),
                            extract_stats.c.user_guid.label(Constants.USER_GUID),
                            extract_stats.c.tenant.label(Constants.TENANT)],
                           from_obj=[extract_stats])
            query = query.where(extract_stats.c.request_guid == request_id)
            results = connector.get_result(query)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][Constants.TASK_ID], task_id)
            self.assertEqual(results[0][Constants.EXTRACT_STATUS], ExtractStatus.QUEUED)
            self.assertEqual(results[0][Constants.TENANT], DummyUser().get_tenant())
            self.assertEqual(results[0][Constants.USER_GUID], DummyUser().get_guid())
            self.assertEqual(results[0][Constants.REQUEST_GUID], request_id)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
