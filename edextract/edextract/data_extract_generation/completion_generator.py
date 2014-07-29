__author__ = 'tshewchuk'

"""
This module contains functions to generate data rows for the Student Registration Completion Report.
"""

from edextract.data_extract_generation.data_generator_helper import format_intval, percentage, format_floatval, get_row_identifiers
from edextract.student_reg_extract_processors.assessment_constants import AssessmentType, AssessmentSubject


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
            current_year_count = summ_math_count = summ_ela_count = int_comp_math_count = int_comp_ela_count = 0
            if entry_data:
                current_year_count = entry_data.get(current_year, 0)
                summ_math_count = entry_data.get((AssessmentType.SUMMATIVE, AssessmentSubject.MATH), 0)
                summ_ela_count = entry_data.get((AssessmentType.SUMMATIVE, AssessmentSubject.ELA), 0)
                int_comp_math_count = entry_data.get((AssessmentType.INTERIM_COMPREHENSIVE, AssessmentSubject.MATH), 0)
                int_comp_ela_count = entry_data.get((AssessmentType.INTERIM_COMPREHENSIVE, AssessmentSubject.ELA), 0)

            row = [state_name, district_name, school_name, category, value] + _generate_data_row(current_year_count, summ_math_count,
                                                                                                 summ_ela_count, int_comp_math_count,
                                                                                                 int_comp_ela_count)

            yield row


def _generate_data_row(registered_count, summ_math_count, summ_ela_count, int_comp_math_count, int_comp_ela_count):
    '''
    Generates a data row with completion data.

    @param registered_count: The count of registered students of a certain demographic for the current year
    @param summ_math_count: The count of registered students of a certain demographic who took Summative Math assessments
    @param summ_ela_count: The count of registered students of a certain demographic who took Summative ELA assessments
    @param int_comp_math_count: The count of registered students of a certain demographic who took Interim Comprehensive Math assessments
    @param int_comp_ela_count: The count of registered students of a certain demographic who took Interim Comprehensive ELA assessments

    @return: A data row including all completion data
    '''

    summ_math_percent = percentage(summ_math_count, registered_count)
    summ_ela_percent = percentage(summ_ela_count, registered_count)
    int_comp_math_percent = percentage(int_comp_math_count, registered_count)
    int_comp_ela_percent = percentage(int_comp_ela_count, registered_count)

    return [format_intval(registered_count), format_intval(summ_math_count), format_floatval(summ_math_percent),
            format_intval(summ_ela_count), format_floatval(summ_ela_percent), format_intval(int_comp_math_count),
            format_floatval(int_comp_math_percent), format_intval(int_comp_ela_count), format_floatval(int_comp_ela_percent)]
