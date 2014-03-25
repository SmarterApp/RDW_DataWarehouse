__author__ = 'tshewchuk'

"""
This module contains the definition of the TotalTracker class, which tracks visitor totals.
"""


class TotalTracker():

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

    def get_map(self):
        """
        Return the map containing all of the edorg totals by year.
        Map entries are of the format:
            {edOrgGuid: {previousAcademicYear: totalRowsForYear, currentAcademicYear: totalRowsForYear}}

        @return: Map containing all of the edorg totals by year
        """

        return self._map
