__author__ = 'tshewchuk'

"""
This module contains the definition of the CategoryTracker class, the base class for all category tracker classes.
"""

from abc import ABCMeta, abstractmethod


class CategoryTracker(metaclass=ABCMeta):

    def __init__(self):
        self._map = {}

    def track(self, guid, row):
        """
        Increment total of rows based on the year this row contains for the given guid.

        @param guid: GUID of edorg for which to increment the total for the row's year.
        @param row: Current DB table row to be counted
        """

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

    @abstractmethod
    def get_category_and_value(self):
        """
        Abstract method returns category and value names for this class.
        """

        return
