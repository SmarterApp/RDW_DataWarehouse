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
