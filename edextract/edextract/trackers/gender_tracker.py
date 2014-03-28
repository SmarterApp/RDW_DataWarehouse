from edextract.student_reg_extract_processors.attribute_constants import AttributeFieldConstants, AttributeValueConstants

__author__ = 'ablum'

"""
This module contains the definition of the MaleTracker and FemaleTracker classes,
which tracks visitor totals.
"""

from edextract.trackers.category_tracker import CategoryTracker
from edextract.student_reg_extract_processors.category_constants import CategoryNameConstants, CategoryValueConstants


class MaleTracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.GENDER, CategoryValueConstants.MALE)

    def should_increment(self, row):

        return row[AttributeFieldConstants.GENDER] == AttributeValueConstants.MALE


class FemaleTracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.GENDER, CategoryValueConstants.FEMALE)

    def should_increment(self, row):

        return row[AttributeFieldConstants.GENDER] == AttributeValueConstants.FEMALE
