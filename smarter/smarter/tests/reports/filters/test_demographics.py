'''
Created on Jul 16, 2013

@author: tosako
'''
import unittest
from smarter.reports.filters import Constants_filter_names
from smarter.reports.filters.Constants_filter_names import DEMOGRAPHICS_PROGRAM_IEP
from sqlalchemy.sql.expression import true, false, null, select
from smarter.reports.filters.demographics import get_demographic_filter,\
    has_demographics_filters, apply_demographics_filter_to_query
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite_no_data_load,\
    UnittestSmarterDBConnection
from smarter.reports.helpers.constants import Constants


class TestDemographics(Unittest_with_smarter_sqlite_no_data_load):

    def test_get_demographic_program_filter(self):
        test_filter = {}
        value = get_demographic_filter(DEMOGRAPHICS_PROGRAM_IEP, None, test_filter)
        self.assertFalse(value)
        test_filter = {DEMOGRAPHICS_PROGRAM_IEP: [Constants_filter_names.YES]}
        value = get_demographic_filter(DEMOGRAPHICS_PROGRAM_IEP, True, test_filter)
        self.assertEqual(str(value), str(True == true()))
        test_filter = {DEMOGRAPHICS_PROGRAM_IEP: [Constants_filter_names.NO]}
        value = get_demographic_filter(DEMOGRAPHICS_PROGRAM_IEP, False, test_filter)
        self.assertEqual(str(value), str(False == false()))
        test_filter = {DEMOGRAPHICS_PROGRAM_IEP: [Constants_filter_names.NOT_STATED]}
        value = get_demographic_filter(DEMOGRAPHICS_PROGRAM_IEP, None, test_filter)
        self.assertEqual(str(value), str(None == null()))
        test_filter = {DEMOGRAPHICS_PROGRAM_IEP: [Constants_filter_names.YES, Constants_filter_names.NO, Constants_filter_names.NOT_STATED]}
        value = get_demographic_filter(DEMOGRAPHICS_PROGRAM_IEP, None, test_filter)
        self.assertEqual(3, len(value))
        test_filter = {DEMOGRAPHICS_PROGRAM_IEP: [Constants_filter_names.YES, 'whatever']}
        value = get_demographic_filter(DEMOGRAPHICS_PROGRAM_IEP, True, test_filter)
        self.assertEqual(str(value), str(True == true()))

    def test_has_demographics_filters_with_empty_params(self):
        self.assertFalse(has_demographics_filters({}))

    def test_has_demographics_filters_with_no_filters(self):
        self.assertFalse(has_demographics_filters({'notDemographicFilter': 'a'}))

    def test_has_demographics_filters_with_filters(self):
        self.assertTrue(has_demographics_filters({Constants_filter_names.DEMOGRAPHICS_PROGRAM_IEP: 'a'}))
        self.assertTrue(has_demographics_filters({Constants_filter_names.DEMOGRAPHICS_PROGRAM_504: 'a'}))
        self.assertTrue(has_demographics_filters({Constants_filter_names.DEMOGRAPHICS_PROGRAM_LEP: 'a'}))
        self.assertTrue(has_demographics_filters({Constants_filter_names.DEMOGRAPHICS_PROGRAM_TT1: 'a'}))
        self.assertTrue(has_demographics_filters({Constants_filter_names.DEMOGRAPHICS_ETHNICITY: 'a'}))
        self.assertTrue(has_demographics_filters({Constants_filter_names.DEMOGRAPHICS_GENDER: 'a'}))
        self.assertTrue(has_demographics_filters({Constants_filter_names.DEMOGRAPHICS_GRADE: 'a'}))

    def test_apply_demographics_filter_to_query_with_no_filters(self):
        with UnittestSmarterDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
            query = select([fact_asmt_outcome.c.school_guid],
                           from_obj=([fact_asmt_outcome]))
            query = apply_demographics_filter_to_query(query, fact_asmt_outcome, {})
            self.assertIsNone(query._whereclause)

    def test_apply_demographics_filter_to_query_with_grade_filters(self):
        with UnittestSmarterDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
            query = select([fact_asmt_outcome.c.school_guid],
                           from_obj=([fact_asmt_outcome]))
            query = apply_demographics_filter_to_query(query, fact_asmt_outcome, {Constants_filter_names.DEMOGRAPHICS_GRADE: ['3', '4']})
            self.assertIsNotNone(query._whereclause)
            self.assertIn("fact_asmt_outcome.asmt_grade", str(query._whereclause))

    def test_apply_demographics_filter_to_query_with_iep_filters(self):
        with UnittestSmarterDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
            query = select([fact_asmt_outcome.c.school_guid],
                           from_obj=([fact_asmt_outcome]))
            query = apply_demographics_filter_to_query(query, fact_asmt_outcome, {Constants_filter_names.DEMOGRAPHICS_PROGRAM_IEP: [Constants_filter_names.YES]})
            self.assertIsNotNone(query._whereclause)
            self.assertIn("fact_asmt_outcome.dmg_prg_iep", str(query._whereclause))

    def test_apply_demographics_filter_to_query_with_lep_filters(self):
        with UnittestSmarterDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
            query = select([fact_asmt_outcome.c.school_guid],
                           from_obj=([fact_asmt_outcome]))
            query = apply_demographics_filter_to_query(query, fact_asmt_outcome, {Constants_filter_names.DEMOGRAPHICS_PROGRAM_LEP: [Constants_filter_names.NO]})
            self.assertIsNotNone(query._whereclause)
            self.assertIn("fact_asmt_outcome.dmg_prg_lep", str(query._whereclause))

    def test_apply_demographics_filter_to_query_with_504_filters(self):
        with UnittestSmarterDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
            query = select([fact_asmt_outcome.c.school_guid],
                           from_obj=([fact_asmt_outcome]))
            query = apply_demographics_filter_to_query(query, fact_asmt_outcome, {Constants_filter_names.DEMOGRAPHICS_PROGRAM_504: [Constants_filter_names.NOT_STATED]})
            self.assertIsNotNone(query._whereclause)
            self.assertIn("fact_asmt_outcome.dmg_prg_504", str(query._whereclause))

    def test_apply_demographics_filter_to_query_with_tt1_filters(self):
        with UnittestSmarterDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
            query = select([fact_asmt_outcome.c.school_guid],
                           from_obj=([fact_asmt_outcome]))
            query = apply_demographics_filter_to_query(query, fact_asmt_outcome, {Constants_filter_names.DEMOGRAPHICS_PROGRAM_TT1: [Constants_filter_names.YES]})
            self.assertIsNotNone(query._whereclause)
            self.assertIn("fact_asmt_outcome.dmg_prg_tt1", str(query._whereclause))

    def test_apply_demographics_filter_to_query_with_ethnic_filters(self):
        with UnittestSmarterDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
            query = select([fact_asmt_outcome.c.school_guid],
                           from_obj=([fact_asmt_outcome]))
            query = apply_demographics_filter_to_query(query, fact_asmt_outcome, {Constants_filter_names.DEMOGRAPHICS_ETHNICITY: [Constants_filter_names.DEMOGRAPHICS_ETHNICITY_AMERICAN]})
            self.assertIsNotNone(query._whereclause)
            self.assertIn("fact_asmt_outcome.dmg_eth_derived", str(query._whereclause))

    def test_apply_demographics_filter_to_query_with_gender_filters(self):
        with UnittestSmarterDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
            query = select([fact_asmt_outcome.c.school_guid],
                           from_obj=([fact_asmt_outcome]))
            query = apply_demographics_filter_to_query(query, fact_asmt_outcome, {Constants_filter_names.DEMOGRAPHICS_GENDER: [Constants_filter_names.DEMOGRAPHICS_GENDER_FEMALE, Constants_filter_names.DEMOGRAPHICS_GENDER_MALE]})
            self.assertIsNotNone(query._whereclause)
            self.assertIn("fact_asmt_outcome.gender", str(query._whereclause))

    def test_apply_demographics_filter_to_query_with_multi_filters(self):
        with UnittestSmarterDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME)
            query = select([fact_asmt_outcome.c.school_guid],
                           from_obj=([fact_asmt_outcome]))
            filters = {Constants_filter_names.DEMOGRAPHICS_GENDER: [Constants_filter_names.DEMOGRAPHICS_GENDER_FEMALE],
                       Constants_filter_names.DEMOGRAPHICS_PROGRAM_IEP: [Constants_filter_names.NOT_STATED],
                       Constants_filter_names.DEMOGRAPHICS_ETHNICITY: [Constants_filter_names.DEMOGRAPHICS_ETHNICITY_MULTI]}
            query = apply_demographics_filter_to_query(query, fact_asmt_outcome, filters)
            self.assertIsNotNone(query._whereclause)
            self.assertIn("fact_asmt_outcome.gender", str(query._whereclause))
            self.assertIn("fact_asmt_outcome.dmg_eth_derived", str(query._whereclause))
            self.assertIn("fact_asmt_outcome.dmg_prg_iep", str(query._whereclause))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_value_NONE']
    unittest.main()
