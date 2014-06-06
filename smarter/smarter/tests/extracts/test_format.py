'''
Created on Nov 16, 2013

@author: dip
'''
import unittest
from smarter.extracts.format import setup_input_file_format, get_column_mapping
from smarter.reports.helpers.constants import Constants


class TestFormat(unittest.TestCase):

    def setUp(self):
        setup_input_file_format()

    def test_dim_asmt_mapping_from_json(self):
        dim_asmt = get_column_mapping(Constants.DIM_ASMT, True)
        self.assertIsNotNone(dim_asmt)
        self.assertEqual(dim_asmt['asmt_guid'], 'Identification.Guid')
        self.assertEqual(dim_asmt['asmt_claim_1_name'], 'Claims.Claim1.Name')
        self.assertEqual(dim_asmt['asmt_perf_lvl_name_1'], 'PerformanceLevels.Level1.Name')
        self.assertEqual(dim_asmt['asmt_score_min'], 'Overall.MinScore')
        self.assertEqual(dim_asmt['asmt_claim_1_score_max'], 'Claims.Claim1.MaxScore')
        self.assertEqual(dim_asmt['asmt_cut_point_3'], 'PerformanceLevels.Level4.CutPoint')

    def test_workaround_with_asmt_guid(self):
        dim_asmt = get_column_mapping(Constants.DIM_ASMT)
        self.assertIsNotNone(dim_asmt)
        self.assertEqual(dim_asmt['asmt_guid'], 'AssessmentGuid')

    def test_dim_student_mapping(self):
        dim_student = get_column_mapping(Constants.DIM_STUDENT)
        self.assertIsNotNone(dim_student)
        self.assertEqual(dim_student['student_guid'], 'StudentIdentifier')
        self.assertEqual(dim_student['first_name'], 'FirstName')
        self.assertEqual(dim_student['sex'], 'Sex')
        self.assertEqual(dim_student['birthdate'], 'Birthdate')

    def test_dim_inst_hier(self):
        dim_inst = get_column_mapping(Constants.DIM_INST_HIER)
        self.assertIsNotNone(dim_inst)
        self.assertEqual(dim_inst['state_name'], 'StateName')
        self.assertEqual(dim_inst['state_code'], 'StateAbbreviation')
        self.assertEqual(dim_inst['district_guid'], 'ResponsibleDistrictIdentifier')
        self.assertEqual(dim_inst['district_name'], 'OrganizationName')

    def test_fact_asmt_outcome_vw(self):
        fact = get_column_mapping(Constants.FACT_ASMT_OUTCOME_VW)
        self.assertIsNotNone(fact)
        self.assertEqual(fact['student_guid'], 'StudentIdentifier')
        self.assertEqual(fact['where_taken_id'], 'AssessmentSessionLocationId')
        self.assertEqual(fact['where_taken_name'], 'AssessmentSessionLocation')
        self.assertEqual(fact['enrl_grade'], 'GradeLevelWhenAssessed')
        self.assertEqual(fact['date_taken'], 'AssessmentAdministrationFinishDate')
        self.assertEqual(fact['asmt_score'], 'AssessmentSubtestResultScoreValue')
        self.assertEqual(fact['asmt_score_range_min'], 'AssessmentSubtestMinimumValue')
        self.assertEqual(fact['asmt_perf_lvl'], 'AssessmentPerformanceLevelIdentifier')
        self.assertEqual(fact['asmt_claim_1_score'], 'AssessmentSubtestResultScoreClaim1Value')
        self.assertEqual(fact['asmt_claim_1_score_range_max'], 'AssessmentSubtestClaim1MaximumValue')
        self.assertEqual(fact['sex'], 'Sex')
        self.assertEqual(fact['acc_closed_captioning_embed'], 'AccommodationClosedCaptioning')
        self.assertEqual(fact['acc_print_on_demand_nonembed'], 'AccommodationPrintOnDemand')
        self.assertEqual(fact['acc_streamline_mode'], 'AccommodationStreamlineMode')

#TODO: add more tests

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
