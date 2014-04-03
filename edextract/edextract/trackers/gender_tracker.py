__author__ = 'ablum'

"""
This module contains the definition of the MaleTracker and FemaleTracker classes,
which tracks visitor totals.
"""

from edextract.trackers.category_tracker import CategoryTracker
from edextract.student_reg_extract_processors.category_constants import CategoryNameConstants, CategoryValueConstants
from edextract.student_reg_extract_processors.attribute_constants import AttributeFieldConstants, AttributeValueConstants


class MaleTracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.GENDER, CategoryValueConstants.MALE, AttributeFieldConstants.GENDER)

    def _should_increment(self, row):
        return row[AttributeFieldConstants.GENDER] == AttributeValueConstants.MALE


class FemaleTracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.GENDER, CategoryValueConstants.FEMALE, AttributeFieldConstants.GENDER)

    def _should_increment(self, row):
        return row[AttributeFieldConstants.GENDER] == AttributeValueConstants.FEMALE
