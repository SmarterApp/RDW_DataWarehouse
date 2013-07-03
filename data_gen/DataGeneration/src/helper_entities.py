class State:
    '''
    State object
    Intended for record keeping when creating InstitutionHierarchy objects
    '''

    def __init__(self, state_name, state_code):
        '''
        Constructor
        '''
        self.state_code = state_code
        self.state_name = state_name


class District:
    '''
    District object
    Intended for record keeping when creating InstitutionHierarchy objects
    '''

    def __init__(self, district_guid, district_name):
        '''
        Constructor
        '''
        self.district_guid = district_guid
        self.district_name = district_name


class School:
    '''
    School Object
    Intended for record keeping when creating InstitutionHierarchy objects
    '''

    def __init__(self, school_guid, school_name, school_category):
        self.school_guid = school_guid
        self.school_name = school_name
        self.school_category = school_category


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


class StudentBioInfo:

    def __init__(self, student_guid, first_name, last_name, address_1, dob, district_guid, state_code, gender, email, school_guid, zip_code, city, middle_name=None, address_2=None):

        super().__init__(first_name, last_name, middle_name=middle_name)

        # Ids can either be given to the constructor or provided by constructor
        # Either way, both Id fields must have a value
        id_generator = IdGen()
        if student_guid is None:
            self.student_guid = id_generator.get_id()
        else:
            self.student_guid = student_guid
        if student_rec_id is None:
            self.student_rec_id = id_generator.get_id()
        else:
            self.student_rec_id = student_rec_id

        self.address_1 = address_1
        self.address_2 = address_2
        self.dob = dob
        self.district_guid = district_guid
        self.city = city
        self.state_code = state_code
        self.zip_code = zip_code
        self.gender = gender
        self.email = email
        self.school_guid = school_guid
