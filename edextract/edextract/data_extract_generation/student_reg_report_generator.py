__author__ = 'tshewchuk'

"""
This module contains methods to obtain data for the different Student Registration report types.
"""

import csv
from sqlalchemy.sql.expression import select

from edextract.status.constants import Constants
from edextract.tasks.student_reg_constants import Constants as TaskConstants, TableName
from edextract.status.status import ExtractStatus, insert_extract_stats
from edcore.database.edcore_connector import EdCoreDBConnection


def generate_statistics_report_data(tenant, academic_year):
    """
    This method generates the data for the student registration statistics report.

    @param tenant: Requestor's tenant ID
    @param academic_year: Academic year of report

    @return: Report header and data
    """

    this_year = str(academic_year)
    last_year = str(academic_year - 1)
    header = ('State',
              'District',
              'School',
              'Category',
              'Value',
              'AY{last_year} Count'.format(last_year=last_year),
              'AY{last_year} Percent of Total'.format(last_year=last_year),
              'AY{this_year} Count'.format(this_year=this_year), 'AY{this_year} Percent of Total'.format(this_year=this_year),
              'Change in Count',
              'Percent Difference in Count',
              'Change in Percent of Total',
              'AY{this_year} Matched IDs to AY{last_year} Count'.format(last_year=last_year, this_year=this_year),
              'AY{this_year} Matched IDs Percent of AY{last_year} count'.format(last_year=last_year, this_year=this_year))

    data = get_sr_tenant_data_for_academic_year(tenant, academic_year)

    return header, data


def generate_completion_report_data(tenant, academic_year):
    """
    This method generates the data for the student registration completion report.

    @param tenant: Requestor's tenant ID
    @param academic_year: Academic year of report

    @return: Report header and data
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


def generate_statistics_report(tenant, output_file, task_info, extract_args):
    """
    Run generate_report with the arguments, directing it to call generate_statistics_report_data.

    @param tenant: Requestor's tenant ID
    @param output_file: File pathname of extract file
    @param task_info: Task information for recording stats
    @param extract_args: Arguments specific to generate_statistics_report_data
    """

    generate_report(tenant, output_file, task_info, extract_args, generate_statistics_report_data)


def generate_completion_report(tenant, output_file, task_info, extract_args):
    """
    Run generate_report with the arguments, directing it to call generate_completion_report_data.

    @param tenant: Requestor's tenant ID
    @param output_file: File pathname of extract file
    @param task_info: Task information for recording stats
    @param extract_args: Arguments specific to generate_completion_report_data
    """

    generate_report(tenant, output_file, task_info, extract_args, generate_completion_report_data)


def generate_report(tenant, output_file, task_info, extract_args, data_extract_func):
    """
    Generate the student registration statistics report CSV file.

    @param tenant: Requestor's tenant ID
    @param output_file: File pathname of extract file
    @param task_info: Task information for recording stats
    @param extract_args: Arguments specific to generate_completion_report_data
    @param data_extract_func: Function to perform the specific report data extraction
    """

    academic_year = extract_args[TaskConstants.ACADEMIC_YEAR]

    header, data = data_extract_func(tenant, academic_year)

    with open(output_file, 'w') as csv_file:
        csvwriter = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(header)
        for row in data:
            csvwriter.writerow(row)
        insert_extract_stats(task_info, {Constants.STATUS: ExtractStatus.EXTRACTED})


def get_sr_tenant_data_for_academic_year(tenant, academic_year):
    """
    Get all the tenant's student registration data for the academic year.

    @param tenant: Requestor's tenant ID
    @param academic_year: Academic year of report

    @return:
    """

    with EdCoreDBConnection(tenant=tenant) as connection:
        student_reg = connection.get_table(TableName.STUDENT_REG)
        query = select([student_reg.c.state_name, student_reg.c.district_name, student_reg.c.school_name, student_reg.c.gender,
                       student_reg.c.enrl_grade, student_reg.c.dmg_eth_hsp, student_reg.c.dmg_eth_ami, student_reg.c.dmg_eth_asn,
                       student_reg.c.dmg_eth_blk, student_reg.c.dmg_eth_pcf, student_reg.c.dmg_eth_wht, student_reg.c.dmg_prg_iep,
                       student_reg.c.dmg_prg_lep, student_reg.c.dmg_prg_504, student_reg.c.dmg_sts_ecd, student_reg.c.dmg_sts_mig,
                       student_reg.c.dmg_multi_race], from_obj=[student_reg]).where(student_reg.c.academic_year == academic_year)

        results = connection.get_streaming_result(query)  # This result is a generator

    data = []

    return data
