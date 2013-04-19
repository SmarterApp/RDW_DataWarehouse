'''
Created on Apr 17, 2013

@author: swimberly
'''
import unittest
import os
from datetime import date
from mock import MagicMock
import generate_data
import generate_entities
from helper_entities_2 import District


class Test(unittest.TestCase):

    def setUp(self):
        self.cut_points = [1400, 1800, 2100]
        self.perf_lvl_dist = {'ELA': {'3': {'percentages': [30, 34, 28, 9]}},
                              'Math': {'3': {'percentages': [14, 42, 37, 7]}}}
        self.score_details = {'min': 1200, 'max': 2400, 'cut_points': [1400, 1800, 2100]}
        self.config_module = ConfigModule()
        self.config_module.PERCENTAGES = 'percentages'
        self.config_module.MIN = 'min'
        self.config_module.MAX = 'max'
        self.config_module.CUT_POINTS = 'cut_points'
        generate_data.config_module = self.config_module

    def test_generate_name_list_dictionary(self):
        list_name_to_path_dictionary = {}
        file_count = 10
        name_count = 50
        file_names = self.create_test_name_files(file_count, name_count)
        for name in file_names:
            list_name_to_path_dictionary[name] = name
        res = generate_data.generate_name_list_dictionary(list_name_to_path_dictionary)

        self.assertEqual(len(res), file_count)
        for name in res:
            number_of_lines = len(res[name])
            self.assertEqual(number_of_lines, name_count)
        self.remove_test_files(file_names)

    def test_generate_district_dictionary(self):
        district_types = {'Big': 2, 'Medium': 6, 'Small': 40}
        res = generate_data.generate_district_dictionary(district_types, ['n1', 'n2', 'n3', 'n4'], ['n11', 'n22', 'n33', 'n44'])
        self.assertEqual(len(res['Big']), 2)
        self.assertEqual(len(res['Medium']), 6)
        self.assertEqual(len(res['Small']), 40)

        for item in res['Big']:
            self.assertIsInstance(item, District)
            self.assertIsNotNone(item.district_name)
            self.assertIsNotNone(item.district_guid)
        for item in res['Medium']:
            self.assertIsInstance(item, District)
            self.assertIsNotNone(item.district_name)
            self.assertIsNotNone(item.district_guid)
        for item in res['Small']:
            self.assertIsInstance(item, District)
            self.assertIsNotNone(item.district_name)
            self.assertIsNotNone(item.district_guid)

    def test_generate_list_of_scores(self):
        total = 100
        res = generate_data.generate_list_of_scores(total, self.score_details, self.perf_lvl_dist, 'Math', 3)
        self.assertEqual(len(res), 100)
        for score in res:
            self.assertGreaterEqual(score, self.score_details['min'])
            self.assertLessEqual(score, self.score_details['max'])

    def test_calcuate_claim_scores(self):
        assmt = self.create_assessment()
        res = generate_data.calculate_claim_scores(2105, assmt, 32, 8, -10, 25)
        for claim in res:
            print(claim.claim_score)

    def test_translate_scores_to_assessment_score(self):
        assmt = self.create_assessment()
        scores = [2180, 1200, 2400, 1590, 1890, 1800, 2100, 1400]
        expected_pl = [4, 1, 4, 2, 3, 3, 4, 2]
        res = generate_data.translate_scores_to_assessment_score(scores, self.cut_points, assmt, 32, 8, -10, 25)
        for i in range(len(res)):
            self.assertEqual(res[i].perf_lvl, expected_pl[i])
            self.assertIn(res[i].perf_lvl, [1, 2, 3, 4])

    def test_get_subset_of_students(self):
        students = [object()] * 100
        print(len(students))
        res = generate_data.get_subset_of_students(students, .9)
        self.assertEqual(len(res), 90)

    def test_set_students_rec_id_and_section_id(self):
        old_section_guid = 'old_id'
        students = generate_entities.generate_students(10, old_section_guid, 5, 'SC', '123', '234', 'school', ['a', 'b'], date.today(), True)
        for stu in students:
            self.assertEqual(stu.section_guid, old_section_guid)
        students = generate_data.set_students_rec_id_and_section_id(students, 'new_id')
        for stu in students:
            self.assertEqual(stu.section_guid, 'new_id')

        students = generate_entities.generate_students(10, old_section_guid, 5, 'SC', '123', '234', 'school', ['a', 'b'], date.today(), True)
        for stu in students:
            self.assertEqual(stu.section_guid, old_section_guid)
        generate_data.set_students_rec_id_and_section_id(students, 'new_id')
        for stu in students:
            self.assertEqual(stu.section_guid, 'new_id')

    # Helper functions
    def create_assessment(self):
        asmts = generate_entities.generate_assessments([5], self.cut_points, date.today(), True, date.today())
        return asmts[0]

    def create_test_name_files(self, file_count, name_count):
        list_name = 'unit_test_file_for_testing{num}'
        file_list = []
        for i in range(file_count):
            file_name = list_name.format(num=i)
            with open(file_name, 'w') as f:
                for i in range(name_count):
                    f.write('name_{0}\n'.format(i))
            file_list.append(file_name)
        return file_list

    def remove_test_files(self, file_list):
        for name in file_list:
            os.remove(name)


class ConfigModule(object):
    pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
