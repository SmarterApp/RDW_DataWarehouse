'''
Created on Mar 20, 2013

@author: dip
'''
import unittest
from smarter.reports.helpers.assessments import get_overall_asmt_interval,\
    get_cut_points, get_claims


class TestAssessments(unittest.TestCase):

    def test_get_overall_asmt_interval(self):
        result = {'asmt_score': 1000, 'asmt_score_range_min': 200}
        value = get_overall_asmt_interval(result)
        self.assertEqual(value, 800)

    def test_rearrange_cut_points_with_custom_metadata(self):
        result = {'asmt_custom_metadata': '[{"one":"1"},{"two":"1"},{"three":"1"},{"four":"1"}]',
                  'asmt_cut_point_1': 100,
                  'asmt_cut_point_2': 200,
                  'asmt_cut_point_3': 300,
                  'asmt_cut_point_4': 400,
                  'asmt_cut_point_name_1': 'one',
                  'asmt_cut_point_name_2': 'two',
                  'asmt_cut_point_name_3': 'three',
                  'asmt_cut_point_name_4': 'four',
                  'asmt_cut_point_name_5': 'five',
                  'asmt_score_max': 500}
        formatted_results = get_cut_points(result)
        self.assertNotIn('asmt_custom_metadata', formatted_results)
        self.assertNotIn('asmt_cut_point_name_5', formatted_results)
        self.assertIn('cut_point_intervals', formatted_results)
        # Test that we get 4 intervals
        self.assertEqual(len(formatted_results['cut_point_intervals']), 4)
        self.assertNotIn('asmt_cut_point_2', formatted_results)
        # Test that we get the custom metadata
        self.assertEqual(formatted_results['cut_point_intervals'][0]['one'], '1')
        self.assertEqual(formatted_results['cut_point_intervals'][0]['name'], 'one')
        self.assertEqual(formatted_results['cut_point_intervals'][3]['interval'], '500')

    def test_rearrange_cut_points_with_no_custom_metadata(self):
        result = {'asmt_custom_metadata': None,
                  'asmt_cut_point_1': 100,
                  'asmt_cut_point_2': 200,
                  'asmt_cut_point_3': 300,
                  'asmt_cut_point_4': 400,
                  'asmt_cut_point_name_1': 'one',
                  'asmt_cut_point_name_2': 'two',
                  'asmt_cut_point_name_3': 'three',
                  'asmt_cut_point_name_4': 'four',
                  'asmt_cut_point_name_5': 'five',
                  'asmt_score_max': 500}
        formatted_results = get_cut_points(result)
        self.assertEqual(len(formatted_results['cut_point_intervals'][0].keys()), 2)

    def test_get_claims_with_no_claims(self):
        claims = get_claims(number_of_claims=0, result=None, get_names_only=False)
        self.assertEqual(len(claims), 0)

    def test_get_claims_with_one_claim(self):
        result = {'asmt_cut_point_name_1': 'one',
                  'asmt_claim_1_score_range_min': 1,
                  'asmt_claim_1_score_range_max': 4,
                  'asmt_claim_1_score_min': 2,
                  'asmt_claim_1_score_max': 5,
                  'asmt_score_max': 500,
                  'asmt_claim_1_score': 2,
                  'asmt_claim_1_name': 'name',
                  'asmt_subject': 'ELA'}
        claims = get_claims(number_of_claims=1, result=result, get_names_only=False)
        self.assertEqual(len(result), 3)
        self.assertTrue(len(claims), 1)
        self.assertEqual(claims[0]['name2'], 'Claim 1')

    def test_get_claims_for_Math(self):
        result = {'asmt_cut_point_name_1': 'one',
                  'asmt_claim_1_score_range_min': 1,
                  'asmt_claim_1_score_range_max': 4,
                  'asmt_claim_1_score_min': 2,
                  'asmt_claim_1_score_max': 5,
                  'asmt_score_max': 500,
                  'asmt_claim_1_score': 2,
                  'asmt_claim_1_name': 'name',
                  'asmt_subject': 'Math',
                  'asmt_cut_point_name_2': 'two',
                  'asmt_claim_2_score_range_min': 1,
                  'asmt_claim_2_score_range_max': 4,
                  'asmt_claim_2_score_min': 2,
                  'asmt_claim_2_score_max': 5,
                  'asmt_score_max': 500,
                  'asmt_claim_2_score': 2,
                  'asmt_claim_2_name': 'Two'}
        claims = get_claims(number_of_claims=2, result=result, get_names_only=False)
        self.assertEqual(len(result), 4)
        self.assertTrue(len(claims), 2)
        self.assertEqual(claims[1]['name2'], 'Claim 2 & 4')

    def test_get_claims_for_names_only(self):
        result = {'asmt_cut_point_name_1': 'one',
                  'asmt_claim_1_score_range_min': 1,
                  'asmt_claim_1_score_range_max': 4,
                  'asmt_claim_1_score_min': 2,
                  'asmt_claim_1_score_max': 5,
                  'asmt_score_max': 500,
                  'asmt_claim_1_score': 2,
                  'asmt_claim_1_name': 'name',
                  'asmt_subject': 'ELA',
                  'asmt_cut_point_name_2': 'two',
                  'asmt_claim_2_score_range_min': 1,
                  'asmt_claim_2_score_range_max': 4,
                  'asmt_claim_2_score_min': 2,
                  'asmt_claim_2_score_max': 5,
                  'asmt_score_max': 500,
                  'asmt_claim_2_score': 2,
                  'asmt_claim_2_name': 'Two'}
        claims = get_claims(number_of_claims=2, result=result, get_names_only=True)
        self.assertEqual(len(result), 4)
        self.assertTrue(len(claims), 2)
        self.assertEqual(claims[1]['name2'], 'Claim 2')
        self.assertEqual(len(claims[0]), 2)
        self.assertEqual(len(claims[1]), 2)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
