__author__ = 'tshewchuk'

"""
This module contain functions to compile report data from trackers into a generator.
"""

from edextract.data_extract_generation.statistics_generator import generate_data_row
from itertools import chain


def get_tracker_results(report_map, total_tracker, trackers, current_year):
    """
    Use the report map to transform the tracker data into the report data format.

    @param report_map: Hierarchical map of basic report format
    @param total_tracker: Totals tracker, from which to obtain the EdOrg totals, for percentage calculations
    @param trackers: List of trackers containing needed data to fill the report
    @param: current_year: Current academic year of the report

    @return: Report data, as a list of lists
    """

    # First, get all the edorg totals.
    previous_year = current_year - 1
    data = ()
    for key, val in report_map.items():
        total_entry_data = total_tracker.get_map_entry(val)
        previous_year_total = total_entry_data.get(previous_year, None)
        current_year_total = total_entry_data.get(current_year, None)

        for tracker in trackers:
            state_name = key.state_name
            district_name = key.district_name if key.district_name else 'ALL'
            school_name = key.school_name if key.school_name else 'ALL'
            category, value = tracker.get_category_and_value()
            if total_entry_data:
                entry_data = _get_map_entry(tracker.get_map_entry(val), current_year, previous_year)

                previous_year_count = _get_year_count(entry_data.get(previous_year, 0), previous_year_total)
                current_year_count = _get_year_count(entry_data.get(current_year, 0), current_year_total)
                row = [state_name, district_name, school_name, category, value] + \
                    generate_data_row(current_year_count, previous_year_count, current_year_total, previous_year_total)
                data = chain(data, [row])

    return data


def _get_map_entry(entry_data, current_year, previous_year):
    """
    Adjust the current entry data, based on it's existence status.

    @param entry_data: Current entry data
    @param current_year: Current academic year
    @param previous_year: Previous academic year

    @return: Adjusted current entry data
    """

    if entry_data:
        return entry_data
    else:
        return {current_year: 0, previous_year: 0}


def _get_year_count(count, total):
    """
    Determine the year count, based on the year total.

    @param count: Count for some category for the year
    @param total: Total for the year

    @return: Adjusted year count for the category (int or None)
    """

    if total is None:
        return None
    else:
        return count
