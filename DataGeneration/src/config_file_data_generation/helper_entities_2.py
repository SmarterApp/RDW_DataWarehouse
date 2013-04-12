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