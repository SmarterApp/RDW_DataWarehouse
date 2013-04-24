import unittest
import util_2 as util
import re
import datetime
from constants_2 import ASSMT_PERIOD_TO_MONTHS_DICT

class TestUtil2(unittest.TestCase):

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


class DummyAssessment(object):
    pass