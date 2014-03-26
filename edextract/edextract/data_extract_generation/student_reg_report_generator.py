__author__ = 'tshewchuk'

"""
This module contains methods to obtain data for the different Student Registration report types.
"""

from collections import OrderedDict

from edextract.status.constants import Constants
from edextract.tasks.constants import Constants as TaskConstants
from edextract.utils.csv_writer import write_csv
from edextract.status.status import ExtractStatus, insert_extract_stats
from edextract.student_reg_extract_processors.state_data_processor import StateDataProcessor
from edextract.student_reg_extract_processors.district_data_processor import DistrictDataProcessor
from edextract.student_reg_extract_processors.school_data_processor import SchoolDataProcessor
from edextract.trackers.total_tracker import TotalTracker
from edextract.data_extract_generation.statistics_data_generator import generate_data_row
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

    data = data_extract_func(tenant, academic_year, query)
    write_csv(output_file, headers, data)

    insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.EXTRACTED})


def _generate_statistics_report_data(tenant, academic_year, query):
    """
    Get all the tenant's student registration data for the academic year.

    @param tenant: Requestor's tenant ID
    @param academic_year: Academic year of report
    @param query: DB query to extract rows

    @return: List of rows to be included in the CSV report.
    """

    with EdCoreDBConnection(tenant=tenant) as connection:
        results = connection.get_streaming_result(query)  # This result is a generator

        data = _get_sr_stat_tenant_data_for_academic_year(results, academic_year)

    return data


def _generate_completion_report_data(tenant, academic_year, query):
    """
    This method generates the data for the student registration completion report.

    @param tenant: Requestor's tenant ID
    @param academic_year: Academic year of report
    @param query: DB query to extract rows

    @return: Report data
    """

    return []


def _get_sr_stat_tenant_data_for_academic_year(db_rows, academic_year):
    """
    Get all the tenant's student registration data for the academic year.

    @param: db_rows: Iterable containing all pertinent database rows
    @param academic_year: Academic year of report

    @return: List of rows to be included in the CSV report.
    """

    hierarchy_map = {}
    total_tracker = TotalTracker()
    trackers = [total_tracker]

    _process_db_data_for_sr_stat(db_rows, hierarchy_map, trackers)

    report_map = OrderedDict(sorted(hierarchy_map.items()))

    return _get_tracker_results_for_sr_stat(report_map, total_tracker, trackers, academic_year)


def _process_db_data_for_sr_stat(db_rows, hierarchy_map, trackers):
    """
    Iterate through the database results, creating the student registration statistics report data.

    @param: db_rows: Iterable containing all pertinent database rows
    @param hierarchy_map: Hierarchical map of basic report format
    @param trackers: List of trackers containing needed data to fill the report

    @return: List of rows to be included in the CSV report.
    """

    data_processors = [StateDataProcessor(trackers, hierarchy_map), DistrictDataProcessor(trackers, hierarchy_map),
                       SchoolDataProcessor(trackers, hierarchy_map)]

    for db_row in db_rows:
        for processor in data_processors:
            processor.process_data(db_row)


def _get_tracker_results_for_sr_stat(report_map, total_tracker, trackers, academic_year):
    """
    Use the report map to transform the tracker data into the report data format.

    @param report_map: Hierarchical map of basic report format
    @param total_tracker: Totals tracker, from which to obtain the EdOrg totals, for percentage calculations
    @param trackers: List of trackers containing needed data to fill the report
    @param: academic_year: Academic year of the report

    @return: Report data, as a list of lists
    """

    # First, get all the edorg totals.
    previous_year = academic_year - 1
    edorg_totals = {}
    for _, val in report_map.items():
        edorg_totals[val] = {previous_year: total_tracker.get_map_entry(val).get(previous_year, 0),
                             academic_year: total_tracker.get_map_entry(val).get(academic_year, 0)}

    data = []
    for key, val in report_map.items():
        for tracker in trackers:
            state_name = key.state_name
            district_name = key.district_name if key.district_name else 'ALL'
            school_name = key.school_name if key.school_name else 'ALL'
            category, value = tracker.get_category_and_value()
            row = [state_name, district_name, school_name, category, value]

            entry_data = tracker.get_map_entry(val)
            if entry_data:
                row += generate_data_row(entry_data.get(academic_year, 0), entry_data.get(previous_year, 0),
                                         edorg_totals[val].get(academic_year, 0), edorg_totals[val].get(previous_year, 0))
                data.append(row)

    return data
