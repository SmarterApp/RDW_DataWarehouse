'''
Created on Jan 8, 2013

@author: swimberly
'''


import gennames
import random
from datetime import date
from entities import Student, Teacher, Parent
from readnaminglists import PeopleNames
from idgen import IdGen
from write_to_csv import create_csv
import constants


# constants
STUDENT = 0
TEACHER = 1
PARENT = 2


def generate_people(person_type, total, school, state_code, male_ratio=0.5, grade=None):
    '''
    Entry point for generating people. If type = STUDENT parents are generated and saved
    Student objects will include the parents ids.
    person_type : STUDENT or TEACHER
    total       : Total number of people to generate
    male_ratio  : male/total, 0 >= n <= 1, Default: 0.5 (50% male)
    Returns     : a list of people objects
    '''

    people = []
    female_total = int(total * (1 - male_ratio))
    male_total = int(total * male_ratio)
    boy_year = date.today().year
    if date.today().month < 8:
        boy_year -= 1

    for i in range(total - male_total - female_total):
        if random.randint(0, 1):
            male_total += 1
        else:
            female_total += 1

    if person_type == STUDENT:
        people, parents = _generate_students(total, male_total, school, state_code)

        for student in people:
            student.dob = assign_dob(grade, boy_year)
        #write parents
        create_csv(parents, constants.PARENTS)

    elif person_type == TEACHER:
        people = _generate_teachers(total, male_total, school, state_code)

    return people


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


def _generate_students(total, male_total, school, state_code):
    '''
    Private
    generates a list of students with created parents
    total      : Total number of people to generate
    male_total : total of those that should be male
    Returns    : a list of students and a list of parents
    '''
    students = []
    parents = []
    peopleNames = PeopleNames()
    idgen = IdGen()

    for i in range(total):
        student = Student()
        gennames.assign_random_name(i, student, male_total, peopleNames)

        student.student_id = idgen.get_id()
        email_string = "%s.%s%d@%s.com" % (student.firstname, student.lastname, random.randint(0, 99), school.school_name.replace(' ', ''))
        student.email = email_string
        #set schoolid
        student.school_id = school.sch_id
        student.state_id = state_code
        #assign address?

        #assign parents
        parentz = _assign_parent(student)

        students.append(student)
        parents.extend(parentz)

    return students, parents


def _generate_teachers(total, male_total, school, state_code):
    '''
    Private
    Generate a list of teachers
    '''

    teachers = []
    idgen = IdGen()
    peopleNames = PeopleNames()
    for i in range(total):
        teacher = Teacher()
        gennames.assign_random_name(i, teacher, male_total, peopleNames)
        teacher.teacher_id = idgen.get_id()

        # other teacher stuff?
        teachers.append(teacher)

    return teachers


def _assign_parent(student):
    '''
    takes a student object and assigns it two parents with the same last name.
    parents will be saved to file. Parent id's will be saved in student object.
    Returns a list of 2 parents
    '''
    lastname = student.lastname
    parent1 = Parent()
    parent2 = Parent()
    peopleNames = PeopleNames()

    parent1.lastname = lastname
    parent2.lastname = lastname

    gennames.assign_random_name(0, parent1, 1, peopleNames, lastname, False)
    gennames.assign_random_name(1, parent2, 1, peopleNames, lastname, False)

    idgen = IdGen()

    parent1.parent_id = idgen.get_id()
    parent2.parent_id = idgen.get_id()

    parent1.student_id = student.student_id
    parent2.student_id = student.student_id

    # student.parents = [parent1.parent_id, parent2.parent_id]

    return [parent1, parent2]

if __name__ == '__main__':

    total = 5000  # 387549  # pop in AL
    ratio = 0.51
    grade = 12

    from time import time

    time_start = time()
    list_of_students = generate_people(STUDENT, total, ratio, grade)
    time_end = time()

    print("Gen time for %s students generated: %.2fs" % (total, time_end - time_start))

    male_count = 0

    print("num gen:", len(list_of_students))
    for st in list_of_students:
        if st.gender == 'male':
            male_count += 1
    print('males', male_count)
    for i in range(0, 5):
        print(list_of_students[i].dob)
