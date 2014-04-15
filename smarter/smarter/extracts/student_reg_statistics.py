from sqlalchemy import or_, and_
from edcore.database.edcore_connector import EdCoreDBConnection
from smarter.security.context import select_with_context
from smarter.reports.helpers.constants import Constants
from smarter.security.constants import RolesConstants


__author__ = 'ablum'


def get_academic_year_query(academic_year, state_code):

    with EdCoreDBConnection(state_code=state_code) as connection:
        student_reg = connection.get_table(Constants.STUDENT_REG)
        academic_year_query = select_with_context([student_reg.c.state_code, student_reg.c.state_name, student_reg.c.district_guid, student_reg.c.district_name,
                                                   student_reg.c.school_guid, student_reg.c.school_name, student_reg.c.gender, student_reg.c.enrl_grade,
                                                   student_reg.c.dmg_eth_hsp, student_reg.c.dmg_eth_ami, student_reg.c.dmg_eth_asn, student_reg.c.dmg_eth_blk,
                                                   student_reg.c.dmg_eth_pcf, student_reg.c.dmg_eth_wht, student_reg.c.dmg_prg_iep, student_reg.c.dmg_prg_lep,
                                                   student_reg.c.dmg_prg_504, student_reg.c.dmg_sts_ecd, student_reg.c.dmg_sts_mig, student_reg.c.dmg_multi_race,
                                                   student_reg.c.academic_year],
                                                  from_obj=[student_reg], permission=RolesConstants.SRS_EXTRACTS, state_code=state_code).where(or_(student_reg.c.academic_year == academic_year,
                                                                                                                                                   student_reg.c.academic_year == academic_year - 1))
    return academic_year_query


def get_match_id_query(academic_year, state_code):
    with EdCoreDBConnection(state_code=state_code) as connection:
        student_reg = connection.get_table(Constants.STUDENT_REG)
        current_sr = student_reg.alias()
        prev_sr = student_reg.alias()

        match_id_query = select_with_context([current_sr.c.state_code, prev_sr.c.state_code.label('prev_state_code'), current_sr.c.state_name, current_sr.c.district_guid,
                                              prev_sr.c.district_guid.label('prev_district_guid'), current_sr.c.district_name, current_sr.c.school_guid,
                                              prev_sr.c.school_guid.label('prev_school_guid'), current_sr.c.school_name, current_sr.c.gender, prev_sr.c.gender.label('prev_gender'),
                                              current_sr.c.enrl_grade, prev_sr.c.enrl_grade.label('prev_enrl_grade'), current_sr.c.dmg_eth_hsp, prev_sr.c.dmg_eth_hsp.label('prev_dmg_eth_hsp'),
                                              current_sr.c.dmg_eth_ami, prev_sr.c.dmg_eth_ami.label('prev_dmg_eth_ami'), current_sr.c.dmg_eth_asn, prev_sr.c.dmg_eth_asn.label('prev_dmg_eth_asn'),
                                              current_sr.c.dmg_eth_blk, prev_sr.c.dmg_eth_blk.label('prev_dmg_eth_blk'), current_sr.c.dmg_eth_pcf, prev_sr.c.dmg_eth_pcf.label('prev_dmg_eth_pcf'),
                                              current_sr.c.dmg_eth_wht, prev_sr.c.dmg_eth_wht.label('prev_dmg_eth_wht'), current_sr.c.dmg_prg_iep,
                                              prev_sr.c.dmg_prg_iep.label('prev_dmg_prg_iep'), current_sr.c.dmg_prg_lep, prev_sr.c.dmg_prg_lep.label('prev_dmg_prg_lep'),
                                              current_sr.c.dmg_prg_504, prev_sr.c.dmg_prg_504.label('prev_dmg_prg_504'), current_sr.c.dmg_sts_ecd,
                                              prev_sr.c.dmg_sts_ecd.label('prev_dmg_sts_ecd'), current_sr.c.dmg_sts_mig,
                                              prev_sr.c.dmg_sts_mig.label('prev_dmg_sts_mig'), current_sr.c.dmg_multi_race, prev_sr.c.dmg_multi_race.label('prev_dmg_multi_race'), current_sr.c.academic_year],
                                             from_obj=[current_sr.join(prev_sr, and_(current_sr.c.student_guid == prev_sr.c.student_guid))], permission=RolesConstants.SRS_EXTRACTS, state_code=state_code)\
            .where(and_(current_sr.c.academic_year == academic_year, prev_sr.c.academic_year == academic_year - 1))
    return match_id_query


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
