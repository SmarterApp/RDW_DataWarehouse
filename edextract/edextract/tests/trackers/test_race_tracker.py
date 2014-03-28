__author__ = 'npandey'

import unittest
from edextract.student_reg_extract_processors.attribute_constants import AttributeFieldConstants, AttributeValueConstants
from edextract.trackers.race_tracker import HispanicLatino, AmericanIndian, Asian, AfricanAmerican, PacificIslander, \
    White, MultiRace


class TestRaceTracker(unittest.TestCase):
    def setUp(self):
        self.hispanic_tracker = HispanicLatino()
        self.ami_tracker = AmericanIndian()
        self.asn_tracker = Asian()
        self.afm_tracker = AfricanAmerican()
        self.pac_tracker = PacificIslander()
        self.wht_tracker = White()
        self.mul_tracker = MultiRace()

        self.race_trackers = [self.hispanic_tracker, self.ami_tracker, self.asn_tracker, self.afm_tracker, self.pac_tracker,
                              self.wht_tracker, self.mul_tracker]

        self.hsp_db_rows = [
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school1', 'academic_year': 2013,
             AttributeFieldConstants.HISPANIC_ETH: True},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school1', 'academic_year': 2014,
             AttributeFieldConstants.HISPANIC_ETH: True},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school2', 'academic_year': 2013,
             AttributeFieldConstants.HISPANIC_ETH: False},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school2', 'academic_year': 2014,
             AttributeFieldConstants.HISPANIC_ETH: True},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school1', 'academic_year': 2013,
             AttributeFieldConstants.HISPANIC_ETH: False},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school1', 'academic_year': 2014,
             AttributeFieldConstants.HISPANIC_ETH: False},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school2', 'academic_year': 2013,
             AttributeFieldConstants.HISPANIC_ETH: False},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school2', 'academic_year': 2014,
             AttributeFieldConstants.HISPANIC_ETH: True}
        ]

        self.race_db_rows = [
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school1', 'academic_year': 2013,
             AttributeFieldConstants.HISPANIC_ETH: True,
             AttributeFieldConstants.AMERICAN_INDIAN: True,
             AttributeFieldConstants.ASIAN: True,
             AttributeFieldConstants.AFRICAN_AMERICAN: True,
             AttributeFieldConstants.PACIFIC: True,
             AttributeFieldConstants.WHITE: True,
             AttributeFieldConstants.MULTI_RACE: True},
            {'state_code': 'NJ', 'district_guid': 'district1', 'school_guid': 'school1', 'academic_year': 2014,
             AttributeFieldConstants.HISPANIC_ETH: False,
             AttributeFieldConstants.AMERICAN_INDIAN: True,
             AttributeFieldConstants.ASIAN: False,
             AttributeFieldConstants.AFRICAN_AMERICAN: True,
             AttributeFieldConstants.PACIFIC: True,
             AttributeFieldConstants.WHITE: False,
             AttributeFieldConstants.MULTI_RACE: False}
        ]

    def test_validate_category_names(self):
        category, value = self.hispanic_tracker.get_category_and_value()
        self.assertEquals('Ethnicity', category)
        self.assertEquals('HispanicOrLatinoEthnicity', value)

        category, value = self.ami_tracker.get_category_and_value()
        self.assertEquals('Race', category)
        self.assertEquals('AmericanIndianOrAlaskaNative', value)

        category, value = self.asn_tracker.get_category_and_value()
        self.assertEquals('Race', category)
        self.assertEquals('Asian', value)

        category, value = self.afm_tracker.get_category_and_value()
        self.assertEquals('Race', category)
        self.assertEquals('BlackOrAfricanAmerican', value)

        category, value = self.pac_tracker.get_category_and_value()
        self.assertEquals('Race', category)
        self.assertEquals('NativeHawaiianOrOtherPacificIslander', value)

        category, value = self.wht_tracker.get_category_and_value()
        self.assertEquals('Race', category)
        self.assertEquals('White', value)

        category, value = self.mul_tracker.get_category_and_value()
        self.assertEquals('Race', category)
        self.assertEquals('DemographicRaceTwoOrMoreRaces', value)

    def test_hisp_eth_count(self):
        for row in self.hsp_db_rows:
            self.hispanic_tracker.track(row['state_code'], row)
            self.hispanic_tracker.track(row['district_guid'], row)
            self.hispanic_tracker.track(row['school_guid'], row)

        self.assertEquals(2, len(self.hispanic_tracker.get_map_entry('NJ')))
        self.assertEquals(2, len(self.hispanic_tracker.get_map_entry('district1')))
        self.assertEquals(2, len(self.hispanic_tracker.get_map_entry('school1')))
        self.assertEquals(1, len(self.hispanic_tracker.get_map_entry('school2')))

        self.assertEquals(1, self.hispanic_tracker.get_map_entry('NJ')[2013])
        self.assertEquals(3, self.hispanic_tracker.get_map_entry('NJ')[2014])

        self.assertEquals(1, self.hispanic_tracker.get_map_entry('district1')[2013])
        self.assertEquals(3, self.hispanic_tracker.get_map_entry('district1')[2014])

        self.assertEquals(1, self.hispanic_tracker.get_map_entry('school1')[2013])
        self.assertEquals(1, self.hispanic_tracker.get_map_entry('school1')[2014])

        self.assertEquals(2, self.hispanic_tracker.get_map_entry('school2')[2014])

    def test_race_trackers(self):
        for tracker in self.race_trackers:
            for row in self.race_db_rows:
                tracker.track(row['state_code'], row)
                tracker.track(row['district_guid'], row)
                tracker.track(row['school_guid'], row)

        self.validate_two_years_data([self.ami_tracker, self.afm_tracker, self.pac_tracker])
        self.validate_single_year_data([self.hispanic_tracker, self.asn_tracker, self.wht_tracker, self.mul_tracker])

    def validate_two_years_data(self, trackers):
        for tracker in trackers:
            self.assertEquals(2, len(tracker.get_map_entry('NJ')))
            self.assertEquals(2, len(tracker.get_map_entry('district1')))
            self.assertEquals(2, len(tracker.get_map_entry('school1')))

            self.assertEquals(1, tracker.get_map_entry('NJ')[2013])
            self.assertEquals(1, tracker.get_map_entry('NJ')[2014])

    def validate_single_year_data(self, trackers):
        for tracker in trackers:
            self.assertEquals(1, len(tracker.get_map_entry('NJ')))
            self.assertEquals(1, len(tracker.get_map_entry('district1')))
            self.assertEquals(1, len(tracker.get_map_entry('school1')))

            self.assertEquals(1, tracker.get_map_entry('NJ')[2013])
