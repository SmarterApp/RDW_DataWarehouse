'''
Created on Jul 16, 2013

@author: tosako
'''
import unittest
from sqlalchemy.sql.expression import true, false, null, select
from smarter.reports.helpers.filters import _get_filter,\
    has_filters, apply_filter_to_query, FILTERS_PROGRAM_IEP,\
    FILTERS_SEX_FEMALE, FILTERS_ETHNICITY, FILTERS_ETHNICITY_MULTI,\
    FILTERS_SEX_MALE, FILTERS_ETHNICITY_AMERICAN,\
    FILTERS_PROGRAM_504, FILTERS_PROGRAM_LEP, FILTERS_PROGRAM_ECD, FILTERS_PROGRAM_MIG,\
    FILTERS_GRADE, YES, NOT_STATED, NO,\
    reverse_filter_map, get_student_demographic, FILTERS_SEX
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite_no_data_load,\
    UnittestEdcoreDBConnection
from smarter.reports.helpers.constants import Constants


class TestDemographics(Unittest_with_edcore_sqlite_no_data_load):

    def test_get_demographic_program_filter(self):
        test_filter = {}
        value = _get_filter(FILTERS_PROGRAM_IEP, None, test_filter)
        self.assertFalse(value)
        test_filter = {FILTERS_PROGRAM_IEP: [YES]}
        value = _get_filter(FILTERS_PROGRAM_IEP, True, test_filter)
        self.assertEqual(str(value), str(True == true()))
        test_filter = {FILTERS_PROGRAM_IEP: [NO]}
        value = _get_filter(FILTERS_PROGRAM_IEP, False, test_filter)
        self.assertEqual(str(value), str(False == false()))
        test_filter = {FILTERS_PROGRAM_IEP: [NOT_STATED]}
        value = _get_filter(FILTERS_PROGRAM_IEP, None, test_filter)
        self.assertEqual(str(value), str(None == null()))
        test_filter = {FILTERS_PROGRAM_IEP: [YES, NO, NOT_STATED]}
        value = _get_filter(FILTERS_PROGRAM_IEP, None, test_filter)
        self.assertEqual(3, len(value))
        test_filter = {FILTERS_PROGRAM_IEP: [YES, 'whatever']}
        value = _get_filter(FILTERS_PROGRAM_IEP, True, test_filter)
        self.assertEqual(str(value), str(True == true()))

    def test_has_filters_with_empty_params(self):
        self.assertFalse(has_filters({}))

    def test_has_filters_with_no_filters(self):
        self.assertFalse(has_filters({'notDemographicFilter': 'a'}))

    def test_has_filters_with_filters(self):
        self.assertTrue(has_filters({FILTERS_PROGRAM_IEP: 'a'}))
        self.assertTrue(has_filters({FILTERS_PROGRAM_504: 'a'}))
        self.assertTrue(has_filters({FILTERS_PROGRAM_LEP: 'a'}))
        self.assertTrue(has_filters({FILTERS_PROGRAM_ECD: 'a'}))
        self.assertTrue(has_filters({FILTERS_PROGRAM_MIG: 'a'}))
        self.assertTrue(has_filters({FILTERS_ETHNICITY: 'a'}))
        self.assertTrue(has_filters({FILTERS_SEX: 'a'}))
        self.assertTrue(has_filters({FILTERS_GRADE: 'a'}))

    def test_apply_filter_to_query_with_no_filters(self):
        with UnittestEdcoreDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            dim_student = connection.get_table(Constants.DIM_STUDENT)
            query = select([fact_asmt_outcome.c.school_id],
                           from_obj=([fact_asmt_outcome]))
            query = apply_filter_to_query(query, fact_asmt_outcome, dim_student, {})
            self.assertIsNone(query._whereclause)

    def test_apply_filter_to_query_with_grade_filters(self):
        with UnittestEdcoreDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            dim_student = connection.get_table(Constants.DIM_STUDENT)
            query = select([fact_asmt_outcome.c.school_id],
                           from_obj=([fact_asmt_outcome]))
            query = apply_filter_to_query(query, fact_asmt_outcome, dim_student, {FILTERS_GRADE: ['3', '4']})
            self.assertIsNotNone(query._whereclause)
            self.assertIn("fact_asmt_outcome_vw.asmt_grade", str(query._whereclause))

    def test_apply_filter_to_query_with_iep_filters(self):
        with UnittestEdcoreDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            dim_student = connection.get_table(Constants.DIM_STUDENT)
            query = select([fact_asmt_outcome.c.school_id],
                           from_obj=([fact_asmt_outcome]))
            query = apply_filter_to_query(query, fact_asmt_outcome, dim_student, {FILTERS_PROGRAM_IEP: [YES]})
            self.assertIsNotNone(query._whereclause)
            self.assertIn("fact_asmt_outcome_vw.dmg_prg_iep", str(query._whereclause))

    def test_apply_filter_to_query_with_lep_filters(self):
        with UnittestEdcoreDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            dim_student = connection.get_table(Constants.DIM_STUDENT)
            query = select([fact_asmt_outcome.c.school_id],
                           from_obj=([fact_asmt_outcome]))
            query = apply_filter_to_query(query, fact_asmt_outcome, dim_student, {FILTERS_PROGRAM_LEP: [NO]})
            self.assertIsNotNone(query._whereclause)
            self.assertIn("fact_asmt_outcome_vw.dmg_prg_lep", str(query._whereclause))

    def test_apply_filter_to_query_with_504_filters(self):
        with UnittestEdcoreDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            dim_student = connection.get_table(Constants.DIM_STUDENT)
            query = select([fact_asmt_outcome.c.school_id],
                           from_obj=([fact_asmt_outcome]))
            query = apply_filter_to_query(query, fact_asmt_outcome, dim_student, {FILTERS_PROGRAM_504: [NOT_STATED]})
            self.assertIsNotNone(query._whereclause)
            self.assertIn("fact_asmt_outcome_vw.dmg_prg_504", str(query._whereclause))

    def test_apply_filter_to_query_with_ecd_filters(self):
        with UnittestEdcoreDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            dim_student = connection.get_table(Constants.DIM_STUDENT)
            query = select([fact_asmt_outcome.c.school_id],
                           from_obj=([fact_asmt_outcome]))
            query = apply_filter_to_query(query, fact_asmt_outcome, dim_student, {FILTERS_PROGRAM_ECD: [NO]})
            self.assertIsNotNone(query._whereclause)
            self.assertIn("fact_asmt_outcome_vw.dmg_sts_ecd", str(query._whereclause))

    def test_apply_filter_to_query_with_migrant_filters(self):
        with UnittestEdcoreDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            dim_student = connection.get_table(Constants.DIM_STUDENT)
            query = select([fact_asmt_outcome.c.school_id],
                           from_obj=([fact_asmt_outcome]))
            query = apply_filter_to_query(query, fact_asmt_outcome, dim_student, {FILTERS_PROGRAM_MIG: [NOT_STATED]})
            self.assertIsNotNone(query._whereclause)
            self.assertIn("fact_asmt_outcome_vw.dmg_sts_mig", str(query._whereclause))

    def test_apply_filter_to_query_with_ethnic_filters(self):
        with UnittestEdcoreDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            dim_student = connection.get_table(Constants.DIM_STUDENT)
            query = select([fact_asmt_outcome.c.school_id],
                           from_obj=([fact_asmt_outcome]))
            query = apply_filter_to_query(query, fact_asmt_outcome, dim_student, {FILTERS_ETHNICITY: [FILTERS_ETHNICITY_AMERICAN]})
            self.assertIsNotNone(query._whereclause)
            self.assertIn("fact_asmt_outcome_vw.dmg_eth_derived", str(query._whereclause))

    def test_apply_filter_to_query_with_gender_filters(self):
        with UnittestEdcoreDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            dim_student = connection.get_table(Constants.DIM_STUDENT)
            query = select([fact_asmt_outcome.c.school_id],
                           from_obj=([fact_asmt_outcome]))
            query = apply_filter_to_query(query, fact_asmt_outcome, dim_student, {FILTERS_SEX: [FILTERS_SEX_FEMALE, FILTERS_SEX_MALE]})
            self.assertIsNotNone(query._whereclause)
            self.assertIn("fact_asmt_outcome_vw.sex", str(query._whereclause))

    def test_apply_filter_to_query_with_multi_filters(self):
        with UnittestEdcoreDBConnection() as connection:
            fact_asmt_outcome = connection.get_table(Constants.FACT_ASMT_OUTCOME_VW)
            dim_student = connection.get_table(Constants.DIM_STUDENT)
            query = select([fact_asmt_outcome.c.school_id],
                           from_obj=([fact_asmt_outcome]))
            filters = {FILTERS_SEX: [FILTERS_SEX_FEMALE],
                       FILTERS_PROGRAM_IEP: [NOT_STATED],
                       FILTERS_ETHNICITY: [FILTERS_ETHNICITY_MULTI]}
            query = apply_filter_to_query(query, fact_asmt_outcome, dim_student, filters)
            self.assertIsNotNone(query._whereclause)
            self.assertIn("fact_asmt_outcome_vw.sex", str(query._whereclause))
            self.assertIn("fact_asmt_outcome_vw.dmg_eth_derived", str(query._whereclause))
            self.assertIn("fact_asmt_outcome_vw.dmg_prg_iep", str(query._whereclause))

    def test_get_student_demographics(self):
        result = {Constants.DMG_PRG_IEP: True,
                  Constants.DMG_PRG_504: False,
                  Constants.DMG_PRG_LEP: None,
                  Constants.DMG_STS_ECD: False,
                  Constants.DMG_STS_MIG: None,
                  Constants.DMG_ETH_DERIVED: 4,
                  FILTERS_SEX: 'M'}
        dmg = get_student_demographic(result)
        self.assertEqual(dmg[FILTERS_PROGRAM_IEP], YES)
        self.assertEqual(dmg[FILTERS_PROGRAM_504], NO)
        self.assertEqual(dmg[FILTERS_PROGRAM_LEP], NOT_STATED)
        self.assertEqual(dmg[FILTERS_PROGRAM_ECD], NO)
        self.assertEqual(dmg[FILTERS_PROGRAM_MIG], NOT_STATED)
        self.assertEqual(dmg[FILTERS_SEX], 'M')
        self.assertEqual(dmg[FILTERS_ETHNICITY], '4')

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.test_value_NONE']
    unittest.main()
