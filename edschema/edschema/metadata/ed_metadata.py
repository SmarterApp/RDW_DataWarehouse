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
                        MetaColumn('batch_guid', String(50), nullable=True),
                        Column('state_name', String(32), nullable=False),
                        Column('state_code', String(2), nullable=False, info={'natural_key': True}),
                        Column('district_guid', String(50), nullable=False, info={'natural_key': True}),
                        Column('district_name', String(256), nullable=False),
                        Column('school_guid', String(50), nullable=False, info={'natural_key': True}),
                        Column('school_name', String(256), nullable=False),
                        Column('school_category', String(20), nullable=False),
                        MetaColumn('from_date', String(8), nullable=False),
                        MetaColumn('to_date', String(8), nullable=True),
                        MetaColumn('rec_status', String(1), nullable=False),
                        )

    Index('dim_inst_hier_idx', instit_hier.c.inst_hier_rec_id, unique=True)
    Index('dim_inst_hier_codex', instit_hier.c.state_code, instit_hier.c.district_guid, instit_hier.c.school_guid, unique=False)

    sections = Table('dim_section', metadata,
                     Column('section_rec_id', BigInteger, primary_key=True),
                     MetaColumn('batch_guid', String(50), nullable=True),
                     Column('section_guid', String(50), nullable=False, info={'natural_key': True}),
                     Column('section_name', String(256), nullable=False),
                     Column('grade', String(10), nullable=False),
                     Column('class_name', String(256), nullable=False),
                     Column('subject_name', String(256), nullable=False),
                     Column('state_code', String(2), nullable=False),
                     Column('district_guid', String(50), nullable=False),
                     Column('school_guid', String(50), nullable=False),
                     MetaColumn('from_date', String(8), nullable=False),
                     MetaColumn('to_date', String(8), nullable=True),
                     MetaColumn('rec_status', String(1), nullable=False),
                     )

    Index('dim_section_idx', sections.c.section_rec_id, unique=True)
    Index('dim_section_current_idx', sections.c.section_guid, sections.c.subject_name, sections.c.grade, sections.c.rec_status, unique=False)
    Index('dim_section_dim_inst_hier_idx', sections.c.state_code, sections.c.district_guid, sections.c.school_guid, sections.c.from_date, sections.c.to_date, unique=False)

    # NB! Figure out uniques in dim_student
    students = Table('dim_student', metadata,
                     Column('student_rec_id', BigInteger, primary_key=True),
                     MetaColumn('batch_guid', String(50), nullable=True),
                     Column('student_guid', String(50), nullable=False, info={'natural_key': True}),
                     #Column('external_student_id', String(40), nullable=True),  # TODO: Add this field
                     Column('first_name', String(256), nullable=False),
                     Column('middle_name', String(256), nullable=True),
                     Column('last_name', String(256), nullable=False),
                     Column('address_1', String(256), nullable=True),
                     Column('address_2', String(256), nullable=True),
                     Column('city', String(100), nullable=True),
                     Column('zip_code', String(5), nullable=True),
                     Column('gender', String(10), nullable=True),
                     Column('email', String(256), nullable=True),
                     Column('dob', String(8), nullable=False),
                     Column('section_guid', String(50), nullable=False),
                     Column('grade', String(10), nullable=False),  # TODO: Delete this field
                     Column('state_code', String(2), nullable=False),
                     Column('district_guid', String(50), nullable=False),
                     Column('school_guid', String(50), nullable=False),
                     MetaColumn('from_date', String(8), nullable=False),
                     MetaColumn('to_date', String(8), nullable=True),
                     MetaColumn('rec_status', String(1), nullable=False),
                     )

    Index('dim_student_pk', students.c.student_rec_id, unique=True)
    Index('dim_student_idx', students.c.student_guid, unique=False)

    student_demographics = Table('dim_student_demographics', metadata,
                                 Column('student_demographic_rec_id', BigInteger, primary_key=True),
                                 MetaColumn('batch_guid', String(50), nullable=True),
                                 Column('student_guid', String(50), nullable=False, info={'natural_key': True}),
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
                                 Column('dmg_eth_derived', SmallInteger, nullable=True),
                                 MetaColumn('from_date', String(8), nullable=False),
                                 MetaColumn('to_date', String(8), nullable=True),
                                 MetaColumn('rec_status', String(2), nullable=False)
                                 )

    Index('dim_student_demographics_idx', student_demographics.c.student_guid, unique=False)

    assessment = Table('dim_asmt', metadata,
                       Column('asmt_rec_id', BigInteger, primary_key=True),
                       MetaColumn('batch_guid', String(50), nullable=True),
                       Column('asmt_guid', String(50), nullable=False, info={'natural_key': True}),
                       Column('asmt_type', String(32), nullable=False),
                       Column('asmt_period', String(32), nullable=False),
                       Column('asmt_period_year', SmallInteger, nullable=False),
                       Column('asmt_version', String(16), nullable=False),
                       Column('asmt_subject', String(100)),
                       Column('asmt_claim_1_name', String(256), nullable=True),
                       Column('asmt_claim_2_name', String(256), nullable=True),
                       Column('asmt_claim_3_name', String(256), nullable=True),
                       Column('asmt_claim_4_name', String(256), nullable=True),
                       Column('asmt_perf_lvl_name_1', String(256), nullable=True),
                       Column('asmt_perf_lvl_name_2', String(256), nullable=True),
                       Column('asmt_perf_lvl_name_3', String(256), nullable=True),
                       Column('asmt_perf_lvl_name_4', String(256), nullable=True),
                       Column('asmt_perf_lvl_name_5', String(256), nullable=True),
                       Column('asmt_claim_perf_lvl_name_1', String(256), nullable=True),
                       Column('asmt_claim_perf_lvl_name_2', String(256), nullable=True),
                       Column('asmt_claim_perf_lvl_name_3', String(256), nullable=True),
                       Column('asmt_score_min', SmallInteger, nullable=True),
                       Column('asmt_score_max', SmallInteger, nullable=True),
                       Column('asmt_claim_1_score_min', SmallInteger, nullable=True),
                       Column('asmt_claim_1_score_max', SmallInteger, nullable=True),
                       Column('asmt_claim_1_score_weight', Float, nullable=True),
                       Column('asmt_claim_2_score_min', SmallInteger, nullable=True),
                       Column('asmt_claim_2_score_max', SmallInteger, nullable=True),
                       Column('asmt_claim_2_score_weight', Float, nullable=True),
                       Column('asmt_claim_3_score_min', SmallInteger, nullable=True),
                       Column('asmt_claim_3_score_max', SmallInteger, nullable=True),
                       Column('asmt_claim_3_score_weight', Float, nullable=True),
                       Column('asmt_claim_4_score_min', SmallInteger, nullable=True),
                       Column('asmt_claim_4_score_max', SmallInteger, nullable=True),
                       Column('asmt_claim_4_score_weight', Float, nullable=True),
                       Column('asmt_cut_point_1', SmallInteger, nullable=True),
                       Column('asmt_cut_point_2', SmallInteger, nullable=True),
                       Column('asmt_cut_point_3', SmallInteger, nullable=True),
                       Column('asmt_cut_point_4', SmallInteger, nullable=True),
                       MetaColumn('from_date', String(8), nullable=False),
                       MetaColumn('to_date', String(8), nullable=True),
                       MetaColumn('effective_date', String(8), nullable=True),
                       MetaColumn('rec_status', String(1), nullable=False),
                       )

    Index('dim_asmt_rec_idx', assessment.c.asmt_rec_id, unique=True)
    Index('dim_asmt_guid_idx', assessment.c.asmt_guid, unique=False)
    Index('dim_asmt_id_typex', assessment.c.asmt_rec_id, assessment.c.asmt_type, unique=False)

    custom_metadata = Table('custom_metadata', metadata,
                            Column('state_code', String(2), nullable=False),
                            Column('asmt_subject', String(100), nullable=False),
                            Column('asmt_custom_metadata', Text, nullable=True)
                            )
    Index('custom_metadata_id_idx', custom_metadata.c.state_code, custom_metadata.c.asmt_subject, unique=True)

    assessment_outcome = Table('fact_asmt_outcome', metadata,
                               Column('asmnt_outcome_rec_id', BigInteger, primary_key=True),
                               MetaColumn('batch_guid', String(50), nullable=True),
                               Column('asmt_rec_id', BigInteger, ForeignKey(assessment.c.asmt_rec_id), nullable=False),
                               Column('asmt_guid', String(50), nullable=False, info={'natural_key': True}),
                               Column('student_rec_id', BigInteger, ForeignKey(students.c.student_rec_id), nullable=False),
                               Column('student_guid', String(50), nullable=False, info={'natural_key': True}),
                               Column('external_student_id', String(40), nullable=True),
                               Column('state_code', String(2), nullable=False),
                               Column('district_guid', String(50), nullable=False),
                               Column('school_guid', String(50), nullable=False),
                               Column('section_guid', String(50), nullable=False),  # TODO: Delete this field
                               Column('inst_hier_rec_id', BigInteger, ForeignKey(instit_hier.c.inst_hier_rec_id), nullable=False),
                               Column('section_rec_id', BigInteger, nullable=False),  # this column will be dropped soon
                               Column('where_taken_id', String(50), nullable=True),  # external id if provided
                               Column('where_taken_name', String(256)),
                               Column('asmt_grade', String(10), nullable=False),
                               Column('enrl_grade', String(10), nullable=False),
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
                               MetaColumn('rec_status', String(1), nullable=False),
                               MetaColumn('from_date', String(8), nullable=False),
                               MetaColumn('to_date', String(8), nullable=True),
                               # Add 4 assessment columns
                               Column('asmt_type', String(32), nullable=False),
                               Column('asmt_year', SmallInteger, nullable=False),
                               Column('asmt_subject', String(100)),
                               Column('gender', String(10), nullable=True),
                               # Add 10 demographic columns
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
                               Column('dmg_eth_derived', SmallInteger, nullable=True),
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
                               )

    Index('fact_asmt_outcome_hier_keyx', assessment_outcome.c.state_code, assessment_outcome.c.rec_status, assessment_outcome.c.asmt_type, assessment_outcome.c.district_guid, assessment_outcome.c.school_guid, unique=False)
    Index('fact_asmt_outcome_district_idx', assessment_outcome.c.district_guid, assessment_outcome.c.rec_status, unique=False)
    Index('fact_asmt_outcome_school_grade_idx', assessment_outcome.c.school_guid, assessment_outcome.c.district_guid, assessment_outcome.c.asmt_grade, assessment_outcome.c.rec_status, unique=False)
    Index('fact_asmt_outcome_student_idx', assessment_outcome.c.student_guid, assessment_outcome.c.asmt_guid, unique=False)
    # Filtering related indices
    Index('fact_asmt_outcome_grade', assessment_outcome.c.state_code, assessment_outcome.c.rec_status, assessment_outcome.c.asmt_type, assessment_outcome.c.asmt_grade, unique=False)
    Index('fact_asmt_outcome_lep', assessment_outcome.c.state_code, assessment_outcome.c.rec_status, assessment_outcome.c.asmt_type, assessment_outcome.c.dmg_prg_lep, unique=False)
    Index('fact_asmt_outcome_504', assessment_outcome.c.state_code, assessment_outcome.c.rec_status, assessment_outcome.c.asmt_type, assessment_outcome.c.dmg_prg_504, unique=False)
    Index('fact_asmt_outcome_tt1', assessment_outcome.c.state_code, assessment_outcome.c.rec_status, assessment_outcome.c.asmt_type, assessment_outcome.c.dmg_prg_tt1, unique=False)
    Index('fact_asmt_outcome_iep', assessment_outcome.c.state_code, assessment_outcome.c.rec_status, assessment_outcome.c.asmt_type, assessment_outcome.c.dmg_prg_iep, unique=False)
    Index('fact_asmt_outcome_gender', assessment_outcome.c.state_code, assessment_outcome.c.rec_status, assessment_outcome.c.asmt_type, assessment_outcome.c.gender, unique=False)

    assessment_outcome_primary = Table('fact_asmt_outcome_primary', metadata,
                                       Column('asmnt_outcome_primary_rec_id', BigInteger, primary_key=True),
                                       Column('asmt_rec_id', BigInteger, ForeignKey(assessment.c.asmt_rec_id), nullable=False),
                                       Column('student_rec_id', BigInteger, ForeignKey(students.c.student_rec_id), nullable=False),
                                       Column('inst_hier_rec_id', BigInteger, ForeignKey(instit_hier.c.inst_hier_rec_id), nullable=False),
                                       Column('asmt_guid', String(50), nullable=False, info={'natural_key': True}),
                                       Column('student_guid', String(50), nullable=False, info={'natural_key': True}),
                                       Column('state_code', String(2), nullable=False),
                                       Column('district_guid', String(50), nullable=False),
                                       Column('school_guid', String(50), nullable=False),
                                       Column('where_taken_id', String(50), nullable=True),  # external id if provided
                                       Column('where_taken_name', String(256)),
                                       Column('asmt_grade', String(10), nullable=False),
                                       Column('enrl_grade', String(10), nullable=False),
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
                                       Column('rec_status', String(2), nullable=False),
                                       Column('from_date', String(8), nullable=False),
                                       Column('to_date', String(8), nullable=True),
                                       Column('batch_guid', String(50), nullable=True),
                                       )

    Index('fact_asmt_outcome_primary_student_idx', assessment_outcome_primary.c.student_guid, assessment_outcome_primary.c.asmt_guid, unique=False)

    student_registration = Table('student_reg', metadata,
                                 Column('student_reg_rec_id', BigInteger, primary_key=True),
                                 Column('batch_guid', String(36), nullable=False),
                                 Column('state_name', String(50), nullable=False),
                                 Column('state_code', String(2), nullable=False),
                                 Column('district_guid', String(30), nullable=False),
                                 Column('district_name', String(60), nullable=False),
                                 Column('school_guid', String(30), nullable=False),
                                 Column('school_name', String(60), nullable=False),
                                 Column('student_guid', String(30), nullable=False),
                                 Column('external_student_ssid', String(50), nullable=False),
                                 Column('student_first_name', String(35), nullable=True),
                                 Column('student_middle_name', String(35), nullable=True),
                                 Column('student_last_name', String(35), nullable=True),
                                 Column('gender', String(6), nullable=False),
                                 Column('student_dob', String(10), nullable=True),
                                 Column('enrl_grade', String(10), nullable=False),
                                 Column('dmg_eth_hsp', Boolean, nullable=False),
                                 Column('dmg_eth_ami', Boolean, nullable=False),
                                 Column('dmg_eth_asn', Boolean, nullable=False),
                                 Column('dmg_eth_blk', Boolean, nullable=False),
                                 Column('dmg_eth_pcf', Boolean, nullable=False),
                                 Column('dmg_eth_wht', Boolean, nullable=False),
                                 Column('dmg_prg_iep', Boolean, nullable=False),
                                 Column('dmg_prg_lep', Boolean, nullable=False),
                                 Column('dmg_prg_504', Boolean, nullable=True),
                                 Column('dmg_sts_ecd', Boolean, nullable=False),
                                 Column('dmg_sts_mig', Boolean, nullable=True),
                                 Column('dmg_multi_race', Boolean, nullable=False),
                                 Column('confirm_code', String(35), nullable=False),
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
                                 )
    Index('student_reg_system_id_yearx', student_registration.c.reg_system_id, student_registration.c.academic_year, unique=False)
    Index('student_reg_year_student_id', student_registration.c.academic_year, student_registration.c.student_guid, unique=False)

    return metadata
