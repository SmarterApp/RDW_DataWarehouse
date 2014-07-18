from entities import Person
from idgen import IdGen


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


class Claim:
    '''
    claim information to be used by the assessment object. Simply defines basic parameters about claim.
    '''
    def __init__(self, claim_name, claim_score_min, claim_score_max, claim_score_weight):
        self.claim_name = claim_name
        self.claim_score_min = claim_score_min
        self.claim_score_max = claim_score_max
        self.claim_score_weight = claim_score_weight


class ClaimScore():
    '''
    This is a claim object with scores. Used to create assessment_outcome row.
    '''
    def __init__(self, claim_score, claim_score_interval_minimum, claim_score_interval_maximum):
        self.claim_score = claim_score
        self.claim_score_interval_minimum = claim_score_interval_minimum
        self.claim_score_interval_maximum = claim_score_interval_maximum


class AssessmentScore:
    '''
    Assessment Score object
    '''
    def __init__(self, overall_score, perf_lvl, interval_min, interval_max, claim_scores, asmt_create_date):
        '''
        Constructor
        '''
        self.overall_score = overall_score
        self.perf_lvl = perf_lvl
        self.interval_min = interval_min
        self.interval_max = interval_max
        self.claim_scores = claim_scores
        self.asmt_create_date = asmt_create_date

    def __str__(self):
        '''
        String method
        '''
        return ("Score:[overall: %s, claims: %s]" % (self.overall_score, self.claim_scores))


# TODO: get rid of where_taken
class WhereTaken:
    '''
    Where-taken object
    '''
    def __init__(self, where_taken_id, where_taken_name, district_name=None, address_1=None, city_name=None, zip_code=None, state_code=None, country_id=None, address_2=None):
        '''
        wheretaken_id, wheretaken_name, distr.district_name, address_1, city_name, zip_code, distr.state_code, 'US'
        Constructor
        '''
        self.where_taken_id = where_taken_id
        self.where_taken_name = where_taken_name
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


class Teacher(Person):
    '''
    Teacher Object
    Corresponds to teacher table
    '''

    def __init__(self, first_name, last_name, district_id, state_code, teacher_guid=None, teacher_external_id=None, middle_name=None):
        super().__init__(first_name, last_name, middle_name=middle_name)
        # Ids can either be given to the constructor or provided by constructor
        # Either way, both Id fields must have a value

        id_generator = IdGen()

        if teacher_guid is None:
            self.teacher_guid = id_generator.get_id()
        else:
            self.teacher_guid = teacher_guid
        if teacher_external_id is None:
            self.teacher_external_id = id_generator.get_id()
        else:
            self.teacher_external_id = teacher_external_id

        self.district_id = district_id
        self.state_code = state_code

    def __str__(self):
        return ("%s %s %s" % (self.first_name, self.middle_name, self.last_name))


# TODO: Need to clarify the distinction between student and student_section
class StudentBioInfo(Person):
    '''
    Student Biographical Information Object
    Used to hold student information until it can be passed to Student Object
    '''

    def __init__(self, student_rec_id, student_id, first_name, last_name, address_1, dob, district_id, state_code, gender, email, school_id, zip_code, city, middle_name=None, address_2=None):

        super().__init__(first_name, last_name, middle_name=middle_name)

        # Ids can either be given to the constructor or provided by constructor
        # Either way, both Id fields must have a value
        id_generator = IdGen()
        if student_id is None:
            self.student_id = id_generator.get_id()
        else:
            self.student_id = student_id
        if student_rec_id is None:
            self.student_rec_id = id_generator.get_id()
        else:
            self.student_rec_id = student_rec_id

        self.address_1 = address_1
        self.address_2 = address_2
        self.dob = dob
        self.district_id = district_id
        self.city = city
        self.state_code = state_code
        self.zip_code = zip_code
        self.gender = gender
        self.email = email
        self.school_id = school_id

    def __str__(self):
        return ("%s %s %s" % (self.first_name, self.middle_name, self.last_name))
