import random
import string


class State:
    '''
    state object
    '''

    def __init__(self, name, code, num_of_dist):
        '''
        Constructor
        '''
        self.name = name
        self.num_of_dist = num_of_dist
        self.code = code

    def __str__(self):
        '''
        String method
        '''
        return ("State:[name: %s, code:%s, num_of_dist: %s]" % (self.name, self.code, self.num_of_dist))


class District:
    '''
    District object
    '''
    # total_id = 0
    def __init__(self, state_name, dist_name, num_of_schools, address_1, school_type_in_dist):
        '''
        Constructor
        '''
        # self.dist_id   = District.total_id
        # District.total_id = District.total_id + 1
        self.state_name = state_name
        self.dist_name = dist_name
        self.num_of_schools = num_of_schools
        self.address_1 = address_1
        self.school_type_in_dist = school_type_in_dist
        # self.dist_name = 'district-' + generate_ramdom_name()

    def __str__(self):
        '''
        String method
        '''
        return ("District:[state_name: %s, num_of_schools: %s, dist_name: %s, address_1: %s, school_type_in_dist: %s]" % (self.state_name, self.num_of_schools, self.dist_name, self.address_1, self.school_type_in_dist))


class School:
    '''
    School object
    '''
    # total_id = 0
    def __init__(self, dist_name, school_name, num_of_student, num_of_teacher, address1, school_type, low_grade, high_grade):
        '''
        Constructor
        '''
        # self.dist_id   = District.total_id
        # District.total_id = District.total_id + 1
        self.dist_name = dist_name
        self.school_name = school_name
        self.num_of_student = num_of_student
        self.num_of_teacher = num_of_teacher
        self.address1 = address1
        self.school_type = school_type
        self.low_grade = low_grade
        self.high_grade = high_grade

    def __str__(self):
        '''
        String method
        '''
        return ("School:[dist_name: %s, num_of_student: %s, num_of_teacher: %s, school_name: %s, address1: %s, school_type: %s, low_grade: %s, high_grade: %s]" % (self.dist_name, self.num_of_student, self.num_of_teacher, self.school_name, self.address1, self.school_type, self.low_grade, self.high_grade))


class Student:
    '''
    Student object
    '''
    # total_id = 0
    def __init__(self, school_name):
        '''
        Constructor
        '''
        # self.dist_id   = District.total_id
        # District.total_id = District.total_id + 1
        self.school_name = school_name
        self.last_name = generate_ramdom_name()
        self.first_name = generate_ramdom_name()

    def __str__(self):
        '''
        String method
        '''
        return ("School:[school_name: %s, last_name: %s, first_name: %s]" % (self.school_name, self.last_name, self.first_name))


class Class:
    '''
    Student object
    '''
    # total_id = 0
    def __init__(self, title, sub_name, section_stu_map, section_tea_map):
        '''
        Constructor
        '''
        # self.dist_id   = District.total_id
        # District.total_id = District.total_id + 1
        self.title = title
        self.sub_name = sub_name
        self.section_stu_map = section_stu_map
        self.section_tea_map = section_tea_map

    def __str__(self):
        '''
        String method
        '''
        return ("Class:[title: %s, sub_name: %s, section_stu_map: %s, section_tea_map: %s]" % (self.title, self.sub_name, self.section_stu_map, self.section_tea_map))

class Assessment:
    '''
    Assessment Object
    '''
    def __init__(self, id, subject, type, period, version, grade):
        '''
        Constructor
        '''
        self.id = id
        self.subject = subject
        self.type = type
        self.period = period
        self.version = version
        self.grade = grade

    def __str__(self):
        '''
        toString Method
        '''

        return ("Assessment:[id: %s, subject: %s, type: %s, period: %s, version: %s, grade: %s]" % (self.id, self.subject, self.type, self.period, self.version, self.grade))

def generate_ramdom_name():
    # temporary
    char_set = string.ascii_uppercase + string.digits
    return(''.join(random.sample(char_set, 10)))
