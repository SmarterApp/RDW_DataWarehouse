'''
Created on Jul 29, 2013

@author: swimberly
'''
import unittest
import os
import csv
import random
from datetime import date

from DataGeneration.src.models.helper_entities import AssessmentScore
from DataGeneration.src.demographics.demographics import Demographics, L_PERF_1

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class DemographicsTest(unittest.TestCase):

    def setUp(self):
        self.csv_file = write_csv_file()
        self.dem_obj = Demographics(self.csv_file)
        self.dem_id = 'typical1'
        self.dem_categories = ['male', 'dmg_eth_asn', 'dmg_eth_blk', 'dmg_prg_lep', 'dmg_prg_iep',
                               'dmg_prg_tt1', 'dmg_eth_wht', 'female', 'dmg_eth_hsp', 'dmg_eth_ami']

        self.dem_keys = self.dem_categories + ['all']
        self.address_name_list = ['addr_name_%s' % i for i in range(25)]

    def tearDown(self):
        os.remove(self.csv_file)

    def test_Demographics_get_demo_names_with_string(self):
        result = self.dem_obj.get_demo_names(self.dem_id, 'math', '3')
        expected = self.dem_categories

        for val in expected:
            self.assertIn(val, result, 'check that all expeted keys are return')
        self.assertEqual(len(expected), len(result), 'Check that size of both lists are the same')

    def test_Demographics_get_demo_names_with_int(self):
        result = self.dem_obj.get_demo_names(self.dem_id, 'math', 12)
        expected = self.dem_categories

        for val in expected:
            self.assertIn(val, result, 'check that all expected keys are return')
        self.assertEqual(len(expected), len(result), 'Check that size of both lists are the same')

    def test_Demographics_get_grade_demographics_keys_and_values_lengths_int(self):
        result = self.dem_obj.get_grade_demographics(self.dem_id, 'math', 3)

        for key in self.dem_keys:
            self.assertIn(key, result, 'dict contains all keys')
            self.assertIsInstance(result[key], list, 'check value is list')
            self.assertEqual(len(result[key]), 6, 'check length of value')

    def test_Demographics_get_grade_demographics_keys_and_values_lengths_string(self):
        result = self.dem_obj.get_grade_demographics(self.dem_id, 'math', '12')

        for key in self.dem_keys:
            self.assertIn(key, result, 'dict contains all keys')
            self.assertIsInstance(result[key], list, 'check value is list')
            self.assertEqual(len(result[key]), 6, 'check length of value')

    def test_Demographics_get_grade_demographics_demographic_percentage_sums(self):
        # if corrections is added, for percentages that do not sum.
        # data should be added for the appropriate cases
        result = self.dem_obj.get_grade_demographics(self.dem_id, 'math', '3')

        for k in result:
            perc_sum = sum(result[k][L_PERF_1:])
            self.assertEqual(perc_sum, 100, 'check that percentages for %s sum to 100' % k)

    def test_Demographics_get_subject_demographics(self):
        result = self.dem_obj.get_subject_demographics('typical1', 'math')
        self.assertIn('3', result)
        self.assertIn('12', result)

    def test_Demographics_get_grade_demographics_total_values(self):
        result = self.dem_obj.get_grade_demographics_total(self.dem_id, 'math', '3')

        self.assertIsInstance(result, list, 'check result is list')
        self.assertEqual(len(result), 4, 'check the length of the list')

    def test_Demographics_get_grade_demographics_total_values_int(self):
        result = self.dem_obj.get_grade_demographics_total(self.dem_id, 'math', 12)

        self.assertIsInstance(result, list, 'check result is list')
        self.assertEqual(len(result), 4, 'check the length of the list')

    def test_Demographics_get_grade_demographics_percentage_sum(self):
        result = self.dem_obj.get_grade_demographics_total(self.dem_id, 'math', 12)

        perc_sum = sum(result)
        self.assertEqual(perc_sum, 100, 'Check sum of percentages is 100')

    def test_Demographics__parse_file(self):
        result = self.dem_obj._parse_file(self.csv_file)
        self.assertIsInstance(result, dict)
        self.assertIn('typical1', result)
        self.assertIn('math', result['typical1'])
        self.assertIn('3', result['typical1']['ela'])
        self.assertIn('female', result['typical1']['ela']['3'])

    def test_Demographics__add_row(self):
        row = ('typical1', '0', 'math', '3', 'All Students', 'all', '100', '9', '30', '48', '13')
        dem_dict = {}
        expected = {'typical1': {'math': {'3': {'all': [0, 100, 9, 30, 48, 13]}}}}
        result = self.dem_obj._add_row(row, dem_dict)
        self.assertDictEqual(result, expected)

    def test_Demographics__add_row_2(self):
        row = ('typical1', '2', 'math', '3', 'Black or African American', 'dmg_eth_blk', '18', '17', '40', '37', '6')
        dem_dict = {'typical1': {'math': {'3': {'all': [0, 100, 9, 30, 48, 13]}}}}
        expected = {'typical1': {'math': {'3': {'all': [0, 100, 9, 30, 48, 13],
                                                'dmg_eth_blk': [2, 18, 17, 40, 37, 6]}}}}
        result = self.dem_obj._add_row(row, dem_dict)
        self.assertDictEqual(result, expected)

    def test_Demographics__add_row_3(self):
        row = ('typical1', 1, 'ela', '11', 'Female', 'female', 49, 5, 39, 53, 3)
        dem_dict = {'typical1': {'math': {'3': {'all': [0, 100, 9, 30, 48, 13],
                                                'dmg_eth_blk': [2, 18, 17, 40, 37, 6]}}}}
        expected = {'typical1': {'math': {'3': {'all': [0, 100, 9, 30, 48, 13],
                                                'dmg_eth_blk': [2, 18, 17, 40, 37, 6]}},
                                 'ela': {'11': {'female': [1, 49, 5, 39, 53, 3]}}}}
        result = self.dem_obj._add_row(row, dem_dict)
        self.assertDictEqual(result, expected)

    def test_Demographics__construct_dem_list(self):
        row = ('typical1', 1, 'ela', '11', 'Female', 'female', 49, 5, 39, 53, 3)
        result = self.dem_obj._construct_dem_list(row)
        expected = [1, 49, 5, 39, 53, 3]
        self.assertListEqual(result, expected)


def ethnicity_count(demographics):
    count = 0
    for dem in demographics:
        if 'eth' in dem:
            count += 1
    return count


def generate_100_asmt_scores(perf_lvl_percents):
    assessment_scores = []
    score_ranges = [(1200, 1399), (1400, 1799), (1800, 2099), (2100, 2400)]
    for i in range(len(perf_lvl_percents)):
        perf_level = i + 1
        count = perf_lvl_percents[i]
        lo_range = score_ranges[i][0]
        hi_range = score_ranges[i][1]
        assessment_scores += generate_asmt_scores_in_range(count, lo_range, hi_range, perf_level)
    print('assessment_scores', assessment_scores)
    return assessment_scores


def generate_asmt_scores_in_range(count, lo_range, hi_range, perf_level):
    assessment_scores = []

    for _i in range(count):
        score = random.randint(lo_range, hi_range)
        interval_min = score - 50
        interval_max = score + 50
        claim_scores = None
        create_date = date.today()
        assessment_scores.append(AssessmentScore(score, perf_level, interval_min, interval_max, claim_scores, create_date))
    return assessment_scores


def write_csv_file():
    csv_file_data = [
        ('ID', 'grouping', 'subject', 'grade', 'demographic', 'col_name', 'Total', 1, 2, '3', 4),
        ('typical1', '0', 'math', '3', 'All Students', 'all', '100', '9', '30', '48', '13'),
        ('typical1', '1', 'math', '3', 'Female', 'female', '49', '8', '31', '49', '12'),
        ('typical1', '1', 'math', '3', 'Male', 'male', '51', '10', '29', '48', '13'),
        ('typical1', '2', 'math', '3', 'American Indian or Alaska Native', 'dmg_eth_ami', '1', '12', '36', '43', '9'),
        ('typical1', '2', 'math', '3', 'Black or African American', 'dmg_eth_blk', '18', '17', '40', '37', '6'),
        ('typical1', '2', 'math', '3', 'Hispanic or Latino', 'dmg_eth_hsp', '24', '13', '37', '43', '7'),
        ('typical1', '2', 'math', '3', 'Asian or Native Hawaiian/Other Pacific Islander', 'dmg_eth_asn', '9', '3', '16', '53', '28'),
        ('typical1', '2', 'math', '3', 'White', 'dmg_eth_wht', '48', '5', '25', '54', '16'),
        ('typical1', '3', 'math', '3', 'Students with Disabilities  (IEP)', 'dmg_prg_iep', '15', '29', '42', '26', '3'),
        ('typical1', '4', 'math', '3', 'LEP', 'dmg_prg_lep', '9', '23', '42', '32', '3'),
        ('typical1', '5', 'math', '3', 'Economically Disadvantaged', 'dmg_prg_tt1', '57', '13', '37', '42', '8'),

        ('ID', 'grouping', 'subject', 'grade', 'demographic', 'col_name', 'Total', 1, 2, '3', 4),
        ('typical1', '0', 'math', '12', 'All Students', 'all', '100', '7', '32', '41', '20'),
        ('typical1', '1', 'math', '12', 'Female', 'female', '49', '6', '31', '43', '20'),
        ('typical1', '1', 'math', '12', 'Male', 'male', '51', '8', '33', '40', '19'),
        ('typical1', '2', 'math', '12', 'American Indian or Alaska Native', 'dmg_eth_ami', '1', '9', '40', '39', '12'),
        ('typical1', '2', 'math', '12', 'Black or African American', 'dmg_eth_blk', '19', '14', '45', '34', '7'),
        ('typical1', '2', 'math', '12', 'Hispanic or Latino', 'dmg_eth_hsp', '22', '11', '40', '39', '10'),
        ('typical1', '2', 'math', '12', 'Asian or Native Hawaiian/Other Pacific Islander', 'dmg_eth_asn', '8', '2', '14', '37', '47'),
        ('typical1', '2', 'math', '12', 'White', 'dmg_eth_wht', '50', '4', '25', '47', '24'),
        ('typical1', '3', 'math', '12', 'Students with Disabilities  (IEP)', 'dmg_prg_iep', '16', '27', '50', '21', '2'),
        ('typical1', '4', 'math', '12', 'LEP', 'dmg_prg_lep', '9', '23', '42', '32', '3'),
        ('typical1', '5', 'math', '12', 'Economically Disadvantaged', 'dmg_prg_tt1', '56', '20', '38', '39', '3'),

        ('ID', 'grouping', 'subject', 'grade', 'demographic', 'col_name', 'Total', 1, 2, 3, 4),
        ('typical1', 0, 'ela', 3, 'All Students', 'all', 100, 14, 30, 49, 7),
        ('typical1', 1, 'ela', 3, 'Female', 'female', 49, 11, 29, 52, 8),
        ('typical1', 1, 'ela', 3, 'Male', 'male', 51, 16, 33, 46, 5),
        ('typical1', 2, 'ela', 3, 'American Indian or Alaska Native', 'dmg_eth_ami', 1, 18, 36, 42, 4),
        ('typical1', 2, 'ela', 3, 'Black or African American', 'dmg_eth_blk', 18, 21, 40, 37, 2),
        ('typical1', 2, 'ela', 3, 'Hispanic or Latino', 'dmg_eth_hsp', 24, 20, 39, 38, 3),
        ('typical1', 2, 'ela', 3, 'Asian or Native Hawaiian/Other Pacific Islander', 'dmg_eth_asn', 8, 8, 22, 57, 13),
        ('typical1', 2, 'ela', 3, 'White', 'dmg_eth_wht', 48, 9, 25, 57, 9),
        ('typical1', 3, 'ela', 3, 'Students with Disabilities  (IEP)', 'dmg_prg_iep', 15, 45, 37, 17, 1),
        ('typical1', 4, 'ela', 3, 'LEP', 'dmg_prg_lep', 9, 38, 43, 19, 0),
        ('typical1', 5, 'ela', 3, 'Economically Disadvantaged', 'dmg_prg_tt1', 56, 20, 38, 39, 3),

        ('ID', 'grouping', 'subject', 'grade', 'demographic', 'col_name', 'Total', 1, 2, 3, 4),
        ('typical1', 0, 'ela', 11, 'All Students', 'all', 100, 7, 43, 48, 2),
        ('typical1', 1, 'ela', 11, 'Female', 'female', 49, 5, 39, 53, 3),
        ('typical1', 1, 'ela', 11, 'Male', 'male', 51, 9, 46, 44, 1),
        ('typical1', 2, 'ela', 11, 'American Indian or Alaska Native', 'dmg_eth_ami', 1, 10, 52, 37, 1),
        ('typical1', 2, 'ela', 11, 'Black or African American', 'dmg_eth_blk', 19, 11, 59, 30, 0),
        ('typical1', 2, 'ela', 11, 'Hispanic or Latino ', 'dmg_eth_hsp', 22, 12, 55, 33, 0),
        ('typical1', 2, 'ela', 11, 'Asian or Native Hawaiian/Other Pacific Islander', 'dmg_eth_asn', 8, 7, 28, 61, 4),
        ('typical1', 2, 'ela', 11, 'White', 'dmg_eth_wht', 50, 4, 33, 60, 3),
        ('typical1', 3, 'ela', 11, 'Students with Disabilities  (IEP)', 'dmg_prg_iep', 16, 29, 60, 11, 0),
        ('typical1', 4, 'ela', 11, 'LEP', 'dmg_prg_lep', 5, 43, 54, 3, 0),
        ('typical1', 5, 'ela', 11, 'Economically Disadvantaged', 'dmg_prg_tt1', 52, 11, 54, 34, 1)
    ]

    file_path = os.path.join(__location__, 'test_file.csv')

    with open(file_path, 'w') as cfile:
        cwriter = csv.writer(cfile)
        for row in csv_file_data:
            cwriter.writerow(row)

    return file_path


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
