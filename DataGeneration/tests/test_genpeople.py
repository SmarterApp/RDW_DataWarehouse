'''
Created on Jan 16, 2013

@author: swimberly
'''

import os
import unittest

import genpeople
from nameinfo import NameInfo
from entities import School


class Test(unittest.TestCase):

    def test_generate_people(self):
        school = School(1, 1, 'school1', 10, 15, 'address1', 'primary', 0, 5, 1, 'cat')
        result = genpeople.generate_people(genpeople.STUDENT, 10, school, 'DE', 0.5, 2)

        self.assertEqual(len(result), 10)
        male_count = 0
        for p in result:
            if p.gender == 'male':
                male_count += 1

        self.assertEqual(male_count, 5)

        self.assertEqual([], genpeople.generate_people(genpeople.STUDENT, 0, school, 'DE', 0, 2))

    def test_assign_dob(self):
        grade = 1
        grade_offset = 6 + grade
        boy_year = 2010

        for i in range(20):
            dob = genpeople.assign_dob(grade, boy_year)
            expected_year1 = boy_year - grade_offset
            expected_year2 = (boy_year + 1) - grade_offset

            self.assertIn(dob.year, [expected_year1, expected_year2])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
