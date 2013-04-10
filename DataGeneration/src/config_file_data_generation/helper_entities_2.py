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
        self.districts = districts

    def add_districts(self, districts):
        for district in districts:
            self.add_district(district)

    def add_district(self, district):
        self.districts.append(district)


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
        self.schools = schools

    def add_schools(self, schools):
        for school in schools:
            self.add_school(school)

    def add_school(self, school):
        self.schools.append(school)

class School:
    '''
    School Object
    Intended for record keeping when creating InstitutionHierarchy objects
    '''

    def __init__(self, school_guid, school_name, school_category, sections=None):
        self.school_guid = school_guid
        self.school_name = school_name
        self.school_category = school_category
        self.sections = sections


