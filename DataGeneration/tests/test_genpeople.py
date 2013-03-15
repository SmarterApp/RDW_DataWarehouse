'''
Created on Jan 16, 2013

@author: swimberly
'''

import os
import unittest

from genpeople import generate_teacher, generate_student, generate_staff
from entities import Staff, ExternalUserStudent, InstitutionHierarchy
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

    delaware = State('DE', 'Delaware', 1)
    district_1 = District(1000, 'district_1', 'DE', 'Delaware', 1, {'Dover': [10000, 20000]})
    school_1 = InstitutionHierarchy(1, 1, 1, 12, 'Delaware', 'DE', 'district_id', 'district_name', 'school_id', 'school_name', 'school_category', '2012-09-19', True)
    student_1 = StudentBioInfo(3000, uuid4(), 'John', 'Doe', '55 Washington St', date(2013, 2, 14), district_1, delaware, 'male', 'johndoe@school.edu', school_1)

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
        student, exter_user = generate_student(self.delaware, self.district_1, self.school_1, 1, ['park'])
        self.assertIsNotNone(student)
        self.assertIsInstance(student, StudentBioInfo)

        self.assertIsNotNone(exter_user)
        self.assertIsInstance(exter_user, ExternalUserStudent)

        self.assertEqual(student.student_id, exter_user.student_id)

    def test_generate_staff(self):
        staff = generate_staff(self.district_1, self.delaware, self.school_1)
        self.assertIsInstance(staff, Staff)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
