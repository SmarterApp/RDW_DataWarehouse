__author__ = 'tshewchuk'

"""
This module defines the various program tracker classes, which track the totals for their respective program types.
"""

from edextract.trackers.category_tracker import CategoryTracker
from edextract.student_reg_extract_processors.category_constants import CategoryNameConstants, CategoryValueConstants
from edextract.student_reg_extract_processors.attribute_constants import AttributeFieldConstants


class IDEAIndicatorTracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.PROGRAM, CategoryValueConstants.IDEA_INDICATOR,
                         AttributeFieldConstants.IDEA_INDICATOR)

    def _should_increment_year(self, row):
        return bool(row[AttributeFieldConstants.IDEA_INDICATOR])


class LEPStatusTracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.PROGRAM, CategoryValueConstants.LEP_STATUS, AttributeFieldConstants.LEP_STATUS)

    def _should_increment_year(self, row):
        return bool(row[AttributeFieldConstants.LEP_STATUS])


class Sec504StatusTracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.PROGRAM, CategoryValueConstants.SECTION_504_STATUS,
                         AttributeFieldConstants.SECTION_504_STATUS)

    def _should_increment_year(self, row):
        return bool(row[AttributeFieldConstants.SECTION_504_STATUS])


class EconDisadvStatusTracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.PROGRAM, CategoryValueConstants.ECON_DISADV_STATUS,
                         AttributeFieldConstants.ECON_DISADV_STATUS)

    def _should_increment_year(self, row):
        return bool(row[AttributeFieldConstants.ECON_DISADV_STATUS])


class MigrantStatusTracker(CategoryTracker):

    def __init__(self):
        super().__init__(CategoryNameConstants.PROGRAM, CategoryValueConstants.MIGRANT_STATUS,
                         AttributeFieldConstants.MIGRANT_STATUS)

    def _should_increment_year(self, row):
        return bool(row[AttributeFieldConstants.MIGRANT_STATUS])
