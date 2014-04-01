__author__ = 'npandey'

"""
Track the counts for grade category
"""

from edextract.student_reg_extract_processors.attribute_constants import AttributeFieldConstants, AttributeValueConstants
from edextract.student_reg_extract_processors.category_constants import CategoryNameConstants, CategoryValueConstants
from edextract.trackers.category_tracker import CategoryTracker


class GradeKTracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.GRADEK, CategoryValueConstants.TOTAL)

    def should_increment_year(self, row):
        return row[AttributeFieldConstants.GRADE].upper() == AttributeValueConstants.GRADEK

    def should_increment_matched_ids(self, row):
        return


class Grade1Tracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.GRADE1, CategoryValueConstants.TOTAL)

    def should_increment_year(self, row):
        return row[AttributeFieldConstants.GRADE] == AttributeValueConstants.GRADE1

    def should_increment_matched_ids(self, row):
        return


class Grade2Tracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.GRADE2, CategoryValueConstants.TOTAL)

    def should_increment_year(self, row):
        return row[AttributeFieldConstants.GRADE] == AttributeValueConstants.GRADE2

    def should_increment_matched_ids(self, row):
        return


class Grade3Tracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.GRADE3, CategoryValueConstants.TOTAL)

    def should_increment_year(self, row):
        return row[AttributeFieldConstants.GRADE] == AttributeValueConstants.GRADE3

    def should_increment_matched_ids(self, row):
        return


class Grade4Tracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.GRADE4, CategoryValueConstants.TOTAL)

    def should_increment_year(self, row):
        return row[AttributeFieldConstants.GRADE] == AttributeValueConstants.GRADE4

    def should_increment_matched_ids(self, row):
        return


class Grade5Tracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.GRADE5, CategoryValueConstants.TOTAL)

    def should_increment_year(self, row):
        return row[AttributeFieldConstants.GRADE] == AttributeValueConstants.GRADE5

    def should_increment_matched_ids(self, row):
        return


class Grade6Tracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.GRADE6, CategoryValueConstants.TOTAL)

    def should_increment_year(self, row):
        return row[AttributeFieldConstants.GRADE] == AttributeValueConstants.GRADE6

    def should_increment_matched_ids(self, row):
        return


class Grade7Tracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.GRADE7, CategoryValueConstants.TOTAL)

    def should_increment_year(self, row):
        return row[AttributeFieldConstants.GRADE] == AttributeValueConstants.GRADE7

    def should_increment_matched_ids(self, row):
        return


class Grade8Tracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.GRADE8, CategoryValueConstants.TOTAL)

    def should_increment_year(self, row):
        return row[AttributeFieldConstants.GRADE] == AttributeValueConstants.GRADE8

    def should_increment_matched_ids(self, row):
        return


class Grade9Tracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.GRADE9, CategoryValueConstants.TOTAL)

    def should_increment_year(self, row):
        return row[AttributeFieldConstants.GRADE] == AttributeValueConstants.GRADE9

    def should_increment_matched_ids(self, row):
        return


class Grade10Tracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.GRADE10, CategoryValueConstants.TOTAL)

    def should_increment_year(self, row):
        return row[AttributeFieldConstants.GRADE] == AttributeValueConstants.GRADE10

    def should_increment_matched_ids(self, row):
        return


class Grade11Tracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.GRADE11, CategoryValueConstants.TOTAL)

    def should_increment_year(self, row):
        return row[AttributeFieldConstants.GRADE] == AttributeValueConstants.GRADE11

    def should_increment_matched_ids(self, row):
        return


class Grade12Tracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.GRADE12, CategoryValueConstants.TOTAL)

    def should_increment_year(self, row):
        return row[AttributeFieldConstants.GRADE] == AttributeValueConstants.GRADE12

    def should_increment_matched_ids(self, row):
        return
