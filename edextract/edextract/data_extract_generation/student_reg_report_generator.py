__author__ = 'tshewchuk'

"""
This module contains methods to obtain data for the different Student Registration report types.
"""

from sqlalchemy.sql.expression import select, or_

from edextract.status.constants import Constants
from edextract.tasks.constants import Constants as TaskConstants
from edextract.data_extract_generation.constants import TableName
from edextract.utils.csv_writer import write_csv
from edextract.status.status import ExtractStatus, insert_extract_stats
from edextract.student_reg_extract_processors.state_data_processor import StateDataProcessor
from edextract.student_reg_extract_processors.district_data_processor import DistrictDataProcessor
from edextract.student_reg_extract_processors.school_data_processor import SchoolDataProcessor
from edextract.trackers.total_tracker import TotalTracker
from edcore.database.edcore_connector import EdCoreDBConnection


def generate_statistics_report(tenant, output_file, task_info, extract_args):
    """
    Run generate_report with the arguments, directing it to call generate_statistics_report_data.

    @param tenant: Requestor's tenant ID
    @param output_file: File pathname of extract file
    @param task_info: Task information for recording stats
    @param extract_args: Arguments specific to generate_statistics_report_data
    """

    _generate_report(tenant, output_file, task_info, extract_args, _generate_statistics_report_data)


def generate_completion_report(tenant, output_file, task_info, extract_args):
    """
    Run generate_report with the arguments, directing it to call generate_completion_report_data.

    @param tenant: Requestor's tenant ID
    @param output_file: File pathname of extract file
    @param task_info: Task information for recording stats
    @param extract_args: Arguments specific to generate_completion_report_data
    """

    _generate_report(tenant, output_file, task_info, extract_args, _generate_completion_report_data)


def _generate_report(tenant, output_file, task_info, extract_args, data_extract_func):
    """
    Generate the student registration statistics report CSV file.

    @param tenant: Requestor's tenant ID
    @param output_file: File pathname of extract file
    @param task_info: Task information for recording stats
    @param extract_args: Arguments specific to generate_completion_report_data
    @param data_extract_func: Function to perform the specific report data extraction
    """

    academic_year = extract_args[TaskConstants.ACADEMIC_YEAR]
    query = extract_args[TaskConstants.TASK_QUERY]

    headers = extract_args[TaskConstants.CSV_HEADERS]

    data = data_extract_func(tenant, query)
    write_csv(output_file, headers, data)

    insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.EXTRACTED})


def _generate_statistics_report_data(tenant, query):
    """
    Get all the tenant's student registration data for the academic year.

    @param tenant: Requestor's tenant ID
    @param academic_year: Academic year of report

    @return:
    """

    with EdCoreDBConnection(tenant=tenant) as connection:
        results = connection.get_streaming_result(query)  # this result is a generator

    data = []

    return data


def _generate_completion_report_data(tenant, academic_year):
    """
    This method generates the data for the student registration completion report.

    @param tenant: Requestor's tenant ID
    @param academic_year: Academic year of report

    @return: Report header and data
    """

    data = []

    return data


def _get_tracker_results_for_sr_stat(db_rows):
    """
    Iterate through the database results, creating the student registration statistics report data.

    @param: db_rows: Iterable containing all pertinent database rows.

    @return: List of rows to be included in the CSV report.
    """

    hierarchy_map = {}

    trackers = [TotalTracker()]

    data_processors = [StateDataProcessor(trackers, hierarchy_map), DistrictDataProcessor(trackers, hierarchy_map),
                       SchoolDataProcessor(trackers, hierarchy_map)]

    for db_row in db_rows:
        for processor in data_processors:
            processor.process(db_row)

    report_map = sorted(hierarchy_map)

    data = []

    return data
