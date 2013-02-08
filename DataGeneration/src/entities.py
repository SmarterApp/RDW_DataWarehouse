import random
import string
from idgen import IdGen


class State:
    '''
    state object
    '''

    def __init__(self, state_id, state_name, num_of_dist, state_code=None):
        '''
        Constructor
        '''
        self.state_id = state_id
        self.state_name = state_name
        self.num_of_dist = num_of_dist
        self.state_code = state_code

    def __str__(self):
        '''
        String method
        '''
        return ("State:[state_id: %s, state_name:%s, num_of_dist: %s]" % (self.state_id, self.state_name, self.num_of_dist))

    def getRow(self):
        return [self.state_id, self.state_name, self.state_code]


class District:
    '''
    District object
    '''
    # total_id = 0
    def __init__(self, district_id, district_external_id, district_name, state_code, num_of_schools, zipcode_range, city_names, address_1=None, zipcode=None, address_2=None):
        '''
        Constructor
        '''
        self.district_id = district_id
        self.district_external_id = district_external_id
        self.district_name = district_name
        self.address_1 = address_1
        self.address_2 = address_2
        self.zipcode = zipcode
        self.state_code = state_code

        self.num_of_schools = num_of_schools
        self.zipcode_range = zipcode_range
        self.city_names = city_names

    def __str__(self):
        '''
        String method
        '''
        return ("District:[district_id: %s, district_external_id: %s, district_name: %s]" % (self.district_id, self.district_external_id, self.district_name))

    def getRow(self):
        return [self.district_id, self.district_external_id, self.district_name, self.address_1, self.address_2, self.zipcode, self.state_code]


class School:
    '''
    School object
    '''
    # total_id = 0
    def __init__(self, sch_id, school_external_id, school_name, dist_name, state_code, num_of_student, stu_tea_ratio, low_grade, high_grade, school_categories_type=None, school_type=None, address1=None, city=None, zip_code=None, address2=None):
        '''
        Constructor
        '''
        # self.dist_id   = District.total_id
        # District.total_id = District.total_id + 1
        self.sch_id = sch_id
        self.school_external_id = school_external_id
        self.school_name = school_name
        self.dist_name = dist_name
        self.state_code = state_code
        self.num_of_student = num_of_student
        self.stu_tea_ratio = stu_tea_ratio
        self.low_grade = low_grade
        self.high_grade = high_grade
        self.school_categories_type = school_categories_type
        self.school_type = school_type
        self.address1 = address1
        self.city = city
        self.zip_code = zip_code
        self.address2 = address2

    def __str__(self):
        '''
        String method
        '''
        return ("School:[sch_id: %s, dist_id: %s, num_of_student: %s, stu_tea_ratio: %s, school_name: %s, address1: %s, school_type: %s, low_grade: %s, high_grade: %s, place_id:%s]" % (self.sch_id, self.dist_id, self.num_of_student, self.stu_tea_ratio, self.school_name, self.address1, self.school_type, self.low_grade, self.high_grade, self.place_id))

    def getRow(self):
        return [self.sch_id, self.school_external_id, self.school_name, self.dist_name, self.school_categories_type, self.school_type, self.address1, self.address2, self.city, self.zip_code, self.state_code]


class Class:
    '''
    NOT PRESENT IN NEW SCHEMA
    Class Object
    '''
    # total_id = 0
    def __init__(self, class_id, title, sub_name, section_stu_map, section_tea_map):
        '''
        Constructor
        '''
        # self.dist_id   = District.total_id
        # District.total_id = District.total_id + 1
        self.class_id = class_id
        self.title = title
        self.sub_name = sub_name
        self.section_stu_map = section_stu_map
        self.section_tea_map = section_tea_map

    def __str__(self):
        '''
        String method
        '''
        return ("Class:[class_id: %s, title: %s, sub_name: %s, section_stu_map: %s, section_tea_map: %s]" % (self.class_id, self.title, self.sub_name, self.section_stu_map, self.section_tea_map))

    def getRow(self):
        return [self.class_id, self.title]


class AssessmentType:
    '''
    AssessmentType Object
    ****Adding placeholders for fields so not to break things***
    ****Should we have an asmt_claim table?
    '''
    def __init__(self, assmt_id, subject, assmt_type, period, version, grade):
        '''
        Constructor
        '''
        self.assmt_id = assmt_id  # asmt_id in new schema. (may not wish to change)
        self.asmt_external_id = None  # NEW
        self.assmt_type = assmt_type  # asmt_type
        self.period = period  # asmt_period in new schema
        self.asmt_period_year = None  # NEW
        self.version = version  # NEW
        self.grade = grade  # asmt_grade
        self.subject = subject  # asmt_subject
        # ALL NEW BELOW
        self.asmt_claim_1_name = None
        self.asmt_claim_2_name = None
        self.asmt_claim_3_name = None
        self.asmt_claim_4_name = None
        self.asmt_perf_M_name_1 = None
        self.asmt_perf_M_name_2 = None
        self.asmt_perf_M_name_3 = None
        self.asmt_perf_M_name_4 = None
        self.asmt_score_min = None
        self.asmt_score_max = None
        self.asmt_claim_1_score_min = None
        self.asmt_claim_1_score_max = None
        self.asmt_claim_2_score_min = None
        self.asmt_claim_2_score_max = None
        self.asmt_claim_3_score_min = None
        self.asmt_claim_3_score_max = None
        self.asmt_claim_4_score_min = None
        self.asmt_claim_4_score_max = None
        self.asmt_cut_point_1 = None
        self.asmt_cut_point_2 = None
        self.asmt_cut_point_3 = None
        self.asmt_cut_point_4 = None

    def __str__(self):
        '''
        toString Method
        '''

        return ("Assessment:[assmt_type: %s, subject: %s, assmt_type: %s, period: %s, version: %s, grade: %s]" % (self.assmt_type, self.subject, self.assmt_type, self.period, self.version, self.grade))

    def getRow(self):
        return [self.assmt_id, self.subject, self.assmt_type, self.period, self.version, self.grade]


class Score:
    '''
    Score object
    '''
    def __init__(self, overall, claims):
        '''
        Constructor
        '''
        self.overall = overall
        self.claims = claims
        # self.level = level

    def __str__(self):
        '''
        String method
        '''
        return ("Score:[overall: %s, claims: %s]" % (self.overall, self.claims))


class WhereTaken:
    '''
    Where-taken object
    '''
    def __init__(self, wheretaken_id, wheretaken_name, district_name, address_1, city_name, zip_code, state_code, country_id, address_2=None):
        '''
        wheretaken_id, wheretaken_name, distr.district_name, address_1, city_name, zip_code, distr.state_code, 'US'
        Constructor
        '''
        self.wheretaken_id = wheretaken_id
        self.wheretaken_name = wheretaken_name
        self.district_name = district_name
        self.address_1 = address_1
        self.city_name = city_name
        self.zip_code = zip_code
        self.state_code = state_code
        self.country_id = country_id
        self.address_2 = address_2

    def __str__(self):
        '''
        String method
        '''
        return ("WhereTaken:[wheretaken_id: %s, wheretaken_name: %s, district_name: %s, address_1: %s, address_2: %s,city_name:%s, zip_code:%s, state_code :%s, country_id: %s]" % (self.wheretaken_id, self.wheretaken_name, self.district_name, self. address_1, self.address_2, self.city_name, self.zip_code, self.country_id))

    def getRow(self):
        return [self.wheretaken_id, self.wheretaken_name, self.district_name, self. address_1, self.address_2, self.city_name, self.zip_code, self.state_code, self.country_id]


class AssessmentOutcome(object):
    '''
    Assessment outcome object
    Should map to the fact_asmt_outcome table
    ****Adding placeholders for fields so not to break things***
    '''
    def __init__(self, asmnt_out_id, asmnt_type_id, student_id, stdnt_tmprl_id, teacher_id, date_taken, where_taken_id, score, asmt_create_date):
        self.asmnt_out_id = asmnt_out_id
        self.asmt_outcome_external_id = None  # NEW
        self.asmnt_type_id = asmnt_type_id  # asmt_id
        self.student_id = student_id
        self.teacher_id = teacher_id
        self.state_code = None  # NEW
        self.district_id = None  # NEW
        self.school_id = None  # NEW
        self.asmt_grade_id = None  # NEW
        self.asmt_grade_code = None  # NEW
        self.enrl_grade_id = None  # NEW
        self.enrl_grade_code = None  # NEW
        self.date_taken = date_taken
        self.where_taken_id = where_taken_id
        self.score = score
        self.asmt_type = None  # Should be an AssessmentType object
        self.asmt_create_date = asmt_create_date
        self.stdnt_tmprl_id = stdnt_tmprl_id  # REMOVED
        self.asmt_perf_M = None  # NEW

    def getRow(self):
        claims = list(self.score.claims.items())

        return [self.asmnt_out_id, self.asmnt_type_id, self.student_id, self.stdnt_tmprl_id, self.teacher_id, self.date_taken, self.date_taken.day, self.date_taken.month, self.date_taken.year,
                self.where_taken_id, self.score.overall, claims[0][0], claims[0][1], claims[1][0], claims[1][1], claims[2][0], claims[2][1], claims[3][0], claims[3][1], self.asmt_create_date]


class HistAssessmentOutcome(object):
    '''
    NOT PRESENT IN NEW SCHEMA
    maps to hist_asmt_outcome table
    '''
    def __init__(self, asmnt_out_id, asmnt_type_id, student_id, stdnt_tmprl_id, date_taken, where_taken_id, score, asmt_create_date, hist_create_date):
        self.asmnt_out_id = asmnt_out_id
        self.asmnt_type_id = asmnt_type_id
        self.student_id = student_id
        self.stdnt_tmprl_id = stdnt_tmprl_id
        self.date_taken = date_taken
        self.where_taken_id = where_taken_id
        self.score = score
        self.asmt_create_date = asmt_create_date
        self.hist_create_date = hist_create_date

    def getRow(self):
        claims = list(self.score.claims.items())

        return [self.asmnt_out_id, self.asmnt_type_id, self.student_id, self.stdnt_tmprl_id, self.date_taken, self.date_taken.day, self.date_taken.month, self.date_taken.year, self.where_taken_id,
                self.score.overall, claims[0][0], claims[0][1], claims[1][0], claims[1][1], claims[2][0], claims[2][1], claims[3][0], claims[3][1], self.asmt_create_date, self.hist_create_date]


class StudentTemporalData(object):
    '''
    NOT PRESENT IN NEW SCHEMA
    Object to match the student_tmprl_data table
    '''
    def __init__(self, student_tmprl_id, student_id, grade_id, dist_name, school_id, student_class, section_id):
        self.student_tmprl_id = student_tmprl_id
        self.student_id = student_id
        self.grade_id = grade_id
        self.dist_name = dist_name
        self.school_id = school_id
        self.student_class = student_class
        self.section_id = section_id
        self.effective_date = None
        self.end_date = None

    def getRow(self):
        eff_date = self.effective_date
        end_date = self.end_date

        if eff_date is None:
            eff_date = ''
        if end_date is None:
            end_date = ''

        return [self.student_tmprl_id, self.student_id, self.effective_date, self.end_date, self.grade_id, self.dist_name, self.school_id, self.student_class.class_id, self.section_id]


class Person(object):
    '''
    Base class for teacher, parent, student
    Right now, it only handles name fields
    '''

    def __init__(self, first_name, last_name, middle_name=None):
        '''
        Constructor
        if email and dob are not specified they are set to dummy values
        '''
        self.first_name= first_name
        self.middle_name = middle_name
        self.last_name = last_name


class Student(Person):
    '''
    Student Object
    Corresponds to student Table
    '''

    def __init__(self, first_name, last_name, gender=None, dob=None, email=None, address=None):

        super().__init__(firstname, last_name, middle_name)
        self.student_id = None
        self.student_external_id = None
        self.dob = dob
        self.address1 = None  # NEW
        self.address2 = None  # NEW
        self.city
        self.zip
        self.school_id = None
        self.district_id = None  # NEW
        self.state_id = None  # State Code in new

    def __str__(self):
        return ("%s %s %s" % (self.firstname, self.middlename, self.lastname))

    def getRow(self):
        return [self.student_id, self.firstname, self.middlename, self.lastname, 'address1', 'address2', 'address3', 'city',
                self.state_id, 'zip', 'country', self.gender, self.school_id, self.email, self.dob]


class Parent(Person):
    '''
    Parent Object
    Corresponds to parent table
    '''

    def __init__(self, first_name, last_name, address_1, city, state_code, zip_code, parent_id=None, parent_external_id=None, middle_name=None, address_2=None):
        super().__init__(first_name, middle_name, last_name)

        # Ids can either be given to the constructor or provided by constructor
        # Either way, both Id fields must have a value
        if parent_id == None or parent_external_id == None:
            id_generator = IdGen()
            if parent_id == None:
                self.parent_id = id_generator.get_id()
            if parent_external_id == None:
                self.parent_external_id = id_generator.get_id()

        self.address_1 = address_1
        self.address_2 = address_2
        self.city = city
        self.state_code =state_code
        self.zip_code = zip_code

    def __str__(self):
        return ("%s %s %s" % (self.firstname, self.middlename, self.lastname))

    def getRow(self):
        return [self.parent_id, self.parent_external_id, self.first_name, self.middle_name, self.last_name, self.address_1, self.address_2, self.city, self.state_code, self.zip_code]


class Teacher(Person):
    '''
    Teacher Object
    Corresponds to teacher table
    '''

    def __init__(self, firstname=None, middlename=None, lastname=None, gender=None, email=None, address=None):
        super().__init__(firstname, middlename, lastname, gender, email, address)
        self.teacher_id = None
        self.district_id = None  # NEW
        self.state_code = None  # NEW

    def __str__(self):
        return ("%s %s %s" % (self.firstname, self.middlename, self.lastname))

    def getRow(self):
        return [self.teacher_id, self.firstname, self.middlename, self.lastname]


def generate_ramdom_name():
    # temporary
    char_set = string.ascii_uppercase + string.digits
    return(''.join(random.sample(char_set, 10)))
