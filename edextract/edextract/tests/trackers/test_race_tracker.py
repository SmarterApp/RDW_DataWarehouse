__author__ = 'npandey'


import unittest
from edextract.student_reg_extract_processors.attribute_constants import AttributeFieldConstants, AttributeValueConstants
from edextract.trackers.race_tracker import HispanicLatino, AmericanIndian, Asian, AfricanAmerican, PacificIslander, \
    White, MultiRace


class TestRaceTracker(unittest.TestCase):

    def setUp(self):
        self.hispanic_tracker = HispanicLatino()
        self.african_american = AfricanAmerican()

    def test_validate_category_names(self):

        category, value = self.hispanic_tracker.get_category_and_value()
        self.assertEquals('Ethnicity', category)
        self.assertEquals('HispanicOrLatinoEthnicity', value)

        category, value = AmericanIndian().get_category_and_value()
        self.assertEquals('Race', category)
        self.assertEquals('AmericanIndianOrAlaskaNative', value)

        category, value = Asian().get_category_and_value()
        self.assertEquals('Race', category)
        self.assertEquals('Asian', value)

        category, value = AfricanAmerican().get_category_and_value()
        self.assertEquals('Race', category)
        self.assertEquals('BlackOrAfricanAmerican', value)

        category, value = PacificIslander().get_category_and_value()
        self.assertEquals('Race', category)
        self.assertEquals('NativeHawaiianOrOtherPacificIslander', value)

        category, value = White().get_category_and_value()
        self.assertEquals('Race', category)
        self.assertEquals('White', value)

        category, value = MultiRace().get_category_and_value()
        self.assertEquals('Race', category)
        self.assertEquals('DemographicRaceTwoOrMoreRaces', value)
