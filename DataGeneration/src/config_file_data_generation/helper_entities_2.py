class State:
    '''
    State object
    Intended for record keeping when creating InstitutionHierarchy objects
    '''

    def __init__(self, state_name, state_code, districts=None):
        '''
        Constructor
        '''
        self.state_code = state_code
        self.state_name = state_name
        if districts is None:
            self.districts = []

    def add_districts(self, districts):
        for district in districts:
            self.add_district(district)

    def add_district(self, district):
        self.districts.append(district)

    def get_districts(self):
        return self.districts


class District:
    '''
    District object
    Intended for record keeping when creating InstitutionHierarchy objects
    '''

    def __init__(self, district_guid, district_name, schools=None):
        '''
        Constructor
        '''
        self.district_guid = district_guid
        self.district_name = district_name
        if schools is None:
            self.schools = []

    def add_schools(self, schools):
        for school in schools:
            self.add_school(school)

    def add_school(self, school):
        self.schools.append(school)

    def get_schools(self):
        return self.schools


class School:
    '''
    School Object
    Intended for record keeping when creating InstitutionHierarchy objects
    '''

    def __init__(self, school_guid, school_name, school_category, sections=None):
        self.school_guid = school_guid
        self.school_name = school_name
        self.school_category = school_category
        if sections is None:
            self.sections = []

    def get_sections(self):
        return self.sections


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
