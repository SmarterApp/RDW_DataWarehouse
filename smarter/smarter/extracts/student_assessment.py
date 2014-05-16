'''
Created on Nov 1, 2013

@author: ejen
'''
from edcore.database.edcore_connector import EdCoreDBConnection
from sqlalchemy.sql.expression import and_
from smarter.reports.helpers.constants import Constants
from smarter.security.context import select_with_context
from smarter.extracts.format import get_column_mapping
from smarter.security.constants import RolesConstants
from smarter.reports.helpers.filters import apply_filter_to_query


def get_extract_assessment_query(params):
    """
    private method to generate SQLAlchemy object or sql code for extraction

    :param params: for query parameters asmt_type, asmt_subject, asmt_year, limit
    """
    state_code = params.get(Constants.STATECODE)
    district_guid = params.get(Constants.DISTRICTGUID)
    school_guid = params.get(Constants.SCHOOLGUID)
    asmt_grade = params.get(Constants.ASMTGRADE)
    asmt_type = params.get(Constants.ASMTTYPE)
    asmt_year = params.get(Constants.ASMTYEAR)
    asmt_subject = params.get(Constants.ASMTSUBJECT)

    dim_student_label = get_column_mapping(Constants.DIM_STUDENT)
    dim_inst_hier_label = get_column_mapping(Constants.DIM_INST_HIER)
    dim_asmt_label = get_column_mapping(Constants.DIM_ASMT)
    fact_asmt_outcome_label = get_column_mapping(Constants.FACT_ASMT_OUTCOME)

    with EdCoreDBConnection(state_code=state_code) as connector:
        dim_student = connector.get_table(Constants.DIM_STUDENT)
        dim_asmt = connector.get_table(Constants.DIM_ASMT)
        dim_inst_hier = connector.get_table(Constants.DIM_INST_HIER)
        fact_asmt_outcome = connector.get_table(Constants.FACT_ASMT_OUTCOME)
        # TODO: Look at removing dim_asmt
        query = select_with_context([dim_asmt.c.asmt_guid.label(dim_asmt_label.get(Constants.ASMT_GUID, Constants.ASMT_GUID)),
                                    fact_asmt_outcome.c.where_taken_id.label(fact_asmt_outcome_label.get('where_taken_id', 'guid_asmt_location')),
                                    fact_asmt_outcome.c.where_taken_name.label(dim_asmt_label.get('where_taken_name', 'name_asmt_location')),
                                    fact_asmt_outcome.c.asmt_grade.label(fact_asmt_outcome_label.get(Constants.ASMT_GRADE, Constants.ASMT_GRADE)),
                                    dim_inst_hier.c.state_name.label(dim_inst_hier_label.get(Constants.STATE_NAME, 'name_state')),
                                    dim_inst_hier.c.state_code.label(dim_inst_hier_label.get(Constants.STATE_CODE, 'code_state')),
                                    dim_inst_hier.c.district_guid.label(dim_inst_hier_label.get(Constants.DISTRICT_GUID, 'name_distrct')),
                                    dim_inst_hier.c.district_name.label(dim_inst_hier_label.get(Constants.DISTRICT_NAME, 'name_distrct')),
                                    dim_inst_hier.c.school_guid.label(dim_inst_hier_label.get(Constants.SCHOOL_GUID, 'guid_school')),
                                    dim_inst_hier.c.school_name.label(dim_inst_hier_label.get(Constants.SCHOOL_NAME, 'name_school')),
                                    dim_student.c.student_guid.label(dim_student_label.get(Constants.STUDENT_GUID, 'guid_student')),
                                    dim_student.c.first_name.label(dim_student_label.get('first_name', 'student_first_name')),
                                    dim_student.c.middle_name.label(dim_student_label.get('middle_name', 'student_middle_name')),
                                    dim_student.c.last_name.label(dim_student_label.get('last_name', 'student_last_name')),
                                    dim_student.c.gender.label(dim_student_label.get('gender', 'gender')),
                                    dim_student.c.email.label(dim_student_label.get('email', 'email')),
                                    dim_student.c.dob.label(dim_student_label.get('dob', 'dob')),
                                    fact_asmt_outcome.c.external_student_id.label(fact_asmt_outcome_label.get('external_student_id', 'external_student_id')),
                                    fact_asmt_outcome.c.enrl_grade.label(fact_asmt_outcome_label.get('enrl_grade', 'enrollment_grade')),
                                    fact_asmt_outcome.c.date_taken.label(fact_asmt_outcome_label.get('date_taken', 'date_taken')),
                                    fact_asmt_outcome.c.asmt_score.label(fact_asmt_outcome_label.get('asmt_score', 'asmt_score')),
                                    fact_asmt_outcome.c.asmt_score_range_min.label(fact_asmt_outcome_label.get('asmt_score_range_min', 'asmt_score_range_min')),
                                    fact_asmt_outcome.c.asmt_score_range_max.label(fact_asmt_outcome_label.get('asmt_score_range_max', 'asmt_score_range_max')),
                                    fact_asmt_outcome.c.asmt_perf_lvl.label(fact_asmt_outcome_label.get('asmt_perf_lvl', 'asmt_perf_lvl')),
                                    fact_asmt_outcome.c.asmt_claim_1_score.label(fact_asmt_outcome_label.get('asmt_claim_1_score', 'asmt_claim_1_score')),
                                    fact_asmt_outcome.c.asmt_claim_1_perf_lvl.label(fact_asmt_outcome_label.get('asmt_claim_1_perf_lvl', 'asmt_claim_1_perf_lvl')),
                                    fact_asmt_outcome.c.asmt_claim_1_score_range_min.label(fact_asmt_outcome_label.get('asmt_claim_1_score_range_min', 'asmt_claim_1_score_range_min')),
                                    fact_asmt_outcome.c.asmt_claim_1_score_range_max.label(fact_asmt_outcome_label.get('asmt_claim_1_score_range_max', 'asmt_claim_1_score_range_max')),
                                    fact_asmt_outcome.c.asmt_claim_2_score.label(fact_asmt_outcome_label.get('asmt_claim_2_score', 'asmt_claim_2_score')),
                                    fact_asmt_outcome.c.asmt_claim_2_perf_lvl.label(fact_asmt_outcome_label.get('asmt_claim_2_perf_lvl', 'asmt_claim_2_perf_lvl')),
                                    fact_asmt_outcome.c.asmt_claim_2_score_range_min.label(fact_asmt_outcome_label.get('asmt_claim_2_score_range_min', 'asmt_claim_2_score_range_min')),
                                    fact_asmt_outcome.c.asmt_claim_2_score_range_max.label(fact_asmt_outcome_label.get('asmt_claim_2_score_range_max', 'asmt_claim_2_score_range_max')),
                                    fact_asmt_outcome.c.asmt_claim_3_score.label(fact_asmt_outcome_label.get('asmt_claim_3_score', 'asmt_claim_3_score')),
                                    fact_asmt_outcome.c.asmt_claim_3_perf_lvl.label(fact_asmt_outcome_label.get('asmt_claim_3_perf_lvl', 'asmt_claim_3_perf_lvl')),
                                    fact_asmt_outcome.c.asmt_claim_3_score_range_min.label(fact_asmt_outcome_label.get('asmt_claim_3_score_range_min', 'asmt_claim_3_score_range_min')),
                                    fact_asmt_outcome.c.asmt_claim_3_score_range_max.label(fact_asmt_outcome_label.get('asmt_claim_3_score_range_max', 'asmt_claim_3_score_range_max')),
                                    fact_asmt_outcome.c.asmt_claim_4_score.label(fact_asmt_outcome_label.get('asmt_claim_4_score', 'asmt_claim_4_score')),
                                    fact_asmt_outcome.c.asmt_claim_4_perf_lvl.label(fact_asmt_outcome_label.get('asmt_claim_4_perf_lvl', 'asmt_claim_4_perf_lvl')),
                                    fact_asmt_outcome.c.asmt_claim_4_score_range_min.label(fact_asmt_outcome_label.get('asmt_claim_4_score_range_min', 'asmt_claim_4_score_range_min')),
                                    fact_asmt_outcome.c.asmt_claim_4_score_range_max.label(fact_asmt_outcome_label.get('asmt_claim_4_score_range_max', 'asmt_claim_4_score_range_max')),
                                    fact_asmt_outcome.c.dmg_eth_hsp.label(fact_asmt_outcome_label.get(Constants.DMG_ETH_HSP, Constants.DMG_ETH_HSP)),
                                    fact_asmt_outcome.c.dmg_eth_ami.label(fact_asmt_outcome_label.get(Constants.DMG_ETH_AMI, Constants.DMG_ETH_AMI)),
                                    fact_asmt_outcome.c.dmg_eth_asn.label(fact_asmt_outcome_label.get(Constants.DMG_ETH_ASN, Constants.DMG_ETH_ASN)),
                                    fact_asmt_outcome.c.dmg_eth_blk.label(fact_asmt_outcome_label.get(Constants.DMG_ETH_BLK, Constants.DMG_ETH_BLK)),
                                    fact_asmt_outcome.c.dmg_eth_pcf.label(fact_asmt_outcome_label.get(Constants.DMG_ETH_PCF, Constants.DMG_ETH_PCF)),
                                    fact_asmt_outcome.c.dmg_eth_wht.label(fact_asmt_outcome_label.get(Constants.DMG_ETH_WHT, Constants.DMG_ETH_WHT)),
                                    fact_asmt_outcome.c.dmg_prg_iep.label(fact_asmt_outcome_label.get('dmg_prg_iep', 'dmg_prg_iep')),
                                    fact_asmt_outcome.c.dmg_prg_lep.label(fact_asmt_outcome_label.get('dmg_prg_lep', 'dmg_prg_lep')),
                                    fact_asmt_outcome.c.dmg_prg_504.label(fact_asmt_outcome_label.get('dmg_prg_504', 'dmg_prg_504')),
                                    fact_asmt_outcome.c.dmg_prg_tt1.label(fact_asmt_outcome_label.get('dmg_prg_tt1', 'dmg_prg_tt1')),
                                    fact_asmt_outcome.c.asmt_type.label(fact_asmt_outcome_label.get(Constants.ASMT_TYPE, Constants.ASMT_TYPE)),
                                    fact_asmt_outcome.c.asmt_year.label(fact_asmt_outcome_label.get(Constants.ASMT_YEAR, Constants.ASMT_YEAR)),
                                    fact_asmt_outcome.c.asmt_subject.label(fact_asmt_outcome_label.get(Constants.ASMT_SUBJECT, Constants.ASMT_SUBJECT)),
                                    fact_asmt_outcome.c.acc_asl_video_embed.label(fact_asmt_outcome_label.get('acc_asl_video_embed', 'acc_asl_video_embed')),
                                    fact_asmt_outcome.c.acc_asl_human_nonembed.label(fact_asmt_outcome_label.get('acc_asl_human_nonembed', 'acc_asl_human_nonembed')),
                                    fact_asmt_outcome.c.acc_braile_embed.label(fact_asmt_outcome_label.get('acc_braile_embed', 'acc_braile_embed')),
                                    fact_asmt_outcome.c.acc_closed_captioning_embed.label(fact_asmt_outcome_label.get('acc_closed_captioning_embed', 'acc_closed_captioning_embed')),
                                    fact_asmt_outcome.c.acc_text_to_speech_embed.label(fact_asmt_outcome_label.get('acc_text_to_speech_embed', 'acc_text_to_speech_embed')),
                                    fact_asmt_outcome.c.acc_abacus_nonembed.label(fact_asmt_outcome_label.get('acc_abacus_nonembed', 'acc_abacus_nonembed')),
                                    fact_asmt_outcome.c.acc_alternate_response_options_nonembed.label(fact_asmt_outcome_label.get('acc_alternate_response_options_nonembed', 'acc_alternate_response_options_nonembed')),
                                    fact_asmt_outcome.c.acc_calculator_nonembed.label(fact_asmt_outcome_label.get('acc_calculator_nonembed', 'acc_calculator_nonembed')),
                                    fact_asmt_outcome.c.acc_multiplication_table_nonembed.label(fact_asmt_outcome_label.get('acc_multiplication_table_nonembed', 'acc_multiplication_table_nonembed')),
                                    fact_asmt_outcome.c.acc_print_on_demand_nonembed.label(fact_asmt_outcome_label.get('acc_print_on_demand_nonembed', 'acc_print_on_demand_nonembed')),
                                    fact_asmt_outcome.c.acc_read_aloud_nonembed.label(fact_asmt_outcome_label.get('acc_read_aloud_nonembed', 'acc_read_aloud_nonembed')),
                                    fact_asmt_outcome.c.acc_scribe_nonembed.label(fact_asmt_outcome_label.get('acc_scribe_nonembed', 'acc_scribe_nonembed')),
                                    fact_asmt_outcome.c.acc_speech_to_text_nonembed.label(fact_asmt_outcome_label.get('acc_speech_to_text_nonembed', 'acc_speech_to_text_nonembed')),
                                    fact_asmt_outcome.c.acc_streamline_mode.label(fact_asmt_outcome_label.get('acc_streamline_mode', 'acc_streamline_mode'))],
                                    from_obj=[fact_asmt_outcome
                                              .join(dim_student, and_(fact_asmt_outcome.c.student_rec_id == dim_student.c.student_rec_id))
                                              .join(dim_asmt, and_(dim_asmt.c.asmt_rec_id == fact_asmt_outcome.c.asmt_rec_id,
                                                                   dim_asmt.c.asmt_type == asmt_type))
                                              .join(dim_inst_hier, and_(dim_inst_hier.c.inst_hier_rec_id == fact_asmt_outcome.c.inst_hier_rec_id))], permission=RolesConstants.SAR_EXTRACTS, state_code=state_code)

        query = query.where(and_(fact_asmt_outcome.c.state_code == state_code))
        query = query.where(and_(fact_asmt_outcome.c.asmt_type == asmt_type))
        query = query.where(and_(fact_asmt_outcome.c.rec_status == Constants.CURRENT))
        if school_guid is not None:
            query = query.where(and_(fact_asmt_outcome.c.school_guid == school_guid))
        if district_guid is not None:
            query = query.where(and_(fact_asmt_outcome.c.district_guid == district_guid))
        if asmt_year is not None:
            query = query.where(and_(fact_asmt_outcome.c.asmt_year == asmt_year))
        if asmt_subject is not None:
            query = query.where(and_(fact_asmt_outcome.c.asmt_subject == asmt_subject))
        if asmt_grade is not None:
            query = query.where(and_(fact_asmt_outcome.c.asmt_grade == asmt_grade))

        query = query.order_by(dim_student.c.last_name).order_by(dim_student.c.first_name)
    return query


def get_extract_assessment_item_query(params):
    """
    private method to generate SQLAlchemy object or sql code for extraction of students for item level data

    :param params: for query parameters asmt_year, asmt_type, asmt_subject, asmt_grade
    """
    state_code = params.get(Constants.STATECODE)
    asmt_year = params.get(Constants.ASMTYEAR)
    asmt_type = params.get(Constants.ASMTTYPE)
    asmt_subject = params.get(Constants.ASMTSUBJECT)
    asmt_grade = params.get(Constants.ASMTGRADE)

    with EdCoreDBConnection(state_code=state_code) as connector:
        dim_asmt = connector.get_table(Constants.DIM_ASMT)
        fact_asmt_outcome = connector.get_table(Constants.FACT_ASMT_OUTCOME)
        # TODO: Look at removing dim_asmt
        query = select_with_context([fact_asmt_outcome.c.state_code,
                                     fact_asmt_outcome.c.asmt_year,
                                     fact_asmt_outcome.c.asmt_type,
                                     dim_asmt.c.effective_date,
                                     fact_asmt_outcome.c.asmt_subject,
                                     fact_asmt_outcome.c.asmt_grade,
                                     fact_asmt_outcome.c.district_guid,
                                     fact_asmt_outcome.c.student_guid],
                                    from_obj=[fact_asmt_outcome
                                              .join(dim_asmt, and_(dim_asmt.c.asmt_rec_id == fact_asmt_outcome.c.asmt_rec_id))],
                                    permission=RolesConstants.SAR_EXTRACTS,
                                    state_code=state_code)

        query = query.where(and_(fact_asmt_outcome.c.asmt_year == asmt_year))
        query = query.where(and_(fact_asmt_outcome.c.asmt_type == asmt_type))
        query = query.where(and_(fact_asmt_outcome.c.asmt_subject == asmt_subject))
        query = query.where(and_(fact_asmt_outcome.c.asmt_grade == asmt_grade))
        query = query.where(and_(fact_asmt_outcome.c.rec_status == Constants.CURRENT))
        query = apply_filter_to_query(query, fact_asmt_outcome, params)  # Filters demographics
    return query
