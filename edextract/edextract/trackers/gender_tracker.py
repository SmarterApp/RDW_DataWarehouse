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
        super().__init__(CategoryNameConstants.GENDER, CategoryValueConstants.MALE)

    def should_increment_year(self, row):

        return row[AttributeFieldConstants.GENDER] == AttributeValueConstants.MALE

    def should_increment_matched_ids(self, row):
        return


class FemaleTracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.GENDER, CategoryValueConstants.FEMALE)

    def should_increment_year(self, row):

        return row[AttributeFieldConstants.GENDER] == AttributeValueConstants.FEMALE

    def should_increment_matched_ids(self, row):
        return
