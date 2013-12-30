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
__updated__ = '2013-02-02'


def generate_ed_metadata(schema_name=None, bind=None):

    metadata = MetaData(schema=schema_name, bind=bind)

    # Two-letter state - some countries have 3 or more, but two will do for US
    instit_hier = Table('dim_inst_hier', metadata,
                        Column('inst_hier_rec_id', BigInteger, primary_key=True),
                        Column('state_name', String(32), nullable=False),
                        Column('state_code', String(2), nullable=False),
                        Column('district_guid', String(50), nullable=False),
                        Column('district_name', String(256), nullable=False),
                        Column('school_guid', String(50), nullable=False),
                        Column('school_name', String(256), nullable=False),
                        Column('school_category', String(20), nullable=False),
                        Column('from_date', String(8), nullable=False),
                        Column('to_date', String(8), nullable=True),
                        Column('most_recent', Boolean),
                        )

    Index('dim_inst_hier_idx', instit_hier.c.inst_hier_rec_id, unique=True)
    Index('dim_inst_hier_codex', instit_hier.c.state_code, instit_hier.c.district_guid, instit_hier.c.school_guid, unique=False)

    sections = Table('dim_section', metadata,
                     Column('section_rec_id', BigInteger, primary_key=True),
                     Column('section_guid', String(50), nullable=False),
                     Column('section_name', String(256), nullable=False),
                     Column('grade', String(10), nullable=False),
                     Column('class_name', String(256), nullable=False),
                     Column('subject_name', String(256), nullable=False),
                     Column('state_code', String(2), nullable=False),
                     Column('district_guid', String(50), nullable=False),
                     Column('school_guid', String(50), nullable=False),
                     Column('from_date', String(8), nullable=False),
                     Column('to_date', String(8), nullable=True),
                     Column('most_recent', Boolean),
                     )

    Index('dim_section_idx', sections.c.section_rec_id, unique=True)
    Index('dim_section_current_idx', sections.c.section_guid, sections.c.subject_name, sections.c.grade, sections.c.most_recent, unique=False)
    Index('dim_section_dim_inst_hier_idx', sections.c.state_code, sections.c.district_guid, sections.c.school_guid, sections.c.from_date, sections.c.to_date, unique=False)

    # NB! Figure out uniques in dim_student
    students = Table('dim_student', metadata,
                     Column('student_rec_id', BigInteger, primary_key=True),
                     Column('student_guid', String(50), nullable=False),
                     Column('first_name', String(256), nullable=False),
                     Column('middle_name', String(256), nullable=True),
                     Column('last_name', String(256), nullable=False),
                     Column('address_1', String(256), nullable=False),
                     Column('address_2', String(256), nullable=True),
                     Column('city', String(100), nullable=False),
                     Column('zip_code', String(5), nullable=False),
                     Column('gender', String(10), nullable=True),
                     Column('email', String(256), nullable=False),
                     Column('dob', String(8), nullable=False),
                     Column('section_guid', String(50), nullable=False),
                     Column('grade', String(10), nullable=False),
                     Column('state_code', String(2), nullable=False),
                     Column('district_guid', String(50), nullable=False),
                     Column('school_guid', String(50), nullable=False),
                     Column('from_date', String(8), nullable=False),
                     Column('to_date', String(8), nullable=True),
                     Column('most_recent', Boolean),
                     )

    Index('dim_student_idx', students.c.student_guid, students.c.most_recent, unique=False)

    external_user_student = Table('external_user_student_rel', metadata,
                                  Column('external_user_student_guid', String(50), primary_key=True),
                                  Column('external_user_guid', String(256), nullable=False),
                                  Column('student_guid', String(50), nullable=False),  # NB! Figure out uniques in dim_student
                                  Column('from_date', String(8), nullable=False),
                                  Column('to_date', String(8), nullable=True),
                                  )

    Index('dim_external_user_student_idx', external_user_student.c.external_user_student_guid, unique=True)
    Index('dim_external_user_student_student_x', external_user_student.c.external_user_guid, external_user_student.c.student_guid, unique=True)

    user_mapping = Table('user_mapping', metadata,
                         Column('user_id', String(50), primary_key=True),
                         Column('guid', String(50), nullable=False),
                         )
    Index('user_mapping_idx', user_mapping.c.user_id, unique=True)

    assessment = Table('dim_asmt', metadata,
                       Column('asmt_rec_id', BigInteger, primary_key=True),
                       Column('asmt_guid', String(50), nullable=False),
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
                       Column('from_date', String(8), nullable=False),
                       Column('to_date', String(8), nullable=True),
                       Column('most_recent', Boolean),
                       )

    Index('dim_asmt_rec_idx', assessment.c.asmt_rec_id, unique=True)
    Index('dim_asmt_id_typex', assessment.c.asmt_rec_id, assessment.c.asmt_type, assessment.c.most_recent, unique=False)

    custom_metadata = Table('custom_metadata', metadata,
                            Column('state_code', String(2), nullable=False),
                            Column('asmt_subject', String(100), nullable=False),
                            Column('asmt_custom_metadata', Text, nullable=True)
                            )
    Index('custom_metadata_id_idx', custom_metadata.c.state_code, custom_metadata.c.asmt_subject, unique=True)

    assessment_outcome = Table('fact_asmt_outcome', metadata,
                               Column('asmnt_outcome_rec_id', BigInteger, primary_key=True),
                               Column('asmt_rec_id', BigInteger, ForeignKey(assessment.c.asmt_rec_id), nullable=False),
                               Column('student_guid', String(50), nullable=False),
                               Column('state_code', String(2), nullable=False),
                               Column('district_guid', String(50), nullable=False),
                               Column('school_guid', String(50), nullable=False),
                               Column('section_guid', String(50), nullable=False),
                               Column('inst_hier_rec_id', BigInteger, ForeignKey(instit_hier.c.inst_hier_rec_id), nullable=False),
                               Column('section_rec_id', BigInteger, ForeignKey(sections.c.section_rec_id), nullable=False),
                               Column('where_taken_id', String(50), nullable=True),  # external id if provided
                               Column('where_taken_name', String(256), primary_key=True),
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
                               Column('status', String(2), nullable=False),
                               Column('most_recent', Boolean),
                               Column('batch_guid', String(50), nullable=True),
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
                               )

    Index('fact_asmt_outcome_idx', assessment_outcome.c.asmnt_outcome_rec_id, unique=True)
    Index('fact_asmt_outcome_hier_keyx', assessment_outcome.c.state_code, assessment_outcome.c.most_recent, assessment_outcome.c.asmt_type, assessment_outcome.c.district_guid, assessment_outcome.c.school_guid, unique=False)
    Index('fact_asmt_outcome_district_idx', assessment_outcome.c.district_guid, assessment_outcome.c.most_recent, unique=False)
    Index('fact_asmt_outcome_school_grade_idx', assessment_outcome.c.school_guid, assessment_outcome.c.district_guid, assessment_outcome.c.asmt_grade, assessment_outcome.c.most_recent, unique=False)
    Index('fact_asmt_outcome_student_idx', assessment_outcome.c.student_guid, assessment_outcome.c.most_recent, unique=False)
    # Filtering related indices
    Index('fact_asmt_outcome_grade', assessment_outcome.c.state_code, assessment_outcome.c.most_recent, assessment_outcome.c.asmt_type, assessment_outcome.c.asmt_grade, unique=False)
    Index('fact_asmt_outcome_lep', assessment_outcome.c.state_code, assessment_outcome.c.most_recent, assessment_outcome.c.asmt_type, assessment_outcome.c.dmg_prg_lep, unique=False)
    Index('fact_asmt_outcome_504', assessment_outcome.c.state_code, assessment_outcome.c.most_recent, assessment_outcome.c.asmt_type, assessment_outcome.c.dmg_prg_504, unique=False)
    Index('fact_asmt_outcome_tt1', assessment_outcome.c.state_code, assessment_outcome.c.most_recent, assessment_outcome.c.asmt_type, assessment_outcome.c.dmg_prg_tt1, unique=False)
    Index('fact_asmt_outcome_iep', assessment_outcome.c.state_code, assessment_outcome.c.most_recent, assessment_outcome.c.asmt_type, assessment_outcome.c.dmg_prg_iep, unique=False)
    Index('fact_asmt_outcome_gender', assessment_outcome.c.state_code, assessment_outcome.c.most_recent, assessment_outcome.c.asmt_type, assessment_outcome.c.gender, unique=False)

    return metadata
