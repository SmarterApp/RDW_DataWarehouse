__author__ = 'tshewchuk'

"""
This module contains the definition of the CategoryTracker class, the base class for all category tracker classes.
"""

from abc import ABCMeta, abstractmethod


class CategoryTracker(metaclass=ABCMeta):

    def __init__(self, category, value):
        self._data_counter = DataCounter()
        self._category = category
        self._value = value

    def track(self, guid, row, key=None):
        """
        Increment total of rows based on the year this row contains for the given guid.

        @param guid: GUID of edorg for which to increment the total for the row's year.
        @param row: Current DB table row to be counted

        """
        key = key if key else row['academic_year']
        should_increment = self.should_increment_matched_ids(row) if key == DataCounter.MATCHED_KEY else self.should_increment_year(row)
        if should_increment:
            self._data_counter.increment(guid, key)

    def get_map_entry(self, guid):
        """
        Return the guid entry of the map containing all of the edorg totals by year.
        Map entries are of the format:
            {edOrgGuid: {previousAcademicYear: totalRowsForYear, currentAcademicYear: totalRowsForYear}}


        @param guid: GUID identifying the EdOrg for which to return totals by year

        @return: Map entry containing the totals by year for the edorg specified by the guid
        """

        return self._data_counter.map.get(guid, None)

    def get_category_and_value(self):
        """
        Returns category and value names for this class.

        @return: Category and value for this class
        """

        return self._category, self._value

    @abstractmethod
    def should_increment_year(self, row):
        """
        Determine if internal totals map should be updated for a row.

        @param row: Current row to be assessed

        @return: Whether or not to increment the concrete class's totals map
        """
        return

    @abstractmethod
    def should_increment_matched_ids(self, row):
        """
        Determine if internal totals map should be updated for a row.

        @param row: Current row to be assessed

        @return: Whether or not to increment the concrete class's totals map
        """
        return


class DataCounter():
    MATCHED_KEY = 'MATCHED'

    def __init__(self):
        self.map = {}

    def increment(self, guid, key):
        if guid in self.map.keys():
            if key in self.map[guid]:
                self.map[guid][key] += 1
            else:
                self.map[guid][key] = 1
        else:
            self.map[guid] = {key: 1}
