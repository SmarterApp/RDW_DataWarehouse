'''
Created on Jan 8, 2013

@author: swimberly
'''

from datetime import date
from uuid import uuid4
import random
from DataGeneration.src.helper_entities import Student
from helper_entities import Teacher

from entities import Staff, StudentSection, ExternalUserStudent
from idgen import IdGen
import gennames
import util
import uuid


# constants
STUDENT = 0
TEACHER = 1
PARENT = 2


def generate_teacher(state, district):

    teacher_gender = random.choice(['male', 'female'])
    teacher_has_middle_name = random.randint(0, 1)
    id_generator = IdGen()

    teacher_params = {
        'teacher_id': id_generator.get_id(),
        'teacher_external_id': uuid4(),
        'first_name': gennames.generate_first_or_middle_name(teacher_gender),
        'middle_name': gennames.generate_first_or_middle_name(teacher_gender) if teacher_has_middle_name else None,
        'last_name': gennames.generate_last_name(),
        'district_id': district.district_id,
        'state_code': state.state_code
    }

    teacher = Teacher(**teacher_params)

    return teacher


def generate_student(state, district, school, grade, street_list, gender=None, has_middle_name=False):

    id_generator = IdGen()

    if gender:
        student_gender = gender
    else:
        student_gender = random.choice(['male', 'female'])

    first_name = gennames.generate_first_or_middle_name(student_gender)

    if has_middle_name:
        middle_name = gennames.generate_first_or_middle_name(student_gender)
    else:
        middle_name = None

    last_name = gennames.generate_last_name()
    domain = school.school_name

    student_params = {
        'student_id': id_generator.get_id(),
        'student_external_id': uuid4(),
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_name,
        'address_1': util.generate_address(street_list),
        'dob': util.generate_dob(grade),
        'state': state,
        'gender': student_gender,
        'email': util.generate_email_address(first_name, last_name, domain),
        'district': district,
        'school': school
    }

    student = Student(**student_params)

    ext_user_params = {
        'external_user_student_id': id_generator.get_id(),
        'external_user_id': uuid4(),
        'student_id': student.student_id,
        'rel_start_date': util.generate_start_date(grade),
        'rel_end_date': ''
    }
    ext_user = ExternalUserStudent(**ext_user_params)

    return student, ext_user


def generate_staff(hier_user_type, state_code='None', district_id='None', school_id='None', section_id='None', first_name=None, middle_name=None, last_Name=None, staff_id=None):
    '''
    Generate one staff who can be state_staff, district_staff, school_non_teaching_staff, and school_teaching_staff
    '''
    id_generator = IdGen()
    staff_gender = random.choice(['male', 'female'])
    if(first_name is None):
        first_name = gennames.generate_first_or_middle_name(staff_gender)
    if(middle_name is None):
        middle_name = gennames.generate_first_or_middle_name(staff_gender)
    if(last_Name is None):
        last_Name = gennames.generate_last_name()
    if(staff_id is None):
        staff_id = id_generator.get_id()

    staff_params = {
        'staff_id': staff_id,
        'staff_external_id': uuid.uuid4(),
        'first_name': first_name,
        'middle_name': middle_name,
        'last_name': last_Name,
        'section_id': section_id,
        'hier_user_type': hier_user_type,
        'state_code': state_code,
        'district_id': district_id,
        'school_id': school_id,
        'from_date': '29991201',
        'to_date': '29991201',
        'most_recent': True
    }
    staff = Staff(**staff_params)
    return staff


def generate_student_section(school, student, section_subject_id, section_id, grade, teacher_id):
        student_section_params = {
            'student': student,
            'section_id': section_id,
            'grade': grade,
            'from_date': '20120901',
            'to_date': '20120901',
            'most_recent': True,
            'teacher_id': teacher_id,
            'section_subject_id': section_subject_id
        }
        student_section = StudentSection(**student_section_params)
        return student_section
