'''
Created on Aug 2, 2013

@author: swimberly
'''
import unittest
import uuid
import os
import csv
import numbers

import DataGeneration.src.models.state_population as sp
import DataGeneration.src.demographics.demographics as dmg

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Test(unittest.TestCase):

    def setUp(self):
        self.csv_file = write_demographics_csv()
        self.demo_obj = dmg.Demographics(self.csv_file)
        self.demo_id = 'typical1'
        self.expected_demos = ['all', 'female', 'male', 'dmg_eth_ami', 'dmg_eth_asn', 'dmg_eth_blk', 'dmg_eth_hsp',
                               'dmg_eth_wht', 'dmg_prg_iep', 'dmg_prg_lep', 'dmg_prg_tt1']
        self.grades = [3, 4, 5, 6, 7, 8, 11]

    def tearDown(self):
        os.remove(self.csv_file)

    def test_StatePopulation_get_state_demographics(self):
        state_pop = sp.StatePopulation('Example', 'ES', 'typical_1')
        state_pop.populate_state(get_state_types()['typical_1'], get_district_types(), get_school_types())
        state_pop.get_state_demographics(self.demo_obj, self.demo_id)

        self.assertEqual(len(state_pop.state_demographic_totals), len(self.grades))
        self.verify_demographic_grade_dict_structure(state_pop.state_demographic_totals)

    def test_StatePopulation_populate_state(self):
        state_pop = sp.StatePopulation('Example', 'ES', 'typical_1')
        self.assertEqual(state_pop.districts, [])
        state_pop.populate_state(get_state_types()['typical_1'], get_district_types(), get_school_types())

        self.assertEqual(len(state_pop.districts), 1)

    def test_StatePopulation__generate_districts(self):
        state_pop = sp.StatePopulation('Example', 'ES', 'typical_1')
        self.assertEqual(state_pop.districts, [])
        results = state_pop._generate_districts('Big Average', 5, get_district_types()['Big Average'], get_school_types())

        self.assertEqual(len(results), 5)
        for dist in results:
            self.assertIsInstance(dist, sp.DistrictPopulation)
            self.assertGreater(len(dist.schools), 0)

    def test_DistrictPopulation_determine_district_demographics(self):
        district_pop = sp.DistrictPopulation('Big Average')
        district_pop.populate_district(get_district_types()['Big Average'], get_school_types())
        self.assertEqual(district_pop.district_demographic_totals, {})
        district_pop.determine_district_demographics(self.demo_obj, self.demo_id)

        district_demos = district_pop.district_demographic_totals
        district_pop.determine_district_demographics(self.demo_obj, self.demo_id)
        self.assertEqual(len(district_demos), len(self.grades))
        self.verify_demographic_grade_dict_structure(district_demos)

    def test_DistrictPopulation_populate_district(self):
        district_pop = sp.DistrictPopulation('Big Average')
        self.assertEqual(district_pop.schools, [])
        district_pop.populate_district(get_district_types()['Big Average'], get_school_types())

        self.assertEqual(len(district_pop.schools), 9)

        school_counts = {'Elementary School': 0, 'Middle School': 0, 'High School': 0}
        for school in district_pop.schools:
            school_counts[school.school_type] += 1

        for _k, count in school_counts.items():
            self.assertEqual(count, 3)

    def test_DistrictPopulation__generate_schools_in_school_type(self):
        district_pop = sp.DistrictPopulation('Big Average')
        results = district_pop._generate_schools_in_school_type('Middle School', get_school_types()['Middle School'], 10, 'math')

        self.assertEqual(len(results), 10)
        for sch_pop in results:
            self.assertIsInstance(sch_pop, sp.SchoolPopulation)
            self.assertEqual(sch_pop.school_type, 'Middle School')
            self.assertIsNotNone(sch_pop.total_students_by_grade)

    def test_SchoolPopulation_determine_school_demographic_numbers(self):
        school_pop = sp.SchoolPopulation('Middle School', 'Middle School')
        school_pop.generate_student_numbers(get_school_types()['Middle School'])
        school_pop.determine_school_demographic_numbers(self.demo_obj, self.demo_id)

        school_demo = school_pop.school_demographics
        grades = [6, 7, 8]
        self.assertEqual(len(school_demo), 3)
        for grade in grades:
            self.assertIn(grade, school_demo)
            self.assertIsInstance(school_demo[grade], dict)
            [self.assertIn(dmg, school_demo[grade]) for dmg in self.expected_demos]
        self.verify_demographic_grade_dict_structure(school_demo)

    def test_SchoolPopulation__calculate_grade_demographic_numbers(self):
        school_pop = sp.SchoolPopulation('Middle School', 'Middle School')
        results = school_pop._calculate_grade_demographic_numbers(100, 3, 'math', self.demo_obj, self.demo_id)

        for dmg_key in self.expected_demos:
            self.assertIn(dmg_key, results, 'check that dict, contains all demographic keys')
            self.assertEqual(len(results[dmg_key]), 6)

    def test_SchoolPopulation__calculate_grade_demographic_numbers_with_pld(self):
        school_pop = sp.SchoolPopulation('Middle School', 'Middle School')
        results = school_pop._calculate_grade_demographic_numbers(100, 3, 'math', self.demo_obj, self.demo_id, .5)

        for dmg_key in self.expected_demos:
            self.assertIn(dmg_key, results, 'check that dict, contains all demographic keys')
            self.assertEqual(len(results[dmg_key]), 6)

    def test_SchoolPopulation_generate_student_numbers(self):
        school_pop = sp.SchoolPopulation('Middle School', 'Middle School')
        self.assertIsNone(school_pop.total_students_by_grade)
        school_pop.generate_student_numbers(get_school_types()['Middle School'])
        student_counts = school_pop.total_students_by_grade
        self.assertIsNotNone(student_counts)

        # check each grade
        self.assertEqual(student_counts[6], 50)
        self.assertEqual(student_counts[7], 50)
        self.assertEqual(student_counts[8], 50)

    def test_construct_state_counts_dict(self):
        state_pop = sp.StatePopulation('Example State', 'ES', 'typical_1')
        state_pop.populate_state(get_state_types()['typical_1'], get_district_types(), get_school_types())
        results = sp.construct_state_counts_dict(state_pop)

        self.assertEqual(len(results), 1)
        for guid, district_dict in results.items():
            self.assertIsInstance(guid, uuid.UUID)
            self.assertEqual(len(district_dict), 9)
            for s_guid, grade_dict in district_dict.items():
                self.assertIsInstance(uuid.UUID(s_guid), uuid.UUID)
                [self.assertEqual(v, 50) for _k, v in grade_dict.items()]

    def test_construct_district_counts_dict(self):
        district_pop = sp.DistrictPopulation('Big Average')
        district_pop.populate_district(get_district_types()['Big Average'], get_school_types())
        results = sp.construct_district_counts_dict(district_pop)

        self.assertEqual(len(results), 9)
        for guid, grade_dict in results.items():
            self.assertIsInstance(uuid.UUID(guid), uuid.UUID)
            [self.assertEqual(v, 50) for _k, v in grade_dict.items()]

    def test_calculate_group_demographic_numbers(self):
        total_students = 1000
        group_dict = {'dmg_1': [0, 20, 25, 25, 25, 25],
                      'dmg_2': [0, 40, 30, 50, 15, 15],
                      'dmg_3': [0, 10, 12, 28, 35, 25],
                      'dmg_4': [0, 3, 10, 20, 40, 30],
                      'dmg_5': [0, 27, 20, 20, 20, 40]}
        expected = {'dmg_1': [0, 200, 50, 50, 50, 50],
                    'dmg_2': [0, 400, 120, 200, 60, 60],
                    'dmg_3': [0, 100, 12, 28, 35, 25],
                    'dmg_4': [0, 30, 3, 6, 12, 9],
                    'dmg_5': [0, 270, 54, 54, 54, 108]}
        result = sp.calculate_group_demographic_numbers(group_dict, 0, total_students)
        self.assertDictEqual(result, expected)

    def test_calculate_group_demographic_numbers_2(self):
        total_students = 1000
        group_dict = {'dmg_1': [1, 50, 25, 25, 25, 25]}
        expected = {'dmg_1': [1, 500, 125, 125, 125, 125]}
        result = sp.calculate_group_demographic_numbers(group_dict, 1, total_students)
        self.assertDictEqual(result, expected)

    def test_add_populations(self):
        demo_1 = {3: {'dmg_1': [0, 20, 5, 5, 5, 5], 'dmg_2': [0, 24, 6, 6, 6, 6]},
                  4: {'dmg_1': [0, 20, 5, 5, 5, 5], 'dmg_2': [0, 24, 6, 6, 6, 6]},
                  5: {'dmg_1': [0, 20, 5, 5, 5, 5], 'dmg_2': [0, 24, 6, 6, 6, 6]}}
        demo_2 = {3: {'dmg_1': [0, 10, 2, 2, 2, 4], 'dmg_2': [0, 24, 6, 6, 6, 6]},
                  4: {'dmg_1': [0, 10, 2, 2, 2, 4], 'dmg_2': [0, 24, 6, 6, 6, 6]}}
        expt_1 = {3: {'dmg_1': [0, 30, 7, 7, 7, 9], 'dmg_2': [0, 48, 12, 12, 12, 12]},
                  4: {'dmg_1': [0, 30, 7, 7, 7, 9], 'dmg_2': [0, 48, 12, 12, 12, 12]},
                  5: {'dmg_1': [0, 20, 5, 5, 5, 5], 'dmg_2': [0, 24, 6, 6, 6, 6]}}
        result = sp.add_populations(demo_1, demo_2)
        self.assertDictEqual(result, expt_1)

    def test_add_populations_with_one_empty_dict(self):
        demo_1 = {3: {'dmg_1': [0, 20, 5, 5, 5, 5], 'dmg_2': [0, 24, 6, 6, 6, 6]},
                  4: {'dmg_1': [0, 20, 5, 5, 5, 5], 'dmg_2': [0, 24, 6, 6, 6, 6]},
                  5: {'dmg_1': [0, 20, 5, 5, 5, 5], 'dmg_2': [0, 24, 6, 6, 6, 6]}}
        demo_2 = {}
        expt_1 = {3: {'dmg_1': [0, 20, 5, 5, 5, 5], 'dmg_2': [0, 24, 6, 6, 6, 6]},
                  4: {'dmg_1': [0, 20, 5, 5, 5, 5], 'dmg_2': [0, 24, 6, 6, 6, 6]},
                  5: {'dmg_1': [0, 20, 5, 5, 5, 5], 'dmg_2': [0, 24, 6, 6, 6, 6]}}
        result = sp.add_populations(demo_1, demo_2)
        self.assertDictEqual(result, expt_1)

    def test_add_populations_with_one_empty_dict_2(self):
        demo_1 = {}
        demo_2 = {3: {'dmg_1': [0, 10, 2, 2, 2, 4], 'dmg_2': [0, 24, 6, 6, 6, 6]},
                  4: {'dmg_1': [0, 10, 2, 2, 2, 4], 'dmg_2': [0, 24, 6, 6, 6, 6]}}
        expt_1 = {3: {'dmg_1': [0, 10, 2, 2, 2, 4], 'dmg_2': [0, 24, 6, 6, 6, 6]},
                  4: {'dmg_1': [0, 10, 2, 2, 2, 4], 'dmg_2': [0, 24, 6, 6, 6, 6]}}
        result = sp.add_populations(demo_1, demo_2)
        self.assertDictEqual(result, expt_1)

    def test_add_populations_with_bad_demographics(self):
        demo_1 = {3: {'dmg_1': [0, 20, 5, 5, 5, 5], 'dmg_2': [0, 24, 6, 6, 6, 6]},
                  4: {'dmg_1': [0, 20, 5, 5, 5, 5]},
                  5: {'dmg_1': [0, 20, 5, 5, 5, 5], 'dmg_2': [0, 24, 6, 6, 6, 6]}}
        demo_2 = {3: {'dmg_1': [0, 10, 2, 2, 2, 4], 'dmg_2': [0, 24, 6, 6, 6, 6]},
                  4: {'dmg_1': [0, 10, 2, 2, 2, 4], 'dmg_2': [0, 24, 6, 6, 6, 6]}}
        self.assertRaises(KeyError, sp.add_populations, demo_1, demo_2)

    def test_sum_dict_of_demographics(self):
        demo_1 = {'dmg_1': [0, 20, 5, 5, 5, 5], 'dmg_2': [0, 24, 6, 6, 6, 6], 'dmg_3': [1, 28, 7, 7, 7, 7]}
        demo_2 = {'dmg_1': [0, 12, 3, 3, 3, 3], 'dmg_2': [0, 16, 4, 4, 4, 4], 'dmg_3': [1, 20, 5, 5, 5, 5]}
        expt_0 = {'dmg_1': [0, 32, 8, 8, 8, 8], 'dmg_2': [0, 40, 10, 10, 10, 10], 'dmg_3': [1, 48, 12, 12, 12, 12]}

        result = sp.sum_dict_of_demographics(demo_1, demo_2)
        self.assertDictEqual(result, expt_0)

    def test_sum_dict_of_demographics_with_one_empty_dict_1(self):
        demo_1 = {'dmg_1': [0, 20, 5, 5, 5, 5], 'dmg_2': [0, 24, 6, 6, 6, 6], 'dmg_3': [1, 28, 7, 7, 7, 7]}
        demo_2 = {}
        expt_0 = {'dmg_1': [0, 20, 5, 5, 5, 5], 'dmg_2': [0, 24, 6, 6, 6, 6], 'dmg_3': [1, 28, 7, 7, 7, 7]}

        result = sp.sum_dict_of_demographics(demo_1, demo_2)
        self.assertDictEqual(result, expt_0)

    def test_sum_dict_of_demographics_with_one_empty_dict_2(self):
        demo_1 = {}
        demo_2 = {'dmg_1': [0, 12, 3, 3, 3, 3], 'dmg_2': [0, 16, 4, 4, 4, 4], 'dmg_3': [1, 20, 5, 5, 5, 5]}
        expt_0 = {'dmg_1': [0, 12, 3, 3, 3, 3], 'dmg_2': [0, 16, 4, 4, 4, 4], 'dmg_3': [1, 20, 5, 5, 5, 5]}

        result = sp.sum_dict_of_demographics(demo_1, demo_2)
        self.assertDictEqual(result, expt_0)

    def test_sum_dict_of_demographics_with_two_empty_dict(self):
        result = sp.sum_dict_of_demographics({}, {})
        self.assertDictEqual(result, {})

    def test_sum_dict_of_demographics_non_matching_dicts(self):
        demo_1 = {'dmg_1': [0, 20, 5, 5, 5, 5], 'dmg_2': [0, 24, 6, 6, 6, 6], 'dmg_3': [1, 28, 7, 7, 7, 7]}
        demo_2 = {'dmg_1': [0, 12, 3, 3, 3, 3], 'dmg_2': [0, 16, 4, 4, 4, 4], 'dmg_4': [1, 20, 5, 5, 5, 5]}
        self.assertRaises(KeyError, sp.sum_dict_of_demographics, demo_1, demo_2)

        demo_1 = {'dmg_1': [0, 20, 5, 5, 5, 5], 'dmg_2': [0, 24, 6, 6, 6, 6], 'dmg_4': [1, 28, 7, 7, 7, 7]}
        demo_2 = {'dmg_1': [0, 12, 3, 3, 3, 3], 'dmg_2': [0, 16, 4, 4, 4, 4], 'dmg_4': [1, 20, 5, 5, 5, 5], 'dmg_5': [1, 20, 5, 5, 5, 5]}
        self.assertRaises(KeyError, sp.sum_dict_of_demographics, demo_1, demo_2)

    def test_apply_pld_to_grade_demographics(self):
        demo_1 = {'dmg_1': [0, 80, 20, 10, 20, 50], 'dmg_2': [0, 20, 25, 25, 25, 25], 'dmg_3': [2, 45, 13, 37, 42, 8]}
        pld_adjust = .45
        expected = {'dmg_1': [0, 80, 11, 6, 24, 59], 'dmg_2': [0, 20, 14, 14, 36, 36], 'dmg_3': [2, 45, 8, 21, 58, 13]}
        results = sp.apply_pld_to_grade_demographics(pld_adjust, demo_1)
        self.assertDictEqual(results, expected)

    def test_apply_pld_to_grade_demographics_2(self):
        demo_1 = {'dmg_1': [0, 80, 20, 10, 20, 50], 'dmg_2': [0, 0, 25, 25, 25, 25],
                  'dmg_3': [2, 45, 13, 37, 42, 8], 'dmg_4': [0, 0, 0, 0, 0, 0]}
        pld_adjust = .45
        expected = {'dmg_1': [0, 80, 11, 6, 24, 59], 'dmg_2': [0, 0, 25, 25, 25, 25],
                    'dmg_3': [2, 45, 8, 21, 58, 13], 'dmg_4': [0, 0, 0, 0, 0, 0]}
        results = sp.apply_pld_to_grade_demographics(pld_adjust, demo_1)
        self.assertDictEqual(results, expected)

    ##=========================
    ## Verification methods
    ##=========================
    def verify_demographic_list_structure(self, demo_list):
        self.assertEqual(len(demo_list), 6)
        for val in demo_list:
            self.assertIsInstance(val, numbers.Real)

    def verify_demographic_dict_structure(self, demo_dict):
        self.assertIsInstance(demo_dict, dict)
        self.assertEqual(len(demo_dict), len(self.expected_demos))
        for dmg_key, dmg_list in demo_dict.items():
            self.assertIn(dmg_key, self.expected_demos)
            self.verify_demographic_list_structure(dmg_list)

    def verify_demographic_grade_dict_structure(self, grade_dict):
        self.assertIsInstance(grade_dict, dict)
        for grade, demo_dict in grade_dict.items():
            self.assertIn(grade, self.grades)
            self.verify_demographic_dict_structure(demo_dict)


def get_district_types():
    district_types = {'Big Average': {'school_counts': {'min': 10, 'max': 10, 'avg': 10},
                                      'school_types_and_ratios': {
                                          'High School': 1, 'Middle School': 1, 'Elementary School': 1}}}
    return district_types


def get_school_types():
    school_types = {
        'High School': {'type': 'High School', 'grades': [11], 'students': {'min': 50, 'max': 50, 'avg': 50}},
        'Middle School': {'type': 'Middle School', 'grades': [6, 7, 8], 'students': {'min': 50, 'max': 50, 'avg': 50}},
        'Elementary School': {'type': 'Elementary School', 'grades': [3, 4, 5], 'students': {'min': 50, 'max': 50, 'avg': 50}}}

    return school_types


def get_state_types():
    state_types = {'typical_1': {'district_types_and_counts': {'Big Average': 1},
                                 'subjects_and_percentages': {'Math': .99, 'ELA': .99},
                                 'demographics': 'typical1'}
                   }
    return state_types


def write_demographics_csv():
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
        ('typical1', '0', 'math', '6', 'All Students', 'all', '100', '9', '30', '48', '13'),
        ('typical1', '1', 'math', '6', 'Female', 'female', '49', '8', '31', '49', '12'),
        ('typical1', '1', 'math', '6', 'Male', 'male', '51', '10', '29', '48', '13'),
        ('typical1', '2', 'math', '6', 'American Indian or Alaska Native', 'dmg_eth_ami', '1', '12', '36', '43', '9'),
        ('typical1', '2', 'math', '6', 'Black or African American', 'dmg_eth_blk', '18', '17', '40', '37', '6'),
        ('typical1', '2', 'math', '6', 'Hispanic or Latino', 'dmg_eth_hsp', '24', '13', '37', '43', '7'),
        ('typical1', '2', 'math', '6', 'Asian or Native Hawaiian/Other Pacific Islander', 'dmg_eth_asn', '9', '3', '16', '53', '28'),
        ('typical1', '2', 'math', '6', 'White', 'dmg_eth_wht', '48', '5', '25', '54', '16'),
        ('typical1', '3', 'math', '6', 'Students with Disabilities  (IEP)', 'dmg_prg_iep', '15', '29', '42', '26', '3'),
        ('typical1', '4', 'math', '6', 'LEP', 'dmg_prg_lep', '9', '23', '42', '32', '3'),
        ('typical1', '5', 'math', '6', 'Economically Disadvantaged', 'dmg_prg_tt1', '57', '13', '37', '42', '8'),

        ('ID', 'grouping', 'subject', 'grade', 'demographic', 'col_name', 'Total', 1, 2, '3', 4),
        ('typical1', '0', 'math', '7', 'All Students', 'all', '100', '9', '30', '48', '13'),
        ('typical1', '1', 'math', '7', 'Female', 'female', '49', '8', '31', '49', '12'),
        ('typical1', '1', 'math', '7', 'Male', 'male', '51', '10', '29', '48', '13'),
        ('typical1', '2', 'math', '7', 'American Indian or Alaska Native', 'dmg_eth_ami', '1', '12', '36', '43', '9'),
        ('typical1', '2', 'math', '7', 'Black or African American', 'dmg_eth_blk', '18', '17', '40', '37', '6'),
        ('typical1', '2', 'math', '7', 'Hispanic or Latino', 'dmg_eth_hsp', '24', '13', '37', '43', '7'),
        ('typical1', '2', 'math', '7', 'Asian or Native Hawaiian/Other Pacific Islander', 'dmg_eth_asn', '9', '3', '16', '53', '28'),
        ('typical1', '2', 'math', '7', 'White', 'dmg_eth_wht', '48', '5', '25', '54', '16'),
        ('typical1', '3', 'math', '7', 'Students with Disabilities  (IEP)', 'dmg_prg_iep', '15', '29', '42', '26', '3'),
        ('typical1', '4', 'math', '7', 'LEP', 'dmg_prg_lep', '9', '23', '42', '32', '3'),
        ('typical1', '5', 'math', '7', 'Economically Disadvantaged', 'dmg_prg_tt1', '57', '13', '37', '42', '8'),

        ('ID', 'grouping', 'subject', 'grade', 'demographic', 'col_name', 'Total', 1, 2, '3', 4),
        ('typical1', '0', 'math', '8', 'All Students', 'all', '100', '9', '30', '48', '13'),
        ('typical1', '1', 'math', '8', 'Female', 'female', '49', '8', '31', '49', '12'),
        ('typical1', '1', 'math', '8', 'Male', 'male', '51', '10', '29', '48', '13'),
        ('typical1', '2', 'math', '8', 'American Indian or Alaska Native', 'dmg_eth_ami', '1', '12', '36', '43', '9'),
        ('typical1', '2', 'math', '8', 'Black or African American', 'dmg_eth_blk', '18', '17', '40', '37', '6'),
        ('typical1', '2', 'math', '8', 'Hispanic or Latino', 'dmg_eth_hsp', '24', '13', '37', '43', '7'),
        ('typical1', '2', 'math', '8', 'Asian or Native Hawaiian/Other Pacific Islander', 'dmg_eth_asn', '9', '3', '16', '53', '28'),
        ('typical1', '2', 'math', '8', 'White', 'dmg_eth_wht', '48', '5', '25', '54', '16'),
        ('typical1', '3', 'math', '8', 'Students with Disabilities  (IEP)', 'dmg_prg_iep', '15', '29', '42', '26', '3'),
        ('typical1', '4', 'math', '8', 'LEP', 'dmg_prg_lep', '9', '23', '42', '32', '3'),
        ('typical1', '5', 'math', '8', 'Economically Disadvantaged', 'dmg_prg_tt1', '57', '13', '37', '42', '8'),

        ('ID', 'grouping', 'subject', 'grade', 'demographic', 'col_name', 'Total', 1, 2, '3', 4),
        ('typical1', '0', 'math', '4', 'All Students', 'all', '100', '9', '30', '48', '13'),
        ('typical1', '1', 'math', '4', 'Female', 'female', '49', '8', '31', '49', '12'),
        ('typical1', '1', 'math', '4', 'Male', 'male', '51', '10', '29', '48', '13'),
        ('typical1', '2', 'math', '4', 'American Indian or Alaska Native', 'dmg_eth_ami', '1', '12', '36', '43', '9'),
        ('typical1', '2', 'math', '4', 'Black or African American', 'dmg_eth_blk', '18', '17', '40', '37', '6'),
        ('typical1', '2', 'math', '4', 'Hispanic or Latino', 'dmg_eth_hsp', '24', '13', '37', '43', '7'),
        ('typical1', '2', 'math', '4', 'Asian or Native Hawaiian/Other Pacific Islander', 'dmg_eth_asn', '9', '3', '16', '53', '28'),
        ('typical1', '2', 'math', '4', 'White', 'dmg_eth_wht', '48', '5', '25', '54', '16'),
        ('typical1', '3', 'math', '4', 'Students with Disabilities  (IEP)', 'dmg_prg_iep', '15', '29', '42', '26', '3'),
        ('typical1', '4', 'math', '4', 'LEP', 'dmg_prg_lep', '9', '23', '42', '32', '3'),
        ('typical1', '5', 'math', '4', 'Economically Disadvantaged', 'dmg_prg_tt1', '57', '13', '37', '42', '8'),

        ('ID', 'grouping', 'subject', 'grade', 'demographic', 'col_name', 'Total', 1, 2, '3', 4),
        ('typical1', '0', 'math', '5', 'All Students', 'all', '100', '9', '30', '48', '13'),
        ('typical1', '1', 'math', '5', 'Female', 'female', '49', '8', '31', '49', '12'),
        ('typical1', '1', 'math', '5', 'Male', 'male', '51', '10', '29', '48', '13'),
        ('typical1', '2', 'math', '5', 'American Indian or Alaska Native', 'dmg_eth_ami', '1', '12', '36', '43', '9'),
        ('typical1', '2', 'math', '5', 'Black or African American', 'dmg_eth_blk', '18', '17', '40', '37', '6'),
        ('typical1', '2', 'math', '5', 'Hispanic or Latino', 'dmg_eth_hsp', '24', '13', '37', '43', '7'),
        ('typical1', '2', 'math', '5', 'Asian or Native Hawaiian/Other Pacific Islander', 'dmg_eth_asn', '9', '3', '16', '53', '28'),
        ('typical1', '2', 'math', '5', 'White', 'dmg_eth_wht', '48', '5', '25', '54', '16'),
        ('typical1', '3', 'math', '5', 'Students with Disabilities  (IEP)', 'dmg_prg_iep', '15', '29', '42', '26', '3'),
        ('typical1', '4', 'math', '5', 'LEP', 'dmg_prg_lep', '9', '23', '42', '32', '3'),
        ('typical1', '5', 'math', '5', 'Economically Disadvantaged', 'dmg_prg_tt1', '57', '13', '37', '42', '8'),

        ('ID', 'grouping', 'subject', 'grade', 'demographic', 'col_name', 'Total', 1, 2, '3', 4),
        ('typical1', '0', 'math', '11', 'All Students', 'all', '100', '9', '30', '48', '13'),
        ('typical1', '1', 'math', '11', 'Female', 'female', '49', '8', '31', '49', '12'),
        ('typical1', '1', 'math', '11', 'Male', 'male', '51', '10', '29', '48', '13'),
        ('typical1', '2', 'math', '11', 'American Indian or Alaska Native', 'dmg_eth_ami', '1', '12', '36', '43', '9'),
        ('typical1', '2', 'math', '11', 'Black or African American', 'dmg_eth_blk', '18', '17', '40', '37', '6'),
        ('typical1', '2', 'math', '11', 'Hispanic or Latino', 'dmg_eth_hsp', '24', '13', '37', '43', '7'),
        ('typical1', '2', 'math', '11', 'Asian or Native Hawaiian/Other Pacific Islander', 'dmg_eth_asn', '9', '3', '16', '53', '28'),
        ('typical1', '2', 'math', '11', 'White', 'dmg_eth_wht', '48', '5', '25', '54', '16'),
        ('typical1', '3', 'math', '11', 'Students with Disabilities  (IEP)', 'dmg_prg_iep', '15', '29', '42', '26', '3'),
        ('typical1', '4', 'math', '11', 'LEP', 'dmg_prg_lep', '9', '23', '42', '32', '3'),
        ('typical1', '5', 'math', '11', 'Economically Disadvantaged', 'dmg_prg_tt1', '57', '13', '37', '42', '8'),
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
