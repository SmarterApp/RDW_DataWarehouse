'''
Created on Mar 1, 2014

@author: dip
'''
import unittest
from edcore.database.utils.query import insert_to_table, update_records_in_table,\
    insert_udl_stats, update_udl_stats
from edcore.database.stats_connector import StatsDBConnection
from sqlalchemy.sql.expression import select
from datetime import datetime
from edcore.database.utils.constants import UdlStatsConstants
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite_no_data_load


class TestQuery(Unittest_with_stats_sqlite_no_data_load):

    def tearDown(self):
        with StatsDBConnection() as conn:
            table = conn.get_table('extract_stats')
            conn.execute(table.delete())

    def test_insert_to_table(self):
        insert_to_table(StatsDBConnection, 'extract_stats', {'request_guid': 'a', 'status': 'C'})
        with StatsDBConnection() as conn:
            table = conn.get_table('extract_stats')
            query = select([table.c.request_guid], from_obj=[table])
            results = conn.get_result(query)
            self.assertEqual(results[0]['request_guid'], 'a')

    def test_update_record_table(self):
        with StatsDBConnection() as conn:
            table = conn.get_table('extract_stats')
            query = table.insert({'request_guid': 'b', 'status': 'C'})
            conn.execute(query)
            update_records_in_table(StatsDBConnection, 'extract_stats', {'status': 'D'}, {'request_guid': 'b'})
            query = select([table.c.status], from_obj=[table])
            results = conn.get_result(query)
            self.assertEqual(results[0]['status'], 'D')

    def test_insert_udl_stats(self):
        udl_stats = {
            UdlStatsConstants.BATCH_GUID: 'abc',
            UdlStatsConstants.LOAD_TYPE: 'test',
            UdlStatsConstants.STATE_CODE: 'AB',
            UdlStatsConstants.FILE_ARRIVED: datetime.now(),
            UdlStatsConstants.TENANT: 'tenant',
            UdlStatsConstants.LOAD_STATUS: UdlStatsConstants.STATUS_RECEIVED
        }
        insert_udl_stats(udl_stats)
        with StatsDBConnection() as conn:
            table = conn.get_table('udl_stats')
            query = select([table.c[UdlStatsConstants.LOAD_TYPE]], from_obj=[table])
            results = conn.get_result(query.where(table.c[UdlStatsConstants.BATCH_GUID] == 'abc'))
            self.assertEqual(results[0][UdlStatsConstants.LOAD_TYPE], 'test')

    def test_update_udl_stats(self):
        udl_stats = {
            UdlStatsConstants.BATCH_GUID: 'cde',
            UdlStatsConstants.LOAD_TYPE: 'test',
            UdlStatsConstants.STATE_CODE: 'AB',
            UdlStatsConstants.FILE_ARRIVED: datetime.now(),
            UdlStatsConstants.TENANT: 'tenant',
            UdlStatsConstants.LOAD_STATUS: UdlStatsConstants.STATUS_RECEIVED
        }
        with StatsDBConnection() as conn:
            table = conn.get_table('udl_stats')
            query = table.insert(udl_stats)
            conn.execute(query)
            update_udl_stats('cde', {UdlStatsConstants.STATE_CODE: 'CD'})
            query = select([table.c[UdlStatsConstants.STATE_CODE]], from_obj=[table]).where(table.c[UdlStatsConstants.BATCH_GUID] == 'cde')
            results = conn.get_result(query)
            self.assertEqual(results[0][UdlStatsConstants.STATE_CODE], 'CD')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
