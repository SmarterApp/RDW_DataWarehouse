'''
Created on Mar 20, 2013

@author: dip
'''
import unittest
from smarter.reports.helpers.assessments import get_overall_asmt_interval,\
    rearrange_cut_points


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
        formatted_results = rearrange_cut_points(result)
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
        formatted_results = rearrange_cut_points(result)
        self.assertEqual(len(formatted_results['cut_point_intervals'][0].keys()), 2)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
