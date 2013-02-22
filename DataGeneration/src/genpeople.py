'''
Created on Jan 8, 2013

@author: swimberly
'''

from datetime import date
from uuid import uuid4
import random

from entities import Student, Teacher, Parent, Staff, ExternalUserStudent
from idgen import IdGen
import gennames
import util


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


def generate_parents(student):

    parent_1_params = {
        'first_name': gennames.generate_first_or_middle_name('male'),
        'last_name': student.last_name,
        'address_1': student.address_1,
        'city': student.city,
        'state_code': student.state_code,
        'zip_code': student.zip_code
    }

    parent_2_params = {
        'first_name': gennames.generate_first_or_middle_name('female'),
        'last_name': student.last_name,
        'address_1': student.address_1,
        'city': student.city,
        'state_code': student.state_code,
        'zip_code': student.zip_code
    }

    parent1 = Parent(**parent_1_params)
    parent2 = Parent(**parent_2_params)

    # parent1.student_id = student.student_id
    # parent2.student_id = student.student_id

    return [parent1, parent2]


def generate_staff(district, state, school):

    staff_gender = random.choice(['male', 'female'])
    staff_has_middle_name = random.randint(0, 1)

    staff_params = {
        'first_name': gennames.generate_first_or_middle_name(staff_gender),
        'middle_name': gennames.generate_first_or_middle_name(staff_gender) if staff_has_middle_name else None,
        'last_name': gennames.generate_last_name(),
        'district_id': district.district_id,
        'state_code': state.state_code,
        'school_id': school.school_id
    }

    staff = Staff(**staff_params)

    return staff


def assign_dob(grade, boy_year):
    '''
    Takes a grade and returns a dob that fits in that range
    grade -- the grade the student is in as an int
    boy_year -- the year during the beginning of year as int
    '''
    month_cutoff = 8  # August
    age_offset = grade + 6
    month_num_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # number of days in each month

    year_1 = boy_year
    year_2 = boy_year + 1

    month = random.randint(1, 12)
    day = random.randint(1, month_num_days[month - 1])
    year = 0

    if month > month_cutoff:
        year = year_1 - age_offset
    else:
        year = year_2 - age_offset

    return date(year, month, day)


# if __name__ == '__main__':
#
#    total = 5000  # 387549  # pop in AL
#    ratio = 0.51
#    grade = 12
#
#    from time import time
#
#    time_start = time()
#    list_of_students = generate_people(STUDENT, total, ratio, grade)
#    time_end = time()
#
#    print("Gen time for %s students generated: %.2fs" % (total, time_end - time_start))
#
#    male_count = 0
#
#    print("num gen:", len(list_of_students))
#    for st in list_of_students:
#        if st.gender == 'male':
#            male_count += 1
#    print('males', male_count)
#    for i in range(0, 5):
#        print(list_of_students[i].dob)
