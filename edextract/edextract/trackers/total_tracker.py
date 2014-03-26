__author__ = 'tshewchuk'

"""
This module contains the definition of the TotalTracker class, which tracks visitor totals.
"""

from edextract.trackers.category_tracker import CategoryTracker


class TotalTracker(CategoryTracker):

    def __init__(self):
        super().__init__('Total', 'Total')

    def should_increment(self, row):

        return True
