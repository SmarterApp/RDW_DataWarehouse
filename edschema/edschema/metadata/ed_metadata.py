'''
create_star -- create a star schema

create_star will create a database, a schema within the database, and all the required tables, indexes,
and foreign keys required to implement the star schema

Command line options are available form --help, but as a quick start:
    to locally create a schema use something like:
        --database --name <your_star_db> --schema --sname <your_schema_name> --tables --verbose
    to make a schema on QA:
        --database --name <qa_star_date> --schema --sname <edware> --tables --server monetdb1.poc.dum.edwdc.net:5432 --user edware --password edware --verbose

@author:     smacgibbon

@copyright:  2013 Wireless Generation. All rights reserved.

@contact:    edwaredevs@wgen.net
@deffield    updated: Updated
'''
from sqlalchemy.schema import MetaData
from sqlalchemy import Table, Column, Index
from sqlalchemy import SmallInteger, String, Boolean, Float, BigInteger
from sqlalchemy import ForeignKey
from sqlalchemy.types import Text

__all__ = []
__version__ = 0.1
__date__ = '2013-02-02'
__updated__ = '2014-04-03'


class MetaColumn(Column):
    col_type = 'MetaColumn'


def generate_ed_metadata(schema_name=None, bind=None):

    metadata = MetaData(schema=schema_name, bind=bind)

    # Two-letter state - some countries have 3 or more, but two will do for US
    instit_hier = Table('dim_inst_hier', metadata,
                        Column('inst_hier_rec_id', BigInteger, primary_key=True),
                        Column('state_code', String(2), nullable=False, info={'natural_key': True}),
                        Column('state_name', String(50), nullable=False),
                        Column('district_guid', String(50), nullable=False, info={'natural_key': True}),
                        Column('district_name', String(60), nullable=False),
                        Column('school_guid', String(50), nullable=False, info={'natural_key': True}),
                        Column('school_name', String(60), nullable=False),
                        MetaColumn('from_date', String(8), nullable=False),
                        MetaColumn('to_date', String(8), nullable=True),
                        MetaColumn('rec_status', String(1), nullable=False),
                        MetaColumn('batch_guid', String(50), nullable=False),
                        )

    Index('dim_inst_hier_rec_pk_idx', instit_hier.c.inst_hier_rec_id, unique=True)
    Index('dim_inst_hier_codex', instit_hier.c.state_code, instit_hier.c.district_guid, instit_hier.c.school_guid, unique=False)

    # NB! Figure out uniques in dim_student
    students = Table('dim_student', metadata,
                     Column('student_rec_id', BigInteger, primary_key=True),
                     Column('student_guid', String(50), nullable=False, info={'natural_key': True}),
                     Column('external_student_id', String(50), nullable=True),
                     Column('first_name', String(35), nullable=False),
                     Column('middle_name', String(35), nullable=True),
                     Column('last_name', String(35), nullable=False),
                     Column('birthdate', String(8), nullable=False),
                     Column('sex', String(10), nullable=False),
                     Column('email', String(128), nullable=True),
                     Column('dmg_eth_derived', SmallInteger, nullable=True),
                     Column('dmg_eth_hsp', Boolean, nullable=True),
                     Column('dmg_eth_ami', Boolean, nullable=True),
                     Column('dmg_eth_asn', Boolean, nullable=True),
                     Column('dmg_eth_blk', Boolean, nullable=True),
                     Column('dmg_eth_pcf', Boolean, nullable=True),
                     Column('dmg_eth_wht', Boolean, nullable=True),
                     Column('dmg_prg_iep', Boolean, nullable=True),
                     Column('dmg_prg_lep', Boolean, nullable=True),
                     Column('dmg_prg_504', Boolean, nullable=True),
                     Column('dmg_prg_tt1', Boolean, nullable=True),
                     MetaColumn('from_date', String(8), nullable=False),
                     MetaColumn('to_date', String(8), nullable=True),
                     MetaColumn('rec_status', String(1), nullable=False),
                     MetaColumn('batch_guid', String(50), nullable=False),
                     )

    Index('dim_student_rec_pk_idx', students.c.student_rec_id, unique=True)
    Index('dim_student_guid_idx', students.c.student_guid, unique=False)

    assessment = Table('dim_asmt', metadata,
                       Column('asmt_rec_id', BigInteger, primary_key=True),
                       Column('asmt_guid', String(50), nullable=False, info={'natural_key': True}),
                       Column('asmt_type', String(32), nullable=False),
                       Column('asmt_period', String(32), nullable=False),
                       Column('asmt_period_year', SmallInteger, nullable=False),
                       Column('asmt_version', String(16), nullable=False),
                       Column('asmt_subject', String(64), nullable=False),
                       MetaColumn('effective_date', String(8), nullable=False),
                       Column('asmt_claim_1_name', String(128), nullable=True),
                       Column('asmt_claim_2_name', String(128), nullable=True),
                       Column('asmt_claim_3_name', String(128), nullable=True),
                       Column('asmt_claim_4_name', String(128), nullable=True),
                       Column('asmt_perf_lvl_name_1', String(128), nullable=True),
                       Column('asmt_perf_lvl_name_2', String(128), nullable=True),
                       Column('asmt_perf_lvl_name_3', String(128), nullable=True),
                       Column('asmt_perf_lvl_name_4', String(128), nullable=True),
                       Column('asmt_perf_lvl_name_5', String(128), nullable=True),
                       Column('asmt_claim_perf_lvl_name_1', String(128), nullable=True),
                       Column('asmt_claim_perf_lvl_name_2', String(128), nullable=True),
                       Column('asmt_claim_perf_lvl_name_3', String(128), nullable=True),
                       Column('asmt_score_min', SmallInteger, nullable=False),
                       Column('asmt_score_max', SmallInteger, nullable=False),
                       Column('asmt_claim_1_score_min', SmallInteger, nullable=False),
                       Column('asmt_claim_1_score_max', SmallInteger, nullable=False),
                       Column('asmt_claim_2_score_min', SmallInteger, nullable=False),
                       Column('asmt_claim_2_score_max', SmallInteger, nullable=False),
                       Column('asmt_claim_3_score_min', SmallInteger, nullable=False),
                       Column('asmt_claim_3_score_max', SmallInteger, nullable=False),
                       Column('asmt_claim_4_score_min', SmallInteger, nullable=True),
                       Column('asmt_claim_4_score_max', SmallInteger, nullable=True),
                       Column('asmt_cut_point_1', SmallInteger, nullable=True),
                       Column('asmt_cut_point_2', SmallInteger, nullable=True),
                       Column('asmt_cut_point_3', SmallInteger, nullable=True),
                       Column('asmt_cut_point_4', SmallInteger, nullable=True),
                       MetaColumn('from_date', String(8), nullable=False),
                       MetaColumn('to_date', String(8), nullable=True),
                       MetaColumn('rec_status', String(1), nullable=False),
                       MetaColumn('batch_guid', String(50), nullable=False),
                       )

    Index('dim_asmt_rec_pk_idx', assessment.c.asmt_rec_id, unique=True)
    Index('dim_asmt_guid_idx', assessment.c.asmt_guid, unique=False)
    Index('dim_asmt_id_type_idx', assessment.c.asmt_rec_id, assessment.c.asmt_type, unique=False)

    custom_metadata = Table('custom_metadata', metadata,
                            Column('state_code', String(2), nullable=False),
                            Column('asmt_subject', String(100), nullable=False),
                            Column('asmt_custom_metadata', Text, nullable=True)
                            )
    Index('custom_metadata_id_idx', custom_metadata.c.state_code, custom_metadata.c.asmt_subject, unique=True)

    assessment_outcome_vw = Table('fact_asmt_outcome_vw', metadata,
                                  Column('asmt_outcome_vw_rec_id', BigInteger, primary_key=True),
                                  Column('asmt_rec_id', BigInteger, ForeignKey(assessment.c.asmt_rec_id), nullable=False),
                                  Column('student_rec_id', BigInteger, ForeignKey(students.c.student_rec_id), nullable=False),
                                  Column('inst_hier_rec_id', BigInteger, ForeignKey(instit_hier.c.inst_hier_rec_id), nullable=False),
                                  Column('asmt_guid', String(50), nullable=False, info={'natural_key': True}),
                                  Column('student_guid', String(50), nullable=False, info={'natural_key': True}),
                                  Column('state_code', String(2), nullable=False),
                                  Column('district_guid', String(50), nullable=False),
                                  Column('school_guid', String(50), nullable=False),
                                  Column('where_taken_id', String(50), nullable=True),  # external id if provided
                                  Column('where_taken_name', String(60), nullable=True),
                                  Column('asmt_type', String(32), nullable=False),
                                  Column('asmt_year', SmallInteger, nullable=False),
                                  Column('asmt_subject', String(64), nullable=False),
                                  Column('asmt_grade', String(10), nullable=False),
                                  Column('enrl_grade', String(10), nullable=False),
                                  Column('group_1_id', String(50), nullable=True),
                                  Column('group_1_text', String(60), nullable=True),
                                  Column('group_2_id', String(50), nullable=True),
                                  Column('group_2_text', String(60), nullable=True),
                                  Column('date_taken', String(8), nullable=False),
                                  Column('date_taken_day', SmallInteger, nullable=False),
                                  Column('date_taken_month', SmallInteger, nullable=False),
                                  Column('date_taken_year', SmallInteger, nullable=False),
                                  Column('asmt_score', SmallInteger, nullable=False),
                                  Column('asmt_score_range_min', SmallInteger, nullable=False),
                                  Column('asmt_score_range_max', SmallInteger, nullable=False),
                                  Column('asmt_perf_lvl', SmallInteger, nullable=False),
                                  Column('asmt_claim_1_score', SmallInteger, nullable=True),
                                  Column('asmt_claim_1_score_range_min', SmallInteger, nullable=True),
                                  Column('asmt_claim_1_score_range_max', SmallInteger, nullable=True),
                                  Column('asmt_claim_1_perf_lvl', SmallInteger, nullable=True),
                                  Column('asmt_claim_2_score', SmallInteger, nullable=True),
                                  Column('asmt_claim_2_score_range_min', SmallInteger, nullable=True),
                                  Column('asmt_claim_2_score_range_max', SmallInteger, nullable=True),
                                  Column('asmt_claim_2_perf_lvl', SmallInteger, nullable=True),
                                  Column('asmt_claim_3_score', SmallInteger, nullable=True),
                                  Column('asmt_claim_3_score_range_min', SmallInteger, nullable=True),
                                  Column('asmt_claim_3_score_range_max', SmallInteger, nullable=True),
                                  Column('asmt_claim_3_perf_lvl', SmallInteger, nullable=True),
                                  Column('asmt_claim_4_score', SmallInteger, nullable=True),
                                  Column('asmt_claim_4_score_range_min', SmallInteger, nullable=True),
                                  Column('asmt_claim_4_score_range_max', SmallInteger, nullable=True),
                                  Column('asmt_claim_4_perf_lvl', SmallInteger, nullable=True),
                                  Column('sex', String(10), nullable=False),
                                  Column('dmg_eth_derived', SmallInteger, nullable=True),
                                  Column('dmg_eth_hsp', Boolean, nullable=True),
                                  Column('dmg_eth_ami', Boolean, nullable=True),
                                  Column('dmg_eth_asn', Boolean, nullable=True),
                                  Column('dmg_eth_blk', Boolean, nullable=True),
                                  Column('dmg_eth_pcf', Boolean, nullable=True),
                                  Column('dmg_eth_wht', Boolean, nullable=True),
                                  Column('dmg_prg_iep', Boolean, nullable=True),
                                  Column('dmg_prg_lep', Boolean, nullable=True),
                                  Column('dmg_prg_504', Boolean, nullable=True),
                                  Column('dmg_prg_tt1', Boolean, nullable=True),
                                  Column('acc_asl_video_embed', SmallInteger, nullable=False),
                                  Column('acc_asl_human_nonembed', SmallInteger, nullable=False),
                                  Column('acc_braile_embed', SmallInteger, nullable=False),
                                  Column('acc_closed_captioning_embed', SmallInteger, nullable=False),
                                  Column('acc_text_to_speech_embed', SmallInteger, nullable=False),
                                  Column('acc_abacus_nonembed', SmallInteger, nullable=False),
                                  Column('acc_alternate_response_options_nonembed', SmallInteger, nullable=False),
                                  Column('acc_calculator_nonembed', SmallInteger, nullable=False),
                                  Column('acc_multiplication_table_nonembed', SmallInteger, nullable=False),
                                  Column('acc_print_on_demand_nonembed', SmallInteger, nullable=False),
                                  Column('acc_read_aloud_nonembed', SmallInteger, nullable=False),
                                  Column('acc_scribe_nonembed', SmallInteger, nullable=False),
                                  Column('acc_speech_to_text_nonembed', SmallInteger, nullable=False),
                                  Column('acc_streamline_mode', SmallInteger, nullable=False),
                                  MetaColumn('from_date', String(8), nullable=False),
                                  MetaColumn('to_date', String(8), nullable=True),
                                  MetaColumn('rec_status', String(1), nullable=False),
                                  MetaColumn('batch_guid', String(50), nullable=False),
                                  )

    Index('fact_asmt_outcome_vw_student_idx', assessment_outcome_vw.c.student_guid, assessment_outcome_vw.c.asmt_guid, unique=False)
    Index('fact_asmt_outcome_vw_asmt_subj_typ_idx', assessment_outcome_vw.c.student_guid, assessment_outcome_vw.c.asmt_subject, assessment_outcome_vw.c.asmt_type, unique=False)
    # Filtering related indices
    Index('fact_asmt_outcome_vw_grade_idx', assessment_outcome_vw.c.asmt_grade, unique=False)
    Index('fact_asmt_outcome_vw_eth_derived_idx', assessment_outcome_vw.c.dmg_eth_derived, unique=False)
    Index('fact_asmt_outcome_vw_lep_idx', assessment_outcome_vw.c.dmg_prg_lep, unique=False)
    Index('fact_asmt_outcome_vw_504_idx', assessment_outcome_vw.c.dmg_prg_504, unique=False)
    Index('fact_asmt_outcome_vw_tt1_idx', assessment_outcome_vw.c.dmg_prg_tt1, unique=False)
    Index('fact_asmt_outcome_vw_iep_idx', assessment_outcome_vw.c.dmg_prg_iep, unique=False)
    Index('fact_asmt_outcome_vw_sex_idx', assessment_outcome_vw.c.sex, unique=False)
    Index('fact_asmt_outcome_vw_cpop_stateview_idx', assessment_outcome_vw.c.state_code, assessment_outcome_vw.c.asmt_type, assessment_outcome_vw.c.rec_status, assessment_outcome_vw.c.asmt_year, assessment_outcome_vw.c.inst_hier_rec_id, assessment_outcome_vw.c.asmt_subject, assessment_outcome_vw.c.asmt_perf_lvl, assessment_outcome_vw.c.district_guid, unique=False)
    Index('fact_asmt_outcome_vw_cpop_not_stated_count_idx', assessment_outcome_vw.c.rec_status, assessment_outcome_vw.c.asmt_type, assessment_outcome_vw.c.asmt_year, assessment_outcome_vw.c.state_code, assessment_outcome_vw.c.district_guid, assessment_outcome_vw.c.school_guid, assessment_outcome_vw.c.dmg_prg_iep, assessment_outcome_vw.c.dmg_prg_504, assessment_outcome_vw.c.dmg_prg_lep, assessment_outcome_vw.c.asmt_grade, assessment_outcome_vw.c.dmg_eth_derived, assessment_outcome_vw.c.sex, unique=False)

    assessment_outcome = Table('fact_asmt_outcome', metadata,
                               Column('asmt_outcome_rec_id', BigInteger, primary_key=True),
                               Column('asmt_rec_id', BigInteger, ForeignKey(assessment.c.asmt_rec_id), nullable=False),
                               Column('student_rec_id', BigInteger, ForeignKey(students.c.student_rec_id), nullable=False),
                               Column('inst_hier_rec_id', BigInteger, ForeignKey(instit_hier.c.inst_hier_rec_id), nullable=False),
                               Column('asmt_guid', String(50), nullable=False, info={'natural_key': True}),
                               Column('student_guid', String(50), nullable=False, info={'natural_key': True}),
                               Column('state_code', String(2), nullable=False),
                               Column('district_guid', String(50), nullable=False),
                               Column('school_guid', String(50), nullable=False),
                               Column('where_taken_id', String(50), nullable=True),  # external id if provided
                               Column('where_taken_name', String(60), nullable=True),
                               Column('asmt_grade', String(10), nullable=False),
                               Column('enrl_grade', String(10), nullable=False),
                               Column('group_1_id', String(50), nullable=True),
                               Column('group_1_text', String(60), nullable=True),
                               Column('group_2_id', String(50), nullable=True),
                               Column('group_2_text', String(60), nullable=True),
                               Column('date_taken', String(8), nullable=False),
                               Column('date_taken_day', SmallInteger, nullable=False),
                               Column('date_taken_month', SmallInteger, nullable=False),
                               Column('date_taken_year', SmallInteger, nullable=False),
                               Column('asmt_score', SmallInteger, nullable=False),
                               Column('asmt_score_range_min', SmallInteger, nullable=False),
                               Column('asmt_score_range_max', SmallInteger, nullable=False),
                               Column('asmt_perf_lvl', SmallInteger, nullable=False),
                               Column('asmt_claim_1_score', SmallInteger, nullable=True),
                               Column('asmt_claim_1_score_range_min', SmallInteger, nullable=True),
                               Column('asmt_claim_1_score_range_max', SmallInteger, nullable=True),
                               Column('asmt_claim_1_perf_lvl', SmallInteger, nullable=True),
                               Column('asmt_claim_2_score', SmallInteger, nullable=True),
                               Column('asmt_claim_2_score_range_min', SmallInteger, nullable=True),
                               Column('asmt_claim_2_score_range_max', SmallInteger, nullable=True),
                               Column('asmt_claim_2_perf_lvl', SmallInteger, nullable=True),
                               Column('asmt_claim_3_score', SmallInteger, nullable=True),
                               Column('asmt_claim_3_score_range_min', SmallInteger, nullable=True),
                               Column('asmt_claim_3_score_range_max', SmallInteger, nullable=True),
                               Column('asmt_claim_3_perf_lvl', SmallInteger, nullable=True),
                               Column('asmt_claim_4_score', SmallInteger, nullable=True),
                               Column('asmt_claim_4_score_range_min', SmallInteger, nullable=True),
                               Column('asmt_claim_4_score_range_max', SmallInteger, nullable=True),
                               Column('asmt_claim_4_perf_lvl', SmallInteger, nullable=True),
                               Column('acc_asl_video_embed', SmallInteger, nullable=False),
                               Column('acc_asl_human_nonembed', SmallInteger, nullable=False),
                               Column('acc_braile_embed', SmallInteger, nullable=False),
                               Column('acc_closed_captioning_embed', SmallInteger, nullable=False),
                               Column('acc_text_to_speech_embed', SmallInteger, nullable=False),
                               Column('acc_abacus_nonembed', SmallInteger, nullable=False),
                               Column('acc_alternate_response_options_nonembed', SmallInteger, nullable=False),
                               Column('acc_calculator_nonembed', SmallInteger, nullable=False),
                               Column('acc_multiplication_table_nonembed', SmallInteger, nullable=False),
                               Column('acc_print_on_demand_nonembed', SmallInteger, nullable=False),
                               Column('acc_read_aloud_nonembed', SmallInteger, nullable=False),
                               Column('acc_scribe_nonembed', SmallInteger, nullable=False),
                               Column('acc_speech_to_text_nonembed', SmallInteger, nullable=False),
                               Column('acc_streamline_mode', SmallInteger, nullable=False),
                               MetaColumn('from_date', String(8), nullable=False),
                               MetaColumn('to_date', String(8), nullable=True),
                               MetaColumn('rec_status', String(2), nullable=False),
                               MetaColumn('batch_guid', String(50), nullable=False),
                               )

    Index('fact_asmt_outcome_student_idx', assessment_outcome.c.student_guid, assessment_outcome.c.asmt_guid, unique=False)

    student_registration = Table('student_reg', metadata,
                                 Column('student_reg_rec_id', BigInteger, primary_key=True),
                                 Column('state_code', String(2), nullable=False),
                                 Column('state_name', String(50), nullable=False),
                                 Column('district_guid', String(50), nullable=False),
                                 Column('district_name', String(60), nullable=False),
                                 Column('school_guid', String(50), nullable=False),
                                 Column('school_name', String(60), nullable=False),
                                 Column('student_guid', String(50), nullable=False),
                                 Column('external_student_ssid', String(50), nullable=False),
                                 Column('first_name', String(35), nullable=True),
                                 Column('middle_name', String(35), nullable=True),
                                 Column('last_name', String(35), nullable=True),
                                 Column('birthdate', String(10), nullable=True),
                                 Column('sex', String(10), nullable=False),
                                 Column('enrl_grade', String(10), nullable=False),
                                 Column('dmg_eth_hsp', Boolean, nullable=True),
                                 Column('dmg_eth_ami', Boolean, nullable=True),
                                 Column('dmg_eth_asn', Boolean, nullable=True),
                                 Column('dmg_eth_blk', Boolean, nullable=True),
                                 Column('dmg_eth_pcf', Boolean, nullable=True),
                                 Column('dmg_eth_wht', Boolean, nullable=True),
                                 Column('dmg_multi_race', Boolean, nullable=True),
                                 Column('dmg_prg_iep', Boolean, nullable=True),
                                 Column('dmg_prg_lep', Boolean, nullable=True),
                                 Column('dmg_prg_504', Boolean, nullable=True),
                                 Column('dmg_sts_ecd', Boolean, nullable=True),
                                 Column('dmg_sts_mig', Boolean, nullable=True),
                                 Column('confirm_code', String(50), nullable=False),
                                 Column('language_code', String(3), nullable=True),
                                 Column('eng_prof_lvl', String(20), nullable=True),
                                 Column('us_school_entry_date', String(10), nullable=True),
                                 Column('lep_entry_date', String(10), nullable=True),
                                 Column('lep_exit_date', String(10), nullable=True),
                                 Column('t3_program_type', String(27), nullable=True),
                                 Column('prim_disability_type', String(3), nullable=True),
                                 Column('student_reg_guid', String(50), nullable=False),
                                 Column('academic_year', SmallInteger, nullable=False),
                                 Column('extract_date', String(10), nullable=False),
                                 Column('reg_system_id', String(50), nullable=False),
                                 Column('batch_guid', String(50), nullable=False),
                                 )
    Index('student_reg_year_system_idx', student_registration.c.academic_year, student_registration.c.reg_system_id, unique=False)
    Index('student_reg_guid_idx', student_registration.c.student_guid, unique=False)

    return metadata
