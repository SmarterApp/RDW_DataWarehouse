'''
Created on Nov 5, 2013

@author: dip
'''
import unittest
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite
from edextract.status.status import insert_extract_stats, ExtractStatus,\
    create_new_entry, delete_stats
from edextract.status.constants import Constants
from edcore.database.stats_connector import StatsDBConnection
from sqlalchemy.sql.expression import select
from datetime import datetime


class DummyUser():

    def get_tenants(self):
        return "myTenant"

    def get_guid(self):
        return "myGuid"


class TestStatus(Unittest_with_stats_sqlite):

    def test_insert_status(self):
        values = {Constants.TASK_ID: 'abc',
                  Constants.REQUEST_GUID: 'requestId',
                  Constants.INFO: '{}',
                  Constants.TIMESTAMP: datetime.now(),
                  Constants.STATUS: ExtractStatus.QUEUED}
        insert_extract_stats(values)
        with StatsDBConnection() as connector:
            extract_stats = connector.get_table(Constants.EXTRACT_STATS)
            query = select([extract_stats.c.status.label(Constants.STATUS), ],
                           from_obj=[extract_stats])
            query = query.where(extract_stats.c.task_id == 'abc')
            results = connector.get_result(query)
        self.assertIsNotNone(results)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][Constants.STATUS], values[Constants.STATUS])

    def test_create_new_entry(self):
        values = {'tenant': 'dummy',
                  'uid': '1234',
                  'params': '{}'}
        request_id = 'request_id_1'
        task_id = create_new_entry(DummyUser(), request_id, values)
        self.assertIsNotNone(task_id)
        with StatsDBConnection() as connector:
            extract_stats = connector.get_table(Constants.EXTRACT_STATS)
            query = select([extract_stats.c.task_id.label(Constants.TASK_ID),
                            extract_stats.c.status.label(Constants.STATUS),
                            extract_stats.c.info.label(Constants.INFO),
                            extract_stats.c.request_guid.label(Constants.REQUEST_GUID)],
                           from_obj=[extract_stats])
            query = query.where(extract_stats.c.request_guid == request_id)
            results = connector.get_result(query)
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0][Constants.TASK_ID], task_id)
            self.assertEqual(results[0][Constants.STATUS], ExtractStatus.QUEUED)
            self.assertIn(DummyUser().get_tenants(), results[0][Constants.INFO])
            self.assertIn(DummyUser().get_guid(), results[0][Constants.INFO])
            self.assertEqual(results[0][Constants.REQUEST_GUID], request_id)

    def test_multi_dict_insert(self):
        one = {Constants.TASK_ID: 'abc'}
        two = {Constants.REQUEST_GUID: 'u1'}
        three = {Constants.STATUS: ExtractStatus.ARCHIVED}
        insert_extract_stats(one, two, three)
        with StatsDBConnection() as connector:
            extract_stats = connector.get_table(Constants.EXTRACT_STATS)
            query = select([extract_stats.c.status.label(Constants.STATUS),
                            extract_stats.c.task_id.label(Constants.TASK_ID)],
                           from_obj=[extract_stats])
            query = query.where(extract_stats.c.request_guid == 'u1')
            results = connector.get_result(query)
        self.assertIsNotNone(results)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][Constants.STATUS], three[Constants.STATUS])
        self.assertEqual(results[0][Constants.TASK_ID], one[Constants.TASK_ID])

    def test_delete(self):
        with StatsDBConnection() as connector:
            extract_stats = connector.get_table(Constants.EXTRACT_STATS)
            # Insert test data
            stmt = extract_stats.insert({Constants.REQUEST_GUID: 'abc', Constants.STATUS: 'status'})
            connector.execute(stmt)
            query = select([extract_stats.c.status.label(Constants.STATUS)],
                           from_obj=[extract_stats])
            results = connector.get_result(query)
            self.assertGreater(len(results), 1)
            delete_stats()
            results = connector.get_result(query)
            self.assertEqual(len(results), 0)


if __name__ == "__main__":
    unittest.main()
