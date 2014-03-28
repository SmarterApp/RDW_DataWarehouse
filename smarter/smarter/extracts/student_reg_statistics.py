from sqlalchemy import or_
from edcore.database.edcore_connector import EdCoreDBConnection
from smarter.security.context import select_with_context
from smarter.reports.helpers.constants import Constants


__author__ = 'ablum'


def get_query(academic_year, state_code):

    with EdCoreDBConnection(state_code=state_code) as connection:
        student_reg = connection.get_table(Constants.STUDENT_REG)
        query = select_with_context([student_reg.c.state_code, student_reg.c.state_name, student_reg.c.district_guid, student_reg.c.district_name,
                                     student_reg.c.school_guid, student_reg.c.school_name, student_reg.c.gender, student_reg.c.enrl_grade,
                                     student_reg.c.dmg_eth_hsp, student_reg.c.dmg_eth_ami, student_reg.c.dmg_eth_asn, student_reg.c.dmg_eth_blk,
                                     student_reg.c.dmg_eth_pcf, student_reg.c.dmg_eth_wht, student_reg.c.dmg_prg_iep, student_reg.c.dmg_prg_lep,
                                     student_reg.c.dmg_prg_504, student_reg.c.dmg_sts_ecd, student_reg.c.dmg_sts_mig, student_reg.c.dmg_multi_race,
                                     student_reg.c.academic_year],
                                    from_obj=[student_reg], state_code=state_code).where(or_(student_reg.c.academic_year == academic_year,
                                                                                             student_reg.c.academic_year == academic_year - 1))
    return query


def get_headers(academic_year):
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
              'AY{this_year} Matched IDs Percent of AY{last_year} Count'.format(last_year=last_year, this_year=this_year))

    return header
