from entities import InstitutionHierarchy
from datetime import date


class State:
    '''
    state object
    '''

    def __init__(self, state_code, state_name, num_of_dist):
        '''
        Constructor
        '''
        self.state_code = state_code
        self.state_name = state_name
        self.num_of_dist = num_of_dist
        self.state_code = state_code

    def __str__(self):
        '''
        String method
        '''
        return ("State:[state_code: %s, state_name:%s, num_of_dist: %s]" % (self.state_code, self.state_name, self.num_of_dist))


class District:
    '''
    District object
    '''

    def __init__(self, district_id, district_name, state_code, state_name, number_of_schools, city_zip_map, wheretaken_list=None):
        '''
        Constructor
        '''
        self.district_id = district_id
        self.district_name = district_name
        self.state_code = state_code
        self.state_name = state_name

        self.number_of_schools = number_of_schools
        self.city_zip_map = city_zip_map
        self.wheretaken_list = wheretaken_list

    def __str__(self):
        '''
        String method
        '''
        return ("District:[district_id: %s, district_name: %s]" % (self.district_id, self.district_name))


class School:
    '''
    School object
    '''
    def __init__(self, school_id, school_name, school_category, district_name, district_id, state_code, state_name, number_of_students, student_teacher_ratio, low_grade, high_grade):
        '''
        Constructor
        '''
        self.school_id = school_id
        self.school_name = school_name
        self.school_category = school_category
        self.district_id = district_id
        self.district_name = district_name
        self.state_code = state_code
        self.state_name = state_name
        self.number_of_students = number_of_students
        self.student_teacher_ratio = student_teacher_ratio
        self.low_grade = low_grade
        self.high_grade = high_grade

    def covert_to_institution_hierarchy(self):

        institution_hierarchy_params = {
            'state_name': self.district_name,
            'state_code': self.state_code,
            'district_id': self.district_id,
            'district_name': self.district_name,
            'school_id': self.school_id,
            'school_name': self.school_name,
            'school_category': self.school_category,
            'from_date': date(2012, 9, 1),
            'to_date': date(2999, 12, 31),
            'most_recent': True
        }

        return InstitutionHierarchy(**institution_hierarchy_params)
