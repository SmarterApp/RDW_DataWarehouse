__author__ = 'ablum'

from edcore.database.edcore_connector import EdCoreDBConnection
from smarter.reports.helpers.constants import Constants
from smarter.security.context import select_with_context
from smarter.security.constants import RolesConstants


def get_registered_query(academic_year, state_code):
    with EdCoreDBConnection(state_code=state_code) as connection:
        student_reg = connection.get_table(Constants.STUDENT_REG)
        registered_query = select_with_context([student_reg.c.state_code, student_reg.c.state_name, student_reg.c.district_guid,
                                                student_reg.c.district_name, student_reg.c.school_guid, student_reg.c.school_name,
                                                student_reg.c.gender, student_reg.c.enrl_grade, student_reg.c.dmg_eth_hsp,
                                                student_reg.c.dmg_eth_ami, student_reg.c.dmg_eth_asn, student_reg.c.dmg_eth_blk,
                                                student_reg.c.dmg_eth_pcf, student_reg.c.dmg_eth_wht, student_reg.c.dmg_prg_iep,
                                                student_reg.c.dmg_prg_lep, student_reg.c.dmg_prg_504, student_reg.c.dmg_sts_ecd,
                                                student_reg.c.dmg_sts_mig, student_reg.c.dmg_multi_race, student_reg.c.academic_year],
                                               from_obj=[student_reg], permission=RolesConstants.SRS_EXTRACTS,
                                               state_code=state_code).where(student_reg.c.academic_year == academic_year)

    return registered_query


def get_headers(academic_year):
    header = ('State',
              'District',
              'School',
              'Category',
              'Value',
              'AY{year} Count of Registered Students'.format(year=academic_year),
              'AY{year} Count of Students Assessed by Summative Math'.format(year=academic_year),
              'AY{year} Percent of Registered Students Assessed by Summative Math'.format(year=academic_year),
              'AY{year} Count of Students Assessed by Summative ELA'.format(year=academic_year),
              'AY{year} Percent of Registered Students Assessed by Summative ELA'.format(year=academic_year),
              'AY{year} Count of Students Assessed by Interim Comprehensive Math'.format(year=academic_year),
              'AY{year} Percent of Registered Students Assessed by Interim Comprehensive Math'.format(year=academic_year),
              'AY{year} Count of Students Assessed by Interim Comprehensive ELA'.format(year=academic_year),
              'AY{year} Percent of Registered Students Assessed by Interim Comprehensive ELA'.format(year=academic_year))

    return header
