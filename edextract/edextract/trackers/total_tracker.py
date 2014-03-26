__author__ = 'tshewchuk'

"""
This module contains the definition of the TotalTracker class, which tracks visitor totals.
"""

from edextract.trackers.category_tracker import CategoryTracker


class TotalTracker(CategoryTracker):

    def __init__(self):
        super().__init__()
        self._category = 'Total'
        self._value = 'Total'

    def get_category_and_value(self):
        """
        Returns category and value names for this class.

        @return: Category and value for this class
        """

        return self._category, self._value
