from edextract.student_reg_extract_processors.attribute_constants import AttributeFieldConstants, AttributeValueConstants

__author__ = 'ablum'

"""
This module contains the definition of the MaleTracker and FemaleTracker classes,
which tracks visitor totals.
"""

from edextract.trackers.category_tracker import CategoryTracker


class MaleTracker(CategoryTracker):

    def __init__(self):
        super().__init__('Sex', 'Male')

    def should_increment(self, row):

        return row[AttributeFieldConstants.GENDER] == AttributeValueConstants.MALE


class FemaleTracker(CategoryTracker):

    def __init__(self):
        super().__init__('Sex', 'Female')

    def should_increment(self, row):

        return row[AttributeFieldConstants.GENDER] == AttributeValueConstants.FEMALE
