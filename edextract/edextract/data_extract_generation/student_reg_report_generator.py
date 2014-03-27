from edextract.trackers.gender_tracker import FemaleTracker, MaleTracker

__author__ = 'tshewchuk'

"""
This module contains methods to obtain data for the different Student Registration report types.
"""

from collections import OrderedDict

from edcore.database.edcore_connector import EdCoreDBConnection
from edextract.status.constants import Constants
from edextract.tasks.constants import Constants as TaskConstants
from edextract.utils.csv_writer import write_csv
from edextract.status.status import ExtractStatus, insert_extract_stats
from edextract.trackers.total_tracker import TotalTracker
from edextract.data_extract_generation.row_data_processor import process_row_data
from edextract.data_extract_generation.report_data_generator import get_tracker_results
from edextract.student_reg_extract_processors.state_data_processor import StateDataProcessor
from edextract.student_reg_extract_processors.district_data_processor import DistrictDataProcessor
from edextract.student_reg_extract_processors.school_data_processor import SchoolDataProcessor


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

    total_tracker = TotalTracker()
    trackers = [total_tracker, MaleTracker(), FemaleTracker()]

    data_processors = [StateDataProcessor(trackers), DistrictDataProcessor(trackers), SchoolDataProcessor(trackers)]

    process_row_data(db_rows, data_processors)

    report_map = OrderedDict()
    for data_processor in data_processors:
        report_map.update(sorted(data_processor.get_ed_org_hierarchy().items()))

    return get_tracker_results(report_map, total_tracker, trackers, academic_year)
