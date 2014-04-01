'''
Created on Mar 28, 2014

@author: dip
'''
import unittest
from edudl2.move_to_target.create_queries import get_delete_candidates,\
    match_delete_record_against_prod, update_matched_fact_asmt_outcome_row
from edudl2.tests.unit_tests.unittest_with_udl2_sqlite import Unittest_with_udl2_sqlite,\
    get_unittest_tenant_name, get_unittest_schema_name,\
    UnittestUDLTargetDBConnection
from edudl2.move_to_target.move_to_target_conf import get_move_to_target_conf


class TestCreateQueries(Unittest_with_udl2_sqlite):

    @classmethod
    def setUpClass(cls):
        Unittest_with_udl2_sqlite.setUpClass()

    def tearDown(self):
        pass

    def test_get_delete_candidates_with_no_match(self):
        matching_conf = {}
        matching_conf['columns'] = ['asmnt_outcome_rec_id']
        matching_conf['condition'] = ['student_guid']
        matching_conf['student_guid'] = 'idontexist'
        results = get_delete_candidates(get_unittest_tenant_name(), get_unittest_schema_name(), 'fact_asmt_outcome', '123', matching_conf)
        self.assertEqual(len(results), 0)

    def test_get_delete_candidates_with_matches(self):
        conf = get_move_to_target_conf()['handle_deletions']
        delete_conf = conf['find_deleted_fact_asmt_outcome_rows']
        matching_conf = {}
        matching_conf['columns'] = delete_conf['columns']
        matching_conf['condition'] = delete_conf['condition']
        # We don't test with 'W'
        matching_conf['rec_status'] = 'C'
        results = get_delete_candidates(get_unittest_tenant_name(), get_unittest_schema_name(), conf['target_table'], '820568d0-ddaa-11e2-a63d-68a86d3c2f82', matching_conf)
        self.assertEqual(len(results), 157)
        self.assertEqual(len(results[0].keys()), len(matching_conf['columns']))

    def test_match_delete_record_against_prod_with_no_match(self):
        matching_conf = {}
        matching_conf['columns'] = ['asmnt_outcome_rec_id']
        matching_conf['condition'] = ['student_guid']
        matching_conf['rec_status'] = 'D'
        matched_preprod_values = {}
        matched_preprod_values['student_guid'] = 'idontexist'
        matched_preprod_values['status'] = 'C'
        results = match_delete_record_against_prod(get_unittest_tenant_name(), get_unittest_schema_name(), 'fact_asmt_outcome', matching_conf, matched_preprod_values)
        self.assertEqual(len(results), 0)

    def test_match_delete_record_against_prod_with_matches(self):
        conf = get_move_to_target_conf()['handle_deletions']['match_delete_fact_asmt_outcome_row_in_prod']
        matching_conf = {}
        matching_conf['columns'] = conf['columns']
        matching_conf['condition'] = conf['condition']
        matching_conf['rec_status'] = conf['rec_status']
        matched_preprod_values = {}
        matched_preprod_values['student_guid'] = 'c95bbd44-bc4e-4441-a451-8f0b6aec8c37'
        matched_preprod_values['status'] = 'W'
        matched_preprod_values['asmt_guid'] = '68177b81-a22a-4d53-a4e0-16d0da50937f'
        matched_preprod_values['date_taken'] = '20151213'
        results = match_delete_record_against_prod(get_unittest_tenant_name(), get_unittest_schema_name(), 'fact_asmt_outcome', matching_conf, matched_preprod_values)
        self.assertEqual(len(results), 1)

    def test_update_matched_fact_asmt_outcome_row_with_no_matches(self):
        matching_conf = {}
        matching_conf['rec_status'] = 'C'
        matching_conf['new_status'] = 'Z'
        matching_conf['columns'] = {'asmt_guid': 'asmt_guid'}
        matched_values = {}
        matched_values['asmnt_outcome_rec_id'] = '123'
        matched_values['student_guid'] = 'idontexit'
        matched_values['asmt_guid'] = '123'
        query = update_matched_fact_asmt_outcome_row(get_unittest_tenant_name(), get_unittest_schema_name(), 'fact_asmt_outcome', '820568d0-ddaa-11e2-a63d-68a86d3c2f82', matching_conf, matched_values)
        with UnittestUDLTargetDBConnection() as conn:
            results = conn.execute(query).rowcount
        self.assertEqual(0, results)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
