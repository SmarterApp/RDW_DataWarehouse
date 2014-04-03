__author__ = 'tshewchuk'

"""
This module contains methods to obtain data for the different Student Registration report types.
"""

from collections import OrderedDict

from edcore.database.edcore_connector import EdCoreDBConnection
from edextract.status.constants import Constants
from edextract.tasks.constants import Constants as TaskConstants, QueryType
from edextract.utils.csv_writer import write_csv
from edextract.status.status import ExtractStatus, insert_extract_stats
from edextract.trackers.total_tracker import TotalTracker
from edextract.student_reg_extract_processors.row_data_processor import process_row_data
from edextract.trackers.tracker_results_helper import get_tracker_results
from edextract.student_reg_extract_processors.state_data_processor import StateDataProcessor
from edextract.student_reg_extract_processors.district_data_processor import DistrictDataProcessor
from edextract.student_reg_extract_processors.school_data_processor import SchoolDataProcessor
from edextract.trackers.gender_tracker import FemaleTracker, MaleTracker
from edextract.trackers.race_tracker import HispanicLatinoTracker, AmericanIndianTracker, AsianTracker, \
    AfricanAmericanTracker, PacificIslanderTracker, WhiteTracker, MultiRaceTracker
from edextract.trackers.program_tracker import (IDEAIndicatorTracker, LEPStatusTracker, Sec504StatusTracker,
                                                EconDisadvStatusTracker, MigrantStatusTracker)
from edextract.trackers.grade_tracker import (GradeKTracker, Grade1Tracker, Grade2Tracker, Grade3Tracker, Grade4Tracker,
                                              Grade5Tracker, Grade6Tracker, Grade7Tracker, Grade8Tracker, Grade9Tracker,
                                              Grade10Tracker, Grade11Tracker, Grade12Tracker)


def generate_statistics_report(tenant, output_file, task_info, extract_args):
    """
    Run generate_report with the arguments, directing it to call generate_statistics_report_data.

    @param tenant: Requestor's tenant ID
    @param output_file: File pathname of extract file
    @param task_info: Task information for recording stats
    @param extract_args: Arguments specific to generate_statistics_report_data
    """

    _generate_report(tenant, output_file, task_info, extract_args, _generate_statistics_report_data)


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
    academic_year_query = extract_args[TaskConstants.TASK_QUERIES][QueryType.QUERY]
    match_id_query = extract_args[TaskConstants.TASK_QUERIES][QueryType.MATCH_ID_QUERY]

    headers = extract_args[TaskConstants.CSV_HEADERS]

    data = data_extract_func(tenant, academic_year, academic_year_query, match_id_query)
    write_csv(output_file, headers, data)

    insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.EXTRACTED})


def _generate_statistics_report_data(tenant, academic_year, academic_year_query, match_id_query):
    """
    Get all the tenant's student registration data for the academic year.

    @param tenant: Requestor's tenant ID
    @param academic_year: Academic year of report
    @param query: DB query to extract rows

    @return: List of rows to be included in the CSV report.
    """

    with EdCoreDBConnection(tenant=tenant) as connection:
        academic_year_results = connection.get_streaming_result(academic_year_query)  # This result is a generator
        match_id_results = connection.get_streaming_result(match_id_query)

        data = _get_sr_stat_tenant_data_for_academic_year(academic_year_results, match_id_results, academic_year)

    return data


def _get_sr_stat_tenant_data_for_academic_year(academic_year_db_rows, match_id_db_rows, academic_year):
    """
    Get all the tenant's student registration data for the academic year.

    @param: db_rows: Iterable containing all pertinent database rows
    @param academic_year: Academic year of report

    @return: List of rows to be included in the CSV report.
    """

    total_tracker = TotalTracker()
    trackers = [total_tracker, MaleTracker(), FemaleTracker(), HispanicLatinoTracker(), AmericanIndianTracker(),
                AsianTracker(), AfricanAmericanTracker(), PacificIslanderTracker(), WhiteTracker(), MultiRaceTracker(),
                IDEAIndicatorTracker(), LEPStatusTracker(), Sec504StatusTracker(), EconDisadvStatusTracker(),
                MigrantStatusTracker(), GradeKTracker(), Grade1Tracker(), Grade2Tracker(), Grade3Tracker(),
                Grade4Tracker(), Grade5Tracker(), Grade6Tracker(), Grade7Tracker(), Grade8Tracker(), Grade9Tracker(),
                Grade10Tracker(), Grade11Tracker(), Grade12Tracker()]

    data_processors = [StateDataProcessor(trackers), DistrictDataProcessor(trackers), SchoolDataProcessor(trackers)]

    process_row_data(academic_year_db_rows, match_id_db_rows, data_processors)

    report_map = OrderedDict()
    for data_processor in data_processors:
        report_map.update(sorted(data_processor.get_ed_org_hierarchy().items()))

    return get_tracker_results(report_map, total_tracker, trackers, academic_year)
