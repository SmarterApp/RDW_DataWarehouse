'''
Created on Jan 16, 2013

@author: swimberly
'''

import os
import unittest

from genpeople import generate_teacher, generate_student, generate_staff
from entities import Staff, InstitutionHierarchy, Student
from helper_entities import State, District, Teacher, StudentBioInfo
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

    state = State('DE', 'Delaware', 1)
    district_1 = District(1000, 'district_1', 'DE', 'Delaware', 1, {'Dover': [10000, 20000]})
    school_1 = InstitutionHierarchy(1, 1, 1, 12, 'Delaware', 'DE', 'district_id', 'district_name', 'school_id', 'school_name', 'school_category', '2012-09-19', True)
    student_bio_info_1 = StudentBioInfo(3000, uuid4(), 'John', 'Doe', '55 Washington St', date(2013, 2, 14), district_1.district_id, state.state_code, 'male', 'johndoe@school.edu', school_1.school_id, 94108, 'city_1')

    def test_generate_teacher(self):
        teacher = generate_teacher(self.state.state_code, self.district_1.district_id)
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
        section_rec_id = 14
        section_id = 90
        grade = 3
        teacher_id = 1287
        student = generate_student(self.student_bio_info_1, section_rec_id, section_id, grade, teacher_id)
        self.assertIsNotNone(student)
        self.assertIsInstance(student, Student)
        self.assertEqual(student.student_id, self.student_bio_info_1.student_id)

    def test_generate_staff(self):
        staff = generate_staff(self.district_1, self.state, self.school_1)
        self.assertIsInstance(staff, Staff)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
