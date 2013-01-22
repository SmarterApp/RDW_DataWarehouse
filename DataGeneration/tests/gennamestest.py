'''
Created on Jan 14, 2013

@author: swimberly
'''

import unittest
import operator
from src import gennames
from src.objects.dimensions import Student, Person, Parent
from src.objects.nameinfo import NameInfo
from src.readnaminglists import PeopleNames


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

#    def test_generate_names(self):
#        '''
#        test for gennames.generate_names(...)
#        '''
#
#        # Normal behavior test
#        male_dict = gennames.generate_names('male', 100, self.male_info_list, self.male_info_list[-1].cum_freq * gennames.FREQUENCY_OFFSET)
#        male_dict2 = gennames.generate_names('male', 100000, self.male_info_list, self.male_info_list[-1].cum_freq * gennames.FREQUENCY_OFFSET)
#
#        self.assertEqual(sum(male_dict.values()), 100)
#        self.assertEqual(sum(male_dict2.values()), 100000)

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

    def test_assign_random_name(self):
        '''
        test for gennames.assign_random_names(...)
        '''

        # Normal behavior test
        person1 = Student()  # male
        person2 = Person()  # male
        person3 = Student()  # female
        person4 = Person()  # female

        gennames.assign_random_name(0, person1, 5, self.peopleNames)
        gennames.assign_random_name(7, person3, 5, self.peopleNames)

        person2 = gennames.assign_random_name(1, person2, 5, self.peopleNames)
        person4 = gennames.assign_random_name(8, person4, 5, self.peopleNames)

        self.assertIsNotNone(person1.firstname)
        self.assertIsNotNone(person1.middlename)
        self.assertIsNotNone(person1.lastname)
        self.assertIn(person1.firstname, self.male_list)
        self.assertIn(person1.middlename, self.male_list)
        self.assertIn(person1.lastname, self.last_list)

        self.assertIsNotNone(person2.firstname)
        self.assertIsNotNone(person2.middlename)
        self.assertIsNotNone(person2.lastname)
        self.assertIn(person2.firstname, self.male_list)
        self.assertIn(person2.middlename, self.male_list)
        self.assertIn(person2.lastname, self.last_list)

        self.assertIsNotNone(person3.firstname)
        self.assertIsNotNone(person3.middlename)
        self.assertIsNotNone(person3.lastname)
        self.assertIn(person3.firstname, self.female_list)
        self.assertIn(person3.middlename, self.female_list)
        self.assertIn(person3.lastname, self.last_list)

        self.assertIsNotNone(person4.firstname)
        self.assertIsNotNone(person4.middlename)
        self.assertIsNotNone(person4.lastname)
        self.assertIn(person4.firstname, self.female_list)
        self.assertIn(person4.middlename, self.female_list)
        self.assertIn(person4.lastname, self.last_list)

        parent1 = Parent()
        parent2 = Parent()

        gennames.assign_random_name(0, parent1, 1, self.peopleNames)
        gennames.assign_random_name(1, parent2, 1, self.peopleNames)

        self.assertEqual(parent1.gender, 'male')
        self.assertEqual(parent2.gender, 'female')

    def test_get_random_entry(self):
        '''
        test for gennames.get_random_entry
        '''

        # Normal behavior test
        alist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 12]
        result = gennames.get_random_entry(alist)
        self.assertIn(result, alist)

        result = gennames.get_random_entry([2])
        self.assertEquals(result, 2)
        self.assertIsNone(gennames.get_random_entry([]))
        self.assertRaises(TypeError, gennames.get_random_entry, 12345)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
