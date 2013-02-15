'''
Created on Jan 16, 2013

@author: swimberly
'''

import os
import unittest

from genpeople import generate_teacher, generate_student, assign_dob, generate_parents, generate_staff
from nameinfo import NameInfo
from entities import State, District, Teacher, School, Student, Parent, Staff
from uuid import UUID, uuid4
from datetime import date


class Test(unittest.TestCase):

    def tearDown(self):
        try:
            basepath = os.path.dirname(__file__)
            parentfile = os.path.abspath(os.path.join(basepath, '..', 'datafiles', 'csv', 'parents.csv'))
            os.remove(parentfile)
        except:
            # File does not exist
            pass

    delaware = State('DE', 'Delaware', 1, state_code='DE')
    district_1 = District(1000, uuid4(), 'district_1', 'DE', 1, {'Dover': [10000, 20000]})
    school_1 = School(2000, uuid4(), 'School 1', district_1.district_name, district_1.district_id, 'DE', 1, 1, 1, 12)
    student_1 = Student(3000, uuid4(), 'John', 'Doe', '55 Washington St', date(2013, 2, 14), district_1, delaware, 'male', 'johndoe@school.edu', school_1)

    def test_generate_teacher(self):
        teacher = generate_teacher(self.delaware, self.district_1)
        self.assertIsNotNone(teacher)
        self.assertIsInstance(teacher, Teacher)
        self.assertIsInstance(teacher.teacher_id, int)
        self.assertIsInstance(teacher.teacher_external_id, UUID)
        self.assertIsInstance(teacher.first_name, str)
        if teacher.middle_name:
            self.assertIsInstance(teacher.middle_name, str)
        self.assertIsInstance(teacher.last_name, str)
        self.assertIsInstance(teacher.district_id, int)
        self.assertIsInstance(teacher.state_code, str)

    def test_generate_student(self):
        student, parents = generate_student(self.delaware, self.district_1, self.school_1, 1, ['park'])
        self.assertIsNotNone(student)
        self.assertIsInstance(student, Student)

    def test_generate_parents(self):
        parents = generate_parents(self.student_1)
        for p in parents:
            self.assertIsNotNone(p)
            self.assertIsInstance(p, Parent)

    def test_generate_staff(self):
        staff = generate_staff('John', 'Doe', self.district_1, self.delaware, self.school_1)
        self.assertIsInstance(staff, Staff)

    def test_assign_dob(self):
        grade = 1
        grade_offset = 6 + grade
        boy_year = 2010

        for i in range(20):
            dob = assign_dob(grade, boy_year)
            expected_year1 = boy_year - grade_offset
            expected_year2 = (boy_year + 1) - grade_offset

            self.assertIn(dob.year, [expected_year1, expected_year2])


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
