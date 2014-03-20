__author__ = 'tshewchuk'

"""
This module contains methods to obtain data for the different Student Registration report types.
"""

import csv

from edextract.status.constants import Constants
from edextract.tasks.student_reg_constants import Constants as TaskConstants
from edextract.status.status import ExtractStatus, insert_extract_stats


def generate_statistics_report_data(state_code, academic_year):
    """
    This method generates the data for the student registration statistics report.

    @param state_code: Code for tenant state
    @param academic_year: Academic year of report

    @return: Report data, including field names
    """

    this_year = str(academic_year)
    last_year = str(academic_year - 1)
    header = ('State',
              'District',
              'School',
              'Category',
              'Value',
              '{last_year} Count'.format(last_year=last_year),
              '{last_year} Percent of Total'.format(last_year=last_year),
              '{this_year} Count'.format(this_year=this_year), '{this_year} Percent of Total'.format(this_year=this_year),
              'Change in Count',
              'Percent Difference in Count',
              'Change in Percent of Total',
              '{this_year} Matched IDs to {last_year} Count'.format(last_year=last_year, this_year=this_year),
              '{this_year} Matched IDs Percent of {last_year} count'.format(last_year=last_year, this_year=this_year))

    data = []

    return header, data


def generate_completion_report_data(state_code, academic_year):
    """
    This method generates the data for the student registration completion report.

    @param state_code: Code for tenant state
    @param academic_year: Academic year of report

    @return: Report data, including field names
    """

    header = ('State',
              'District',
              'School',
              'Grade',
              'Category',
              'Value',
              'Assessment Subject',
              'Assessment Type',
              'Assessment Date',
              'Academic Year',
              'Count of Students Registered',
              'Count of Students Assessed',
              'Percent of Students Assessed')

    data = []

    return header, data


def generate_statistics_report(output_file, task_info, extract_args):
    """
    Run generate_report with the arguments, directing it to call generate_statistics_report_data.

    @param output_file: File pathname of extract file
    @param task_info: Task information for recording stats
    @param extract_args: Arguments specific to generate_statistics_report_data
    """

    generate_report(output_file, task_info, extract_args, generate_statistics_report_data)


def generate_completion_report(output_file, task_info, extract_args):
    """
    Run generate_report with the arguments, directing it to call generate_completion_report_data.

    @param output_file: File pathname of extract file
    @param task_info: Task information for recording stats
    @param extract_args: Arguments specific to generate_completion_report_data
    """

    generate_report(output_file, task_info, extract_args, generate_completion_report_data)


def generate_report(output_file, task_info, extract_args, data_extract_func):
    """
    Generate the student registration statistics report CSV file.

    @param output_file: File pathname of extract file
    @param task_info: Task information for recording stats
    @param extract_args: Arguments specific to generate_completion_report_data
    @param data_extract_func: Function to perform the specific report data extraction
    """

    state_code = extract_args[TaskConstants.STATE_CODE]
    academic_year = extract_args[TaskConstants.ACADEMIC_YEAR]

    header, data = data_extract_func(state_code, academic_year)

    with open(output_file, 'w') as csv_file:
        csvwriter = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(header)
        for row in data:
            csvwriter.writerow(row)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.EXTRACTED})
