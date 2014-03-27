__author__ = 'tshewchuk'

"""
This module contain functions to process iterator row data using data processors and trackers.
"""


def process_row_data(rows, data_processors):
    """
    Iterate through the database results, creating the student registration statistics report data.

    @param: db_rows: Iterable containing all pertinent database rows
    @param hierarchy_map: Hierarchical map of basic report format
    @param trackers: List of trackers containing needed data to fill the report

    @return: List of rows to be included in the CSV report.
    """

    for row in rows:
        for processor in data_processors:
            processor.process_data(row)
