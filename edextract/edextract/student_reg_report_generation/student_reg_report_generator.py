__author__ = 'tshewchuk'

"""
This module contains methods to obtain data for the different Student Registration report types.
"""


def generate_sr_statistics_report_data(state_code, academic_year):
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


def generate_sr_completion_report_data(state_code, academic_year):
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
