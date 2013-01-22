'''
Created on Jan 8, 2013

@author: swimberly
'''


from src import gennames
import random
from src.objects.dimensions import Student, Teacher, Parent
from src.readnaminglists import PeopleNames
from src.idgen import IdGen


# constants
STUDENT = 0
TEACHER = 1
PARENT = 2


def generate_people(person_type, total, male_ratio=0.5):
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

    for i in range(total - male_total - female_total):
        if random.randint(0, 1):
            male_total += 1
        else:
            female_total += 1

    if person_type == STUDENT:
        people, parents = _generate_students(total, male_total)
        #write parents
        # TODO: write the list of parents to file
    elif person_type == TEACHER:
        people = _generate_teachers(total, male_total)

    return people


def _generate_students(total, male_total):
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

    for i in range(total):
        student = Student()
        gennames.assign_random_name(i, student, male_total, peopleNames)

        #Assign DOB
        #Assign Email
        #Assign id?
        #eternal studentId???
        #assign parents
        parentz = _assign_parent(student)

        students.append(student)
        parents.extend(parentz)

    return students, parents


def _generate_teachers(total, male_total):
    '''
    Private
    Generate a list of teachers
    '''

    teachers = []
    peopleNames = PeopleNames()
    for i in range(total):
        teacher = Teacher()
        gennames.assign_random_name(i, teacher, male_total, peopleNames)

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

    gennames.assign_random_name(0, parent1, 1, peopleNames, lastname)
    gennames.assign_random_name(1, parent2, 1, peopleNames, lastname)

    idgen = IdGen()

    parent1.pid = idgen.get_id()
    parent2.pid = idgen.get_id()

    student.parents = [parent1.pid, parent2.pid]

    return [parent1, parent2]

if __name__ == '__main__':

    total = 387549  # pop in AL
    ratio = 0.51

    from time import time

    time_start = time()
    list_of_students = generate_people(STUDENT, total, ratio)
    time_end = time()

    print("Gen time for %s students generated: %.2fs" % (total, time_end - time_start))

    male_count = 0

    print("num gen:", len(list_of_students))
    for st in list_of_students:
        if st.gender == 'male':
            male_count += 1
    print('males', male_count)
