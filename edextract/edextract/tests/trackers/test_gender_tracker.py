import unittest
from edextract.trackers.gender_tracker import MaleTracker, FemaleTracker

__author__ = 'ablum'


class TestGenderTracker(unittest.TestCase):

    def setUp(self):
        self.male_tracker = MaleTracker()
        self.female_tracker = FemaleTracker()
        self.valid_db_rows = [
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school1', 'academic_year': 2013, 'gender': 'male'},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school1', 'academic_year': 2014, 'gender': 'male'},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school2', 'academic_year': 2013, 'gender': 'male'},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school2', 'academic_year': 2014, 'gender': 'male'},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school1', 'academic_year': 2013, 'gender': 'female'},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school1', 'academic_year': 2014, 'gender': 'female'},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school2', 'academic_year': 2013, 'gender': 'female'},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school2', 'academic_year': 2014, 'gender': 'female'},

        ]

        self.invalid_db_rows = [
            {'state_code': 'NJ', 'district_guid': 'male_only_dis', 'school_guid': 'male_only_school', 'academic_year': 2014, 'gender': 'male'},
            {'state_code': 'NJ', 'district_guid': 'female_only_dis', 'school_guid': 'female_only_school', 'academic_year': 2014, 'gender': 'female'},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'BAD_VALUE_SCHOOL', 'academic_year': 2014, 'gender': 'BAD_VALUE'},
        ]

    def track_rows(self, track_function, rows):
        for row in rows:
            state_guid = row['state_code']
            district_guid = row['district_guid']
            school_guid = row['school_guid']
            track_function(state_guid, row)
            track_function(district_guid, row)
            track_function(school_guid, row)

    def validate_state_rows(self, tracker):
        self.assertEquals(2, len(tracker.get_map_entry('NJ')))
        self.assertEquals(2, tracker.get_map_entry('NJ')[2013])
        self.assertEquals(2, tracker.get_map_entry('NJ')[2014])

    def validate_district_rows(self, tracker):
        self.assertEquals(2, len(tracker.get_map_entry('district1')))
        self.assertEquals(2, tracker.get_map_entry('district1')[2013])
        self.assertEquals(2, tracker.get_map_entry('district1')[2014])

    def validate_school_rows(self, tracker):
        self.assertEquals(2, len(tracker.get_map_entry('school1')))
        self.assertEquals(1, tracker.get_map_entry('school1')[2013])
        self.assertEquals(1, tracker.get_map_entry('school1')[2014])

        self.assertEquals(2, len(tracker.get_map_entry('school2')))
        self.assertEquals(1, tracker.get_map_entry('school2')[2013])
        self.assertEquals(1, tracker.get_map_entry('school2')[2014])

    def validate_no_rows(self, tracker, guid):
        self.assertEquals(None, tracker.get_map_entry(guid))

    def test_male_tracker(self):
        self.track_rows(self.male_tracker.track_yearly_count, self.valid_db_rows)

        self.validate_state_rows(self.male_tracker)
        self.validate_district_rows(self.male_tracker)
        self.validate_school_rows(self.male_tracker)

    def test_male_tracker_invalid_rows(self):
        self.track_rows(self.male_tracker.track_yearly_count, self.invalid_db_rows)

        self.validate_no_rows(self.male_tracker, 'female_only_school')
        self.validate_no_rows(self.male_tracker, 'female_only_district')
        self.validate_no_rows(self.male_tracker, 'BAD_VALUE_SCHOOL')

    def test_female_tracker(self):
        self.track_rows(self.female_tracker.track_yearly_count, self.valid_db_rows)

        self.validate_state_rows(self.female_tracker)
        self.validate_district_rows(self.female_tracker)
        self.validate_school_rows(self.female_tracker)

    def test_female_tracker_invalid_rows(self):
        self.track_rows(self.female_tracker.track_yearly_count, self.invalid_db_rows)

        self.validate_no_rows(self.female_tracker, 'male_only_school')
        self.validate_no_rows(self.female_tracker, 'male_only_district')
        self.validate_no_rows(self.female_tracker, 'BAD_VALUE_SCHOOL')
