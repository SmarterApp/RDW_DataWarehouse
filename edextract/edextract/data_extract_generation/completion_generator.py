__author__ = 'tshewchuk'

"""
This module contains functions to generate data rows for the Student Registration Completion Report.
"""

from edextract.data_extract_generation.data_generator_helper import format_intval, get_row_identifiers


def get_tracker_results(report_map, trackers, current_year):
    """
    Use the report map to transform the tracker data into the Student Registration Completion Report data format.

    @param report_map: Hierarchical map of basic report format
    @param trackers: List of trackers containing needed data to fill the report
    @param: current_year: Current academic year of the Student Registration Completion Report

    @return: Report data, as a generator
    """

    for key, val in report_map.items():

        for tracker in trackers:
            state_name, district_name, school_name, category, value = get_row_identifiers(key, tracker)

            entry_data = tracker.get_map_entry(val)
            current_year_count = entry_data.get(current_year, 0) if entry_data else 0

            row = [state_name, district_name, school_name, category, value] + _generate_data_row(current_year_count)

            yield row


def _generate_data_row(registered_count):
    '''
    Generates a data row with completion data.

    @param registered_count: The count of registered students of a certain demographic for the current year

    @return: A data row including all completion data
    '''

    return [format_intval(registered_count)]
