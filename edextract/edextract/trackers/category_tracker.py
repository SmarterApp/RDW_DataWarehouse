__author__ = 'tshewchuk'

"""
This module contains the definition of the CategoryTracker class, the base class for all category tracker classes.
"""

from abc import ABCMeta, abstractmethod


class CategoryTracker(metaclass=ABCMeta):

    def __init__(self, category, value):
        self._map = {}
        self._category = category
        self._value = value

    def track(self, guid, row):
        """
        Increment total of rows based on the year this row contains for the given guid.

        @param guid: GUID of edorg for which to increment the total for the row's year.
        @param row: Current DB table row to be counted
        """

        if self.should_increment(row):
            year = row['academic_year']
            if guid in self._map.keys():
                if year in self._map[guid]:
                    self._map[guid][year] += 1
                else:
                    self._map[guid][year] = 1
            else:
                self._map[guid] = {year: 1}

    def get_map_entry(self, guid):
        """
        Return the guid entry of the map containing all of the edorg totals by year.
        Map entries are of the format:
            {edOrgGuid: {previousAcademicYear: totalRowsForYear, currentAcademicYear: totalRowsForYear}}


        @param guid: GUID identifying the EdOrg for which to return totals by year

        @return: Map entry containing the totals by year for the edorg specified by the guid
        """

        return self._map.get(guid, None)

    def get_category_and_value(self):
        """
        Returns category and value names for this class.

        @return: Category and value for this class
        """

        return self._category, self._value

    @abstractmethod
    def should_increment(self, row):
        """
        Determine if internal totals map should be updated for a row.

        @param row: Current row to be assessed

        @return: Whether or not to increment the concrete class's totals map
        @returntype: Boolean
        """
        return
