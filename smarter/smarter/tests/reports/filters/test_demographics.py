'''
Created on Jul 16, 2013

@author: tosako
'''
import unittest
from smarter.reports.filters import Constants_filter_names
from smarter.reports.filters.Constants_filter_names import DEMOGRAPHICS_PROGRAM_IEP
from sqlalchemy.sql.expression import true, false
from smarter.reports.filters.demographics import get_demographic_filter,\
    get_new_criterias, get_false_value_columns, get_ethnicity_filter,\
    get_two_or_more_ethnicity_expr, convert_to_expression
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite_no_data_load,\
    UnittestSmarterDBConnection


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
        self.assertEqual(value, True)
        test_filter = {DEMOGRAPHICS_PROGRAM_IEP: [Constants_filter_names.YES, Constants_filter_names.NO, Constants_filter_names.NOT_STATED]}
        value = get_demographic_filter(DEMOGRAPHICS_PROGRAM_IEP, None, test_filter)
        self.assertEqual(3, len(value))
        test_filter = {DEMOGRAPHICS_PROGRAM_IEP: [Constants_filter_names.YES, 'whatever']}
        value = get_demographic_filter(DEMOGRAPHICS_PROGRAM_IEP, True, test_filter)
        self.assertEqual(str(value), str(True == true()))

    def test_get_new_criterias(self):
        result = get_new_criterias()
        self.assertEqual(len(result.keys()), 6)
        self.assertIn(Constants_filter_names.DEMOGRAPHICS_ETHNICITY_BLACK, result)

    def test_get_false_value_columns_with_Not_Stated(self):
        result = get_false_value_columns(Constants_filter_names.NOT_STATED)
        self.assertEqual(len(result), 6)
        self.assertIn(Constants_filter_names.DEMOGRAPHICS_ETHNICITY_HISPANIC, result)

    def test_get_false_value_columns_with_Hispanic(self):
        result = get_false_value_columns(Constants_filter_names.HSP)
        self.assertEqual(len(result), 0)

    def test_get_false_value_columns(self):
        result = get_false_value_columns(Constants_filter_names.BLK)
        self.assertEqual(len(result), 5)
        self.assertNotIn(Constants_filter_names.DEMOGRAPHICS_ETHNICITY_BLACK, result)

    def test_get_ethnicity_filter_single_filter(self):
        with UnittestSmarterDBConnection() as connection:
            fact_asmt_outcome = connection.get_table('fact_asmt_outcome')
            filters = {'ethnicity': [Constants_filter_names.WHT]}
            clauses = get_ethnicity_filter(filters, fact_asmt_outcome)
            self.assertIsNotNone(clauses)

            expected_clauses = ['fact_asmt_outcome.dmg_eth_wht = true',
                                'fact_asmt_outcome.dmg_eth_hsp = false OR fact_asmt_outcome.dmg_eth_hsp IS NULL',
                                'fact_asmt_outcome.dmg_eth_asn = false OR fact_asmt_outcome.dmg_eth_asn IS NULL']
            for expected in expected_clauses:
                self.assertIn(expected, str(clauses))

    def test_get_ethnicity_filter_two_or_more(self):
        with UnittestSmarterDBConnection() as connection:
            fact_asmt_outcome = connection.get_table('fact_asmt_outcome')
            filters = {'ethnicity': [Constants_filter_names.TWO]}
            clauses = get_ethnicity_filter(filters, fact_asmt_outcome)
            self.assertIsNotNone(clauses)

            expected_clauses = ['fact_asmt_outcome.dmg_eth_wht = true',
                                'fact_asmt_outcome.dmg_eth_hsp = false OR fact_asmt_outcome.dmg_eth_hsp IS NULL',
                                'fact_asmt_outcome.dmg_eth_asn = true']
            for expected in expected_clauses:
                self.assertIn(expected, str(clauses))

    def test_get_ethnicity_filter_Not_Stated(self):
        with UnittestSmarterDBConnection() as connection:
            fact_asmt_outcome = connection.get_table('fact_asmt_outcome')
            filters = {'ethnicity': [Constants_filter_names.NOT_STATED]}
            clauses = get_ethnicity_filter(filters, fact_asmt_outcome)
            self.assertIsNotNone(clauses)

            expected_clauses = ['fact_asmt_outcome.dmg_eth_wht = false OR fact_asmt_outcome.dmg_eth_wht IS NULL',
                                'fact_asmt_outcome.dmg_eth_hsp = false OR fact_asmt_outcome.dmg_eth_hsp IS NULL',
                                'fact_asmt_outcome.dmg_eth_asn = false OR fact_asmt_outcome.dmg_eth_asn IS NULL']
            for expected in expected_clauses:
                self.assertIn(expected, str(clauses))

    def test_get_two_or_more_ethnicity_expr(self):
        with UnittestSmarterDBConnection() as connection:
            fact_asmt_outcome = connection.get_table('fact_asmt_outcome')
            clauses = get_two_or_more_ethnicity_expr(fact_asmt_outcome)
            self.assertIsNotNone(clauses)
            expected_clauses = ['fact_asmt_outcome.dmg_eth_wht = true',
                                'fact_asmt_outcome.dmg_eth_hsp = false OR fact_asmt_outcome.dmg_eth_hsp IS NULL',
                                'fact_asmt_outcome.dmg_eth_asn = true']
            for expected in expected_clauses:
                self.assertIn(expected, str(clauses))

    def test_convert_to_expression_test_true(self):
        with UnittestSmarterDBConnection() as connection:
            fact_asmt_outcome = connection.get_table('fact_asmt_outcome')
            param = {Constants_filter_names.DEMOGRAPHICS_ETHNICITY_PACIFIC: True}
            result = convert_to_expression(param, fact_asmt_outcome)
            self.assertEqual('fact_asmt_outcome.dmg_eth_pcf = true', str(result))

    def test_convert_to_expression_test_false(self):
        with UnittestSmarterDBConnection() as connection:
            fact_asmt_outcome = connection.get_table('fact_asmt_outcome')
            param = {Constants_filter_names.DEMOGRAPHICS_ETHNICITY_PACIFIC: False}
            result = convert_to_expression(param, fact_asmt_outcome)
            self.assertEqual('fact_asmt_outcome.dmg_eth_pcf = false OR fact_asmt_outcome.dmg_eth_pcf IS NULL', str(result))

    def test_convert_to_expression_test_None(self):
        with UnittestSmarterDBConnection() as connection:
            fact_asmt_outcome = connection.get_table('fact_asmt_outcome')
            param = {Constants_filter_names.DEMOGRAPHICS_ETHNICITY_PACIFIC: None}
            result = convert_to_expression(param, fact_asmt_outcome)
            self.assertEqual('', str(result))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_value_NONE']
    unittest.main()
