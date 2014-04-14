import unittest
from edcore.database.utils.constants import UdlStatsConstants
from edudl2.udl2 import message_keys as mk
from edudl2.udl2.W_all_done import _create_stats_row
from json import JSONDecoder

__author__ = 'ablum'


class TestAllDone(unittest.TestCase):

    def test__create_sr_stats_row(self):
        msg = {mk.TOTAL_ROWS_LOADED: 100, mk.LOAD_TYPE: 'studentregistration', mk.REG_SYSTEM_ID: '1234', mk.ACADEMIC_YEAR: 2015}
        endtime = '1111111'
        status = mk.SUCCESS

        results = _create_stats_row(msg, endtime, status)

        self.assertEquals(results['batch_operation'], 's')
        self.assertEquals(results[UdlStatsConstants.LOAD_END], '1111111')
        self.assertEquals(results[UdlStatsConstants.RECORD_LOADED_COUNT], 100)
        self.assertEquals(results[UdlStatsConstants.LOAD_STATUS], UdlStatsConstants.UDL_STATUS_INGESTED)
        snapshot_criteria = JSONDecoder().decode(results[UdlStatsConstants.SNAPSHOT_CRITERIA])
        self.assertEqual(2, len(snapshot_criteria))
        self.assertEqual("1234", snapshot_criteria['reg_system_id'])
        self.assertEqual(2015, snapshot_criteria['academic_year'])

    def test__create_sr_failed_stats_row(self):
        msg = {mk.LOAD_TYPE: 'studentregistration'}
        endtime = '1111111'
        status = mk.FAILURE

        results = _create_stats_row(msg, endtime, status)

        self.assertTrue('batch_operation' not in results)
        self.assertEquals(results[UdlStatsConstants.LOAD_END], '1111111')
        self.assertEquals(results[UdlStatsConstants.RECORD_LOADED_COUNT], 0)
        self.assertEquals(results[UdlStatsConstants.LOAD_STATUS], UdlStatsConstants.UDL_STATUS_FAILED)
        self.assertTrue('snapshot_criteria' not in results)

    def test__create_asmt_stats_row(self):
        msg = {mk.TOTAL_ROWS_LOADED: 100, mk.LOAD_TYPE: 'assessment'}
        endtime = '1111111'
        status = mk.SUCCESS

        results = _create_stats_row(msg, endtime, status)

        self.assertTrue('batch_operation' not in results)
        self.assertEquals(results[UdlStatsConstants.LOAD_END], '1111111')
        self.assertEquals(results[UdlStatsConstants.RECORD_LOADED_COUNT], 100)
        self.assertEquals(results[UdlStatsConstants.LOAD_STATUS], UdlStatsConstants.UDL_STATUS_INGESTED)
        self.assertTrue('snapshot_criteria' not in results)
