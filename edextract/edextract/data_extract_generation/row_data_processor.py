__author__ = 'tshewchuk'

"""
This module contain functions to process iterator row data using data processors and trackers.
"""

from edextract.student_reg_extract_processors.state_data_processor import StateDataProcessor
from edextract.student_reg_extract_processors.district_data_processor import DistrictDataProcessor
from edextract.student_reg_extract_processors.school_data_processor import SchoolDataProcessor


def process_row_data(rows, hierarchy_map, trackers):
    """
    Iterate through the database results, creating the student registration statistics report data.

    @param: db_rows: Iterable containing all pertinent database rows
    @param hierarchy_map: Hierarchical map of basic report format
    @param trackers: List of trackers containing needed data to fill the report

    @return: List of rows to be included in the CSV report.
    """

    data_processors = [StateDataProcessor(trackers, hierarchy_map), DistrictDataProcessor(trackers, hierarchy_map),
                       SchoolDataProcessor(trackers, hierarchy_map)]

    for row in rows:
        for processor in data_processors:
            processor.process_data(row)
