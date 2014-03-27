import unittest
from edextract.student_reg_extract_processors.attribute_constants import AttributeFieldConstants, AttributeValueConstants
from edextract.trackers.gender_tracker import MaleTracker, FemaleTracker

__author__ = 'ablum'


class TestGenderTracker(unittest.TestCase):

    def setUp(self):
        self.male_tracker = MaleTracker()
        self.female_tracker = FemaleTracker()
        self.db_rows = [
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school1', 'academic_year': 2013, AttributeFieldConstants.GENDER: AttributeValueConstants.MALE},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school1', 'academic_year': 2014, AttributeFieldConstants.GENDER: AttributeValueConstants.MALE},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school2', 'academic_year': 2013, AttributeFieldConstants.GENDER: AttributeValueConstants.MALE},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school2', 'academic_year': 2014, AttributeFieldConstants.GENDER: AttributeValueConstants.MALE},
            {'state_code': 'NJ', 'district_guid': 'male_only_dis', 'school_guid': 'male_only_school', 'academic_year': 2014, AttributeFieldConstants.GENDER: AttributeValueConstants.MALE},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school1', 'academic_year': 2013, AttributeFieldConstants.GENDER: AttributeValueConstants.FEMALE},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school1', 'academic_year': 2014, AttributeFieldConstants.GENDER: AttributeValueConstants.FEMALE},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school2', 'academic_year': 2013, AttributeFieldConstants.GENDER: AttributeValueConstants.FEMALE},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school2', 'academic_year': 2014, AttributeFieldConstants.GENDER: AttributeValueConstants.FEMALE},
            {'state_code': 'NJ', 'district_guid': 'female_only_dis', 'school_guid': 'female_only_school', 'academic_year': 2014, AttributeFieldConstants.GENDER: AttributeValueConstants.FEMALE},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'BAD_VALUE_SCHOOL', 'academic_year': 2014, AttributeFieldConstants.GENDER: 'BAD_VALUE'},
        ]

    def track_rows(self, track_function, rows):
        for row in rows:
            state_guid = row['state_code']
            district_guid = row['district_guid']
            school_guid = row['school_guid']
            track_function(state_guid, row)
            track_function(district_guid, row)
            track_function(school_guid, row)

    def test_male_tracker(self):
        self.track_rows(self.male_tracker.track, self.db_rows)

        #State Totals
        self.assertEquals(2, len(self.male_tracker.get_map_entry('NJ')))
        self.assertEquals(2, self.male_tracker.get_map_entry('NJ')[2013])
        self.assertEquals(3, self.male_tracker.get_map_entry('NJ')[2014])

        #District Totals
        self.assertEquals(2, len(self.male_tracker.get_map_entry('district1')))
        self.assertEquals(2, self.male_tracker.get_map_entry('district1')[2013])
        self.assertEquals(2, self.male_tracker.get_map_entry('district1')[2014])

        self.assertEquals(1, len(self.male_tracker.get_map_entry('male_only_dis')))
        self.assertEquals(1, self.male_tracker.get_map_entry('male_only_dis')[2014])

        #School Totals
        self.assertEquals(2, len(self.male_tracker.get_map_entry('school1')))
        self.assertEquals(1, self.male_tracker.get_map_entry('school1')[2013])
        self.assertEquals(1, self.male_tracker.get_map_entry('school1')[2014])

        self.assertEquals(2, len(self.male_tracker.get_map_entry('school2')))
        self.assertEquals(1, self.male_tracker.get_map_entry('school2')[2013])
        self.assertEquals(1, self.male_tracker.get_map_entry('school2')[2014])

        self.assertEquals(1, len(self.male_tracker.get_map_entry('male_only_school')))
        self.assertEquals(1, self.male_tracker.get_map_entry('male_only_school')[2014])

        self.assertEquals(None, self.male_tracker.get_map_entry('female_only_school'))
        self.assertEquals(None, self.male_tracker.get_map_entry('female_only_district'))
        self.assertEquals(None, self.male_tracker.get_map_entry('BAD_VALUE_SCHOOL'))

    def test_female_tracker(self):
        self.track_rows(self.female_tracker.track, self.db_rows)

        #State Totals
        self.assertEquals(2, len(self.female_tracker.get_map_entry('NJ')))
        self.assertEquals(2, self.female_tracker.get_map_entry('NJ')[2013])
        self.assertEquals(3, self.female_tracker.get_map_entry('NJ')[2014])

        #District Totals
        self.assertEquals(2, len(self.female_tracker.get_map_entry('district1')))
        self.assertEquals(2, self.female_tracker.get_map_entry('district1')[2013])
        self.assertEquals(2, self.female_tracker.get_map_entry('district1')[2014])

        self.assertEquals(1, len(self.female_tracker.get_map_entry('female_only_dis')))
        self.assertEquals(1, self.female_tracker.get_map_entry('female_only_dis')[2014])

        #School Totals
        self.assertEquals(2, len(self.female_tracker.get_map_entry('school1')))
        self.assertEquals(1, self.female_tracker.get_map_entry('school1')[2013])
        self.assertEquals(1, self.female_tracker.get_map_entry('school1')[2014])

        self.assertEquals(2, len(self.female_tracker.get_map_entry('school2')))
        self.assertEquals(1, self.female_tracker.get_map_entry('school2')[2013])
        self.assertEquals(1, self.female_tracker.get_map_entry('school2')[2014])

        self.assertEquals(1, len(self.female_tracker.get_map_entry('female_only_school')))
        self.assertEquals(1, self.female_tracker.get_map_entry('female_only_school')[2014])

        self.assertEquals(None, self.male_tracker.get_map_entry('male_only_school'))
        self.assertEquals(None, self.male_tracker.get_map_entry('male_only_district'))
        self.assertEquals(None, self.male_tracker.get_map_entry('BAD_VALUE_SCHOOL'))
