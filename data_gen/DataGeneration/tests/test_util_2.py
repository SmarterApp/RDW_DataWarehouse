import unittest
import DataGeneration.src.utils.util as util
import re
import datetime
import os
from DataGeneration.src.constants.constants import ASSMT_PERIOD_TO_MONTHS_DICT
from DataGeneration.src.models.entities import Assessment


class TestUtil2(unittest.TestCase):

    def test_generate_district_name_exception(self):
        list_1 = ['red', 'blue', 'green']
        list_2 = ['cat', 'dog', 'bird']
        max_name_length = 1
        self.assertRaises(Exception, util.generate_district_name, list_1, list_2, max_name_length)

    def test_generate_district_name_with_max(self):
        list_1 = ['red', 'blue', 'green']
        list_2 = ['cat', 'dog', 'bird']
        max_name_length = 20
        district_name = util.generate_district_name(list_1, list_2, max_name_length)
        self.assertIsInstance(district_name, str)
        self.assertLessEqual(len(district_name), max_name_length)

    def test_generate_district_name_no_max(self):
        list_1 = ['red', 'blue', 'green']
        list_2 = ['cat', 'dog', 'bird']
        district_name = util.generate_district_name(list_1, list_2)
        self.assertIsInstance(district_name, str)
        component_words = district_name.split()
        # The first two words should always be elements of the two lists
        non_suffix_words = component_words[:2]
        master_list = list_1 + list_2
        for word in non_suffix_words:
            self.assertIn(word, master_list)

    def test_generate_school_name_exception(self):
        list_1 = ['red', 'blue', 'green']
        list_2 = ['cat', 'dog', 'bird']
        max_name_length = 1
        self.assertRaises(Exception, util.generate_school_name, 'High School', list_1, list_2, max_name_length)

    def test_generate_school_name_no_max(self):
        list_1 = ['red', 'blue', 'green']
        list_2 = ['cat', 'dog', 'bird']
        school_name = util.generate_school_name('High School', list_1, list_2)
        self.assertIsInstance(school_name, str)
        component_words = school_name.split()
        # The first two words should always be elements of the two lists
        non_suffix_words = component_words[:2]
        master_list = list_1 + list_2
        for word in non_suffix_words:
            self.assertIn(word, master_list)

    def test_generate_school_name_with_max(self):
        list_1 = ['red', 'blue', 'green']
        list_2 = ['cat', 'dog', 'bird']
        max_name_length = 20
        school_name = util.generate_school_name('High School', list_1, list_2, max_name_length)
        self.assertIsInstance(school_name, str)
        self.assertLessEqual(len(school_name), max_name_length)

    def test_generate_name_from_lists_no_max(self):
        list_1 = ['red', 'blue', 'green']
        list_2 = ['cat', 'dog', 'bird']
        name = util.generate_name_from_lists(list_1, list_2)
        component_words = name.split()
        word_1 = component_words[0]
        word_2 = component_words[1]
        self.assertIn(word_1, list_1)
        self.assertIn(word_2, list_2)

    def test_generate_name_from_lists_with_max(self):
        list_1 = ['red', 'blue', 'green']
        list_2 = ['cat', 'dog', 'bird']
        max_len = 8
        name = util.generate_name_from_lists(list_1, list_2, max_len)
        self.assertIsInstance(name, str)
        self.assertLessEqual(len(name), max_len)

    def test_generate_address(self):
        streets = ['Main', 'Park', 'Front']
        address = util.generate_address(streets)
        self.assertIsNotNone(re.match("\d+ [A-Za-z]+ [A-Za-z]+", address))

    def test_generate_email_address(self):
        email = util.generate_email_address('John', 'Doe', 'test')
        self.assertIsNotNone(re.match("[^@]+@[^@]+\.[^@]+", email))

    def test_generate_dob(self):
        grade = 4
        dob = util.generate_dob(grade)
        # self.assertIsInstance(dob, date)
        aprox_age = grade + 6
        birth_year = datetime.date.today().year - aprox_age
        self.assertEqual(dob[0:4], str(birth_year))

    def test_generate_date_given_assessment(self):
        a = DummyAssessment()
        a.asmt_period_year = 2013
        a.asmt_period = 'Spring'
        asmt_date = util.generate_date_given_assessment(a)
        self.assertIsInstance(asmt_date, datetime.date)
        self.assertEquals(asmt_date.year, a.asmt_period_year)
        self.assertIn(asmt_date.month, ASSMT_PERIOD_TO_MONTHS_DICT[a.asmt_period])
        # TODO: add a better check for the day when get_max_date_from_month() has been replaced with a constant dictionary
        self.assertLessEqual(asmt_date.day, 31)

    def test_get_max_date_from_month_success(self):
        month = 3
        max_date = util.get_max_date_from_month(month)
        self.assertLessEqual(max_date, 31)

    def test_chop_year_off_assessment_period(self):
        asmt_period = 'Spring 2011'
        period = util.chop_year_off_asmt_period(asmt_period)
        self.assertIsInstance(period, str)
        self.assertEquals(period, 'Spring')

    def test_select_assessment_from_list_none(self):
        asmt_1 = Assessment(1, 'guid_1', 'summative', '2013', '2013', 'V1', 'subject1',
                            2, '01/01/13', True)
        asmt_2 = Assessment(2, 'guid_2', 'summative', '2013', '2013', 'V1', 'subject2',
                            1, '01/01/13', True)
        asmt_list = [asmt_1, asmt_2]
        grade = 3
        subject = 'unknown'
        actual_asmt = util.select_assessment_from_list(asmt_list, grade, subject)
        self.assertIsNone(actual_asmt)

    def test_select_assessment_from_list(self):
        asmt_1 = Assessment(1, 'guid_1', 'summative', '2013', '2013', 'V1', 'subject1',
                            3, '01/01/13', True)
        asmt_2 = Assessment(2, 'guid_2', 'summative', '2013', '2013', 'V1', 'subject2',
                            1, '01/01/13', True)
        asmt_list = [asmt_1, asmt_2]
        grade = 3
        subject = 'subject1'
        actual_asmt = util.select_assessment_from_list(asmt_list, grade, subject)
        self.assertEqual(actual_asmt, asmt_1)

    def test_get_list_of_cutpoints_three_cut_points(self):
        cut_points = [1200, 1800, 2100]
        asmt_1 = Assessment(1, 'guid_1', 'summative', '2013', '2013', 'V1', 'subject1',
                            3, '01/01/13', True, asmt_cut_point_1=cut_points[0], asmt_cut_point_2=cut_points[1], asmt_cut_point_3=cut_points[2])
        actual_cut_points = util.get_list_of_cutpoints(asmt_1)
        self.assertEqual(actual_cut_points, cut_points)

    def test_get_list_of_cutpoints_four_cut_points(self):
        cut_points = [1200, 1600, 1900, 2100]
        asmt_1 = Assessment(1, 'guid_1', 'summative', '2013', '2013', 'V1', 'subject1',
                            3, '01/01/13', True, asmt_cut_point_1=cut_points[0], asmt_cut_point_2=cut_points[1], asmt_cut_point_3=cut_points[2], asmt_cut_point_4=cut_points[3])
        actual_cut_points = util.get_list_of_cutpoints(asmt_1)
        self.assertEqual(actual_cut_points, cut_points)

    def test_create_list_from_file(self):
        current_file_path = os.path.dirname(os.path.realpath(__file__))
        actual_names = util.create_list_from_file(os.path.join(current_file_path, 'test_data', 'test_file_for_create_list_from_file.txt'))
        expected_names = ['word1', 'word2', 'word3']
        self.assertEqual(actual_names, expected_names)

    def test_combine_dicts_of_lists(self):
        dict_a = {'a': [1, 2, 3, 4, 5, 6], 'b': [1, 2]}
        dict_b = {'a': [7, 8, 9], 'c': [1, 3, 4]}

        result = util.combine_dicts_of_lists(dict_a, dict_b)
        expected = {'a': [1, 2, 3, 4, 5, 6, 7, 8, 9], 'b': [1, 2], 'c': [1, 3, 4]}

        self.assertDictEqual(result, expected)


class DummyAssessment(object):
    pass
