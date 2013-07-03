'''
Created on Jan 14, 2013

@author: swimberly
'''

import unittest
import operator
from nameinfo import NameInfo
from readnaminglists import PeopleNames
from StatisticalDataGeneration.src.gennames import generate_first_or_middle_name
from DataGeneration.old_data_generation.src import gennames


class TestGenNames(unittest.TestCase):
    '''
    Tests for gennames module
    '''

    def setUp(self):
        self.peopleNames = PeopleNames()
        self.peopleNames.male_names = ['james', 'james', 'jack', 'jack', 'ben', 'ben', 'jack']
        self.peopleNames.female_names = ['judy', 'judy', 'jane', 'jane', 'laura', 'anna', 'anna']
        self.peopleNames.last_names = ['jones', 'jones', 'jones', 'stephens', 'stephens', 'smith']
        self.name_dict = {'james': 10, 'jack': 12, 'ben': 1, 'tom': 2, 'doug': 2}
        self.male_list = ['james', 'james', 'jack', 'jack', 'ben', 'ben', 'jack']
        self.female_list = ['judy', 'judy', 'jane', 'jane', 'laura', 'anna', 'anna']
        self.last_list = ['jones', 'jones', 'jones', 'stephens', 'stephens', 'smith']
        self.male_info_list = []
        self.female_info_list = []
        self.last_info_list = []

        start_freq = 3.5
        sum_freq = start_freq

        for i in range(10):
            male_info = NameInfo('mname%d' % i, start_freq, sum_freq, i)
            self.male_info_list.append(male_info)

            female_info = NameInfo('fname%d' % i, start_freq, sum_freq, i)
            self.female_info_list.append(female_info)

            last_info = NameInfo('lname%d' % i, start_freq, sum_freq, i)
            self.last_info_list.append(last_info)

            sum_freq += start_freq
            start_freq -= 0.33

        self.male_info_list.sort(key=operator.attrgetter('rank'))
        self.female_info_list.sort(key=operator.attrgetter('rank'))
        self.last_info_list.sort(key=operator.attrgetter('rank'))

    def test_generate_all_names(self):
        '''
        test for gennames.generate_all_names(...)
        '''

        # Normal behavior test
        malename_dict, femalename_dict, lastnames_dict = gennames.generate_all_names(self.male_info_list, self.female_info_list, self.last_info_list)

        self.assertEqual(len(malename_dict), 10)
        self.assertEqual(len(femalename_dict), 10)
        self.assertEqual(len(lastnames_dict), 10)
        self.assertEqual(sum(malename_dict.values()), 1000000)
        self.assertEqual(sum(femalename_dict.values()), 1000000)
        self.assertEqual(sum(lastnames_dict.values()), 1000000)

        malename_dict, femalename_dict, lastnames_dict = gennames.generate_all_names(self.male_info_list, self.female_info_list, self.last_info_list, 100)

        self.assertIn('mname1', malename_dict.keys())
        self.assertIn('lname2', lastnames_dict.keys())
        self.assertIn('fname5', femalename_dict.keys())

        m1, f1, l1 = gennames.generate_all_names([], [], [])
        self.assertIsNone(m1)
        self.assertIsNone(f1)
        self.assertIsNone(l1)

    # TODO: mock the reading of people names
    def test_generate_first_or_middle_name(self):
        name = generate_first_or_middle_name('male')
        self.assertIsInstance(name, str)

    # TODO: mock the reading of people names
    def test_generate_last_name(self):
        name = generate_first_or_middle_name('male')
        self.assertIsInstance(name, str)

    def test_name_dict_to_list(self):
        '''
        test for gennames.name_dict_to_list
        '''

        # Normal behavior test
        res_list = gennames.name_dict_to_list(self.name_dict)

        self.assertEqual(type(res_list), list)
        self.assertEqual(res_list.count('james'), 10)
        self.assertEqual(res_list.count('jack'), 12)
        self.assertEqual(res_list.count('ben'), 1)
        self.assertEqual(res_list.count('tom'), 2)
        self.assertEqual(res_list.count('doug'), 2)

        res_list = gennames.name_dict_to_list({})
        self.assertEqual(res_list, [])

        res_list = gennames.name_dict_to_list({'a': 'a', 'b': 'b', 'c': 10})
        expected = ['c'] * 10
        self.assertEqual(res_list, expected)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
