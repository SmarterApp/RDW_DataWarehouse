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


