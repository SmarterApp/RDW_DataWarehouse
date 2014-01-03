'''
Authoratative Definitions for UDL's required tables

UDL_METADATA contains all tables, sequences that are used in UDL system

Several methods are provided to create/drop tables/sequences/extensions/foreign data wrapper servers
in postgres database.

Main Method: setup_udl2_schema(conf)
Main method: teardown_udl2_schema(conf)

conf is defined in udl2_conf.py, default is under /opt/wgen/edware-udl/etc/udl2_conf.py

Created on May 10, 2013

@author: ejen
'''
from sqlalchemy.schema import (MetaData, CreateSchema, CreateSequence, ForeignKeyConstraint, UniqueConstraint)
from sqlalchemy import Table, Column, Sequence
from sqlalchemy.types import *
from sqlalchemy.sql.expression import text
import imp
import argparse
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from udl2_util.database_util import connect_db, execute_queries
from udl2.populate_ref_info import populate_ref_column_map, populate_stored_proc
from config import ref_table_data

#
# UDL_METADATA stores all udl2 related database objects, which includes staging tables and table-independent sequeuces
#

UDL_METADATA = {
    #
    # We use a list of columns for table.
    # for each column ('column name', 'is a primary key', 'type', 'default value', 'Nullalbe', 'Comments')
    #
    'TABLES': {
        'STG_MOCK_LOAD': {
            'columns': [
                ('record_sid', True, 'bigserial', '', False, "Non Sequential UUID"),
                ('guid_batch', False, 'varchar(256)', '', False, "Batch ID which caused the record insert"),
                ('substr_test', False, 'varchar(256)', '', False, "mock data for test type conversion during staging to integration"),
                ('number_test', False, 'varchar(256)', '', False, "mock data for test type conversion during staging to integration"),
            ],
            'indexes': [],
            'keys': {},
        },
        'INT_MOCK_LOAD': {
            'columns': [
                ('record_sid', True, 'bigserial', '', False, "Non Sequential UUID"),
                ('guid_batch', False, 'varchar(256)', '', False, "Batch ID which caused the record insert"),
                ('substr_test', False, 'varchar(256)', '', False, "mock data for test type conversion during staging to integration"),
                ('number_test', False, 'varchar(256)', '', False, "mock data for test type conversion during staging to integration"),
            ],
            'indexes': [],
            'keys': {},
        },
        'UDL_BATCH': {
            'columns': [
                ('batch_sid', True, 'bigserial', '', False, "Sequential Auto-increment"),
                ('guid_batch', False, 'varchar(256)', '', False, "Batch guid which caused the record insert"),
                ('load_type', False, 'varchar(50)', '', True, ""),
                ('working_schema', False, 'varchar(50)', '', True, ""),
                ('udl_phase', False, 'varchar(256)', '', True, ""),
                ('udl_phase_step', False, 'varchar(50)', '', True, ""),
                ('udl_phase_step_status', False, 'varchar(50)', '', True, ""),
                ('error_desc', False, 'text', '', True, ""),
                ('stack_trace', False, 'text', '', True, ""),
                ('udl_leaf', False, 'bool', '', True, ""),
                ('size_records', False, 'bigint', '', True, ""),
                ('size_units', False, 'bigint', '', True, ""),
                ('start_timestamp', False, 'timestamp', 'now()', True, ""),
                ('end_timestamp', False, 'timestamp', 'now()', True, ""),
                ('duration', False, 'interval', '', True, ""),
                ('time_for_one_million_records', False, 'time', '', True, ""),
                ('records_per_hour', False, 'bigint', '', True, ""),
                ('task_id', False, 'varchar(256)', '', True, ""),
                ('task_status_url', False, 'varchar(256)', '', True, ""),
                ('user_sid', False, 'bigint', '', True, ""),
                ('user_email', False, 'varchar(256)', '', True, ""),
                ('created_date', False, 'timestamp', 'now()', True, ""),
                ('mod_date', False, 'timestamp', 'now()', False, ""),
            ],
            'keys': {},
            'indexes': [],
        },
        'STG_SBAC_ASMT': {
            'columns': [
                ('record_sid', True, 'bigserial', '', False, "Sequential Auto-increment"),
                ('guid_batch', False, 'varchar(256)', '', False, "Batch ID which caused the record insert"),
                ('guid_asmt', False, 'varchar(256)', '', True, "Assessment GUID"),
                ('type', False, 'varchar(256)', '', True, "Assessment Type - SUMMATIVE or INTERIM"),
                ('period', False, 'varchar(256)', '', True, "Assessment Period - SPRING 2015, FALL 9999"),
                ('year', False, 'varchar(256)', '', True, "Assessment year"),
                ('version', False, 'varchar(256)', '', True, "Assessment Version"),
                ('subject', False, 'varchar(256)', '', True, "Assessment Subject - MATH, ELA"),
                ('score_overall_min', False, 'varchar(256)', '', True, "Minimal Overall Score"),
                ('score_overall_max', False, 'varchar(256)', '', True, "Maximum Overall Score"),
                ('name_claim_1', False, 'varchar(256)', '', True, "Claim 1"),
                ('score_claim_1_min', False, 'varchar(256)', '', True, "Claim 1 Score - Minimum"),
                ('score_claim_1_max', False, 'varchar(256)', '', True, "Claim 1 Score - Maximum"),
                ('score_claim_1_weight', False, 'varchar(256)', '', True, "Claim 1 Weight"),
                ('name_claim_2', False, 'varchar(256)', '', True, "Claim 2"),
                ('score_claim_2_min', False, 'varchar(256)', '', True, "Claim 2 Score - Minimum"),
                ('score_claim_2_max', False, 'varchar(256)', '', True, "Claim 2 Score - Maximum"),
                ('score_claim_2_weight', False, 'varchar(256)', '', True, "Claim 2 Weight"),
                ('name_claim_3', False, 'varchar(256)', '', True, "Claim 3"),
                ('score_claim_3_min', False, 'varchar(256)', '', True, "Claim 3 Score - Minimum"),
                ('score_claim_3_max', False, 'varchar(256)', '', True, "Claim 3 Score - Maximum"),
                ('score_claim_3_weight', False, 'varchar(256)', '', True, "Claim 3 Weight"),
                ('name_claim_4', False, 'varchar(256)', '', True, "Claim 4"),
                ('score_claim_4_min', False, 'varchar(256)', '', True, "Claim 4 Score - Minimum"),
                ('score_claim_4_max', False, 'varchar(256)', '', True, "Claim 4 Score - Maximum"),
                ('score_claim_4_weight', False, 'varchar(256)', '', True, "Claim 4 Weight"),
                ('asmt_claim_perf_lvl_name_1', False, 'varchar(256)', '', True, "Claim Perf level 1"),
                ('asmt_claim_perf_lvl_name_2', False, 'varchar(256)', '', True, "Claim Perf level 2"),
                ('asmt_claim_perf_lvl_name_3', False, 'varchar(256)', '', True, "Claim Perf level 3"),
                ('claim_score_cut_point_1', False, 'varchar(256)', '', True, "Claim Score Cutpoint 1"),
                ('claim_score_cut_point_2', False, 'varchar(256)', '', True, "Claim Score Cutpoint 2"),
                ('name_perf_lvl_1', False, 'varchar(256)', '', True, "Performance Level 1"),
                ('name_perf_lvl_2', False, 'varchar(256)', '', True, "Performance Level 2"),
                ('name_perf_lvl_3', False, 'varchar(256)', '', True, "Performance Level 3"),
                ('name_perf_lvl_4', False, 'varchar(256)', '', True, "Performance Level 4"),
                ('name_perf_lvl_5', False, 'varchar(256)', '', True, "Performance Level 5"),
                ('score_cut_point_1', False, 'varchar(256)', '', True, "Cutpoint 1"),
                ('score_cut_point_2', False, 'varchar(256)', '', True, "Cutpoint 2"),
                ('score_cut_point_3', False, 'varchar(256)', '', True, "Cutpoint 3"),
                ('score_cut_point_4', False, 'varchar(256)', '', True, "Cutpoint 4"),
                ('created_date', False, 'timestamp', 'now()', False, "Date on which record is inserted"),
            ],
            'indexes': [],
            'keys': {},
        },
        'STG_SBAC_ASMT_OUTCOME': {
            'columns': [
                ('record_sid', True, 'bigserial', '', False, "Sequential Auto-increment"),
                ('guid_batch', False, 'varchar(256)', '', False, "Batch ID which caused the record insert"),
                ('src_file_rec_num', False, 'bigint', '', True, "Batch ID which caused the record insert"),
                ('guid_asmt', False, 'varchar(256)', '', True, "Assessment GUID"),
                ('guid_asmt_location', False, 'varchar(256)', '', True, "GUID for location where assessment was taken"),
                ('name_asmt_location', False, 'varchar(256)', '', True, "Name for location where assessment was taken"),
                ('grade_asmt', False, 'varchar(256)', '', True, "Assessment Grade"),
                ('name_state', False, 'varchar(256)', '', True, "Name of the State"),
                ('code_state', False, 'varchar(256)', '', True, "State Code"),
                ('guid_district', False, 'varchar(256)', '', True, "District GUID"),
                ('name_district', False, 'varchar(256)', '', True, "District Name"),
                ('guid_school', False, 'varchar(256)', '', True, "School GUID"),
                ('name_school', False, 'varchar(256)', '', True, "School Name"),
                ('type_school', False, 'varchar(256)', '', True, "Type of School - Hight School, Middle School, Elementary School"),
                ('guid_student', False, 'varchar(256)', '', True, "Student GUID"),
                ('name_student_first', False, 'varchar(256)', '', True, "Student First Name"),
                ('name_student_middle', False, 'varchar(256)', '', True, "Student Middle Name"),
                ('name_student_last', False, 'varchar(256)', '', True, "Student Last Name"),
                ('address_student_line1', False, 'varchar(256)', '', True, "Student Address Line 1"),
                ('address_student_line2', False, 'varchar(256)', '', True, "Student Address Line 2"),
                ('address_student_city', False, 'varchar(256)', '', True, "Student Address City"),
                ('address_student_zip', False, 'varchar(256)', '', True, "Student Address Zip"),
                ('gender_student', False, 'varchar(256)', '', True, "Student Gender"),
                ('email_student', False, 'varchar(256)', '', True, "Student email"),
                ('dob_student', False, 'varchar(256)', '', True, "Student Date of Birth"),
                ('grade_enrolled', False, 'varchar(256)', '', True, "Student Enrollment Grade"),
                ('dmg_eth_hsp', False, 'varchar(256)', '', True, 'Student ethnicity Hispanic'),
                ('dmg_eth_ami', False, 'varchar(256)', '', True, 'Student ethnicity American Indian/Alaskan Native'),
                ('dmg_eth_asn', False, 'varchar(256)', '', True, 'Student ethnicity Asian'),
                ('dmg_eth_blk', False, 'varchar(256)', '', True, 'Student ethnicity Black'),
                ('dmg_eth_pcf', False, 'varchar(256)', '', True, 'Student ethnicity Pacific Islander'),
                ('dmg_eth_wht', False, 'varchar(256)', '', True, 'Student ethnicity White'),
                ('dmg_prg_iep', False, 'varchar(256)', '', True, 'IEP (Individualized Education Program)'),
                ('dmg_prg_lep', False, 'varchar(256)', '', True, 'LEP (Limited English Proficiency)'),
                ('dmg_prg_504', False, 'varchar(256)', '', True, 'Section 504'),
                ('dmg_prg_tt1', False, 'varchar(256)', '', True, 'Title I Status'),
                ('date_assessed', False, 'varchar(256)', '', True, "Date on which student was assessed"),
                ('score_asmt', False, 'varchar(256)', '', True, "Assessment Score"),
                ('score_asmt_min', False, 'varchar(256)', '', True, "Assessment Score - Minimum"),
                ('score_asmt_max', False, 'varchar(256)', '', True, "Assessment Score - Maximum"),
                ('score_perf_level', False, 'varchar(256)', '', True, "Performance Level"),
                ('score_claim_1', False, 'varchar(256)', '', True, "Claim 1 Score"),
                ('score_claim_1_min', False, 'varchar(256)', '', True, "Claim 1 Score - Minimum"),
                ('score_claim_1_max', False, 'varchar(256)', '', True, "Claim 1 Score - Maximum"),
                ('asmt_claim_1_perf_lvl', False, 'varchar(256)', '', True, "Claim 1 Perf level"),
                ('score_claim_2', False, 'varchar(256)', '', True, "Claim 2 Score"),
                ('score_claim_2_min', False, 'varchar(256)', '', True, "Claim 2 Score - Minimum"),
                ('score_claim_2_max', False, 'varchar(256)', '', True, "Claim 2 Score - Maximum"),
                ('asmt_claim_2_perf_lvl', False, 'varchar(256)', '', True, "Claim 2 Perf level"),
                ('score_claim_3', False, 'varchar(256)', '', True, "Claim 3 Score"),
                ('score_claim_3_min', False, 'varchar(256)', '', True, "Claim 3 Score - Minimum"),
                ('score_claim_3_max', False, 'varchar(256)', '', True, "Claim 3 Score - Maximum"),
                ('asmt_claim_3_perf_lvl', False, 'varchar(256)', '', True, "Claim 3 Perf level"),
                ('score_claim_4', False, 'varchar(256)', '', True, "Claim 4 Score"),
                ('score_claim_4_min', False, 'varchar(256)', '', True, "Claim 4 Score - Minimum"),
                ('score_claim_4_max', False, 'varchar(256)', '', True, "Claim 4 Score - Maximum"),
                ('asmt_claim_4_perf_lvl', False, 'varchar(256)', '', True, "Claim 4 Perf level"),
                ('asmt_type', False, 'varchar(256)', '', True, "Assessment Type"),
                ('asmt_subject', False, 'varchar(256)', '', True, "Assessment Subject"),
                ('asmt_year', False, 'varchar(256)', '', True, 'Assessment Year'),
                ('created_date', False, 'timestamp', 'now()', False, "Date on which record is inserted"),
            ],
            'indexes': [],
            'keys': {}
        },
        'ERR_LIST': {
            'columns': [
                ('record_sid', False, 'bigint', '', False, "Foreign Key references to staging tables"),
                ('guid_batch', False, 'varchar(256)', '', False, "Batch ID which caused the record insert"),
                ('err_code', False, 'bigint', '', True, "Error Code"),
                ('err_source', False, 'bigint', '', True, "Pipeline Stage that inserted this error."),
                ('created_date', False, 'timestamp', 'now()', False, "Date on which record is inserted"),
            ],
            'indexes': [],
            'keys': {},
        },
        'INT_SBAC_ASMT': {
            'columns': [
                ('record_sid', True, 'bigserial', '', False, "Sequential Auto-increment"),
                ('guid_batch', False, 'varchar(256)', '', False, "Batch ID which caused the record insert"),
                ('guid_asmt', False, 'varchar(50)', '', False, "Assessment GUID"),
                ('type', False, 'varchar(16)', '', False, "Assessment Type - SUMMATIVE or INTERIM"),
                ('period', False, 'varchar(32)', '', False, "Assessment Period - SPRING 2015, FALL 9999"),
                ('year', False, 'smallint', '', False, "Assessment year"),
                ('version', False, 'varchar(16)', '', False, "Assessment Version"),
                ('subject', False, 'varchar(100)', '', True, "Assessment Subject - MATH, ELA"),
                ('score_overall_min', False, 'smallint', '', True, "Minimum Overall Score"),
                ('score_overall_max', False, 'smallint', '', True, "Maximum Overall Score"),
                ('name_claim_1', False, 'varchar(256)', '', True, "Claim 1"),
                ('score_claim_1_min', False, 'smallint', '', True, "Claim 1 Score - Minimum"),
                ('score_claim_1_max', False, 'smallint', '', True, "Claim 1 Score - Maximum"),
                ('score_claim_1_weight', False, "double", '', True, "Claim 1 weight"),
                ('name_claim_2', False, 'varchar(256)', '', True, "Claim 2"),
                ('score_claim_2_min', False, 'smallint', '', True, "Claim 2 Score - Minimum"),
                ('score_claim_2_max', False, 'smallint', '', True, "Claim 2 Score - Maximum"),
                ('score_claim_2_weight', False, 'double', '', True, "Claim 2 weight"),
                ('name_claim_3', False, 'varchar(256)', '', True, "Claim 3"),
                ('score_claim_3_min', False, 'smallint', '', True, "Claim 3 Score - Minimum"),
                ('score_claim_3_max', False, 'smallint', '', True, "Claim 3 Score - Maximum"),
                ('score_claim_3_weight', False, 'double', '', True, "Claim 3 weight"),
                ('name_claim_4', False, 'varchar(256)', '', True, "Claim 4"),
                ('score_claim_4_min', False, 'smallint', '', True, "Claim 4 Score - Minimum"),
                ('score_claim_4_max', False, 'smallint', '', True, "Claim 4 Score - Maximum"),
                ('score_claim_4_weight', False, 'double', '', True, "Claim 4 weight"),
                ('asmt_claim_perf_lvl_name_1', False, 'varchar(256)', '', True, "Claim Perf level 1"),
                ('asmt_claim_perf_lvl_name_2', False, 'varchar(256)', '', True, "Claim Perf level 2"),
                ('asmt_claim_perf_lvl_name_3', False, 'varchar(256)', '', True, "Claim Perf level 3"),
                ('name_perf_lvl_1', False, 'varchar(256)', '', True, "Performance Level 1"),
                ('name_perf_lvl_2', False, 'varchar(256)', '', True, "Performance Level 2"),
                ('name_perf_lvl_3', False, 'varchar(256)', '', True, "Performance Level 3"),
                ('name_perf_lvl_4', False, 'varchar(256)', '', True, "Performance Level 4"),
                ('name_perf_lvl_5', False, 'varchar(256)', '', True, "Performance Level 5"),
                ('score_cut_point_1', False, 'smallint', '', True, "Cutpoint 1"),
                ('score_cut_point_2', False, 'smallint', '', True, "Cutpoint 2"),
                ('score_cut_point_3', False, 'smallint', '', True, "Cutpoint 3"),
                ('score_cut_point_4', False, 'smallint', '', True, "Cutpoint 4"),
                ('claim_score_cut_point_1', False, 'smallint', '', True, "Claim Score Cutpoint 1"),
                ('claim_score_cut_point_2', False, 'smallint', '', True, "Claim Score Cutpoint 2"),
                ('created_date', False, 'timestamp with time zone', 'now()', False, "Date on which record is inserted"),
            ],
            'indexes': [],
            'keys': {},
        },
        'INT_SBAC_ASMT_OUTCOME': {
            'columns': [
                ('record_sid', True, 'bigserial', '', False, "Sequential Auto-increment"),
                ('guid_batch', False, 'varchar(256)', '', False, "Batch ID which caused the record insert"),
                ('guid_asmt', False, 'varchar(50)', '', True, "Assessment GUID"),
                ('guid_asmt_location', False, 'varchar(50)', '', True, "GUID for location where assessment was taken"),
                ('name_asmt_location', False, 'varchar(256)', '', True, "Name for location where assessment was taken"),
                ('grade_asmt', False, 'varchar(10)', '', False, "Assessment Grade"),
                ('name_state', False, 'varchar(32)', '', False, "Name of the State"),
                ('code_state', False, 'varchar(2)', '', False, "State Code"),
                ('guid_district', False, 'varchar(50)', '', False, "District GUID"),
                ('name_district', False, 'varchar(256)', '', False, "District Name"),
                ('guid_school', False, 'varchar(50)', '', False, "School GUID"),
                ('name_school', False, 'varchar(256)', '', False, "School Name"),
                ('type_school', False, 'varchar(20)', '', False, "Type of School - High School, Middle School, Elementary School"),
                ('guid_student', False, 'varchar(50)', '', False, "Student GUID"),
                ('name_student_first', False, 'varchar(256)', '', True, "Student First Name"),
                ('name_student_middle', False, 'varchar(256)', '', True, "Student Middle Name"),
                ('name_student_last', False, 'varchar(256)', '', True, "Student Last Name"),
                ('address_student_line1', False, 'varchar(256)', '', True, "Student Address Line 1"),
                ('address_student_line2', False, 'varchar(256)', '', True, "Student Address Line 2"),
                ('address_student_city', False, 'varchar(100)', '', True, "Student Address City"),
                ('address_student_zip', False, 'varchar(5)', '', True, "Student Address Zip"),
                ('gender_student', False, 'varchar(10)', '', True, "Student Gender"),
                ('email_student', False, 'varchar(256)', '', True, "Student email"),
                ('dob_student', False, 'varchar(8)', '', True, "Student Date of Birth"),
                ('grade_enrolled', False, 'varchar(10)', '', False, "Student Enrollment Grade"),
                ('dmg_eth_hsp', False, 'bool', '', True, 'Student ethnicity Hispanic'),
                ('dmg_eth_ami', False, 'bool', '', True, 'Student ethnicity American Indian/Alaskan Native'),
                ('dmg_eth_asn', False, 'bool', '', True, 'Student ethnicity Asian'),
                ('dmg_eth_blk', False, 'bool', '', True, 'Student ethnicity Black'),
                ('dmg_eth_pcf', False, 'bool', '', True, 'Student ethnicity Pacific Islander'),
                ('dmg_eth_wht', False, 'bool', '', True, 'Student ethnicity White'),
                ('dmg_prg_iep', False, 'bool', '', True, 'IEP (Individualized Education Program)'),
                ('dmg_prg_lep', False, 'bool', '', True, 'LEP (Limited English Proficiency)'),
                ('dmg_prg_504', False, 'bool', '', True, 'Section 504'),
                ('dmg_prg_tt1', False, 'bool', '', True, 'Title I Status'),
                ('dmg_eth_derived', False, 'smallint', '', True, 'Derived student etnicity category code'),
                ('date_assessed', False, 'varchar(8)', '', False, "Date on which student was assessed"),
                ('date_taken_day', False, 'smallint', '', False, ""),
                ('date_taken_month', False, 'smallint', '', False, ""),
                ('date_taken_year', False, 'smallint', '', False, ""),
                ('score_asmt', False, 'smallint', '', False, "Assessment Score"),
                ('score_asmt_min', False, 'smallint', '', False, "Assessment Score - Minimum"),
                ('score_asmt_max', False, 'smallint', '', False, "Assessment Score - Maximum"),
                ('score_perf_level', False, 'smallint', '', False, "Performance Level"),
                ('score_claim_1', False, 'smallint', '', True, "Claim 1 Score"),
                ('score_claim_1_min', False, 'smallint', '', True, "Claim 1 Score - Minimum"),
                ('score_claim_1_max', False, 'smallint', '', True, "Claim 1 Score - Maximum"),
                ('asmt_claim_1_perf_lvl', False, 'smallint', '', True, "Claim 1 Perf level"),
                ('score_claim_2', False, 'smallint', '', True, "Claim 2 Score"),
                ('score_claim_2_min', False, 'smallint', '', True, "Claim 2 Score - Minimum"),
                ('score_claim_2_max', False, 'smallint', '', True, "Claim 2 Score - Maximum"),
                ('asmt_claim_2_perf_lvl', False, 'smallint', '', True, "Claim 2 Perf level"),
                ('score_claim_3', False, 'smallint', '', True, "Claim 3 Score"),
                ('score_claim_3_min', False, 'smallint', '', True, "Claim 3 Score - Minimum"),
                ('score_claim_3_max', False, 'smallint', '', True, "Claim 3 Score - Maximum"),
                ('asmt_claim_3_perf_lvl', False, 'smallint', '', True, "Claim 3 Perf level"),
                ('score_claim_4', False, 'smallint', '', True, "Claim 4 Score"),
                ('score_claim_4_min', False, 'smallint', '', True, "Claim 4 Score - Minimum"),
                ('score_claim_4_max', False, 'smallint', '', True, "Claim 4 Score - Maximum"),
                ('asmt_claim_4_perf_lvl', False, 'smallint', '', True, "Claim 4 Perf level"),
                ('asmt_type', False, 'varchar(16)', '', False, "Assessment Type - SUMMATIVE or INTERIM"),
                ('asmt_subject', False, 'varchar(32)', '', False, "Math, ELA ..."),
                ('asmt_year', False, 'smallint', '', False, "Assessment year"),
                ('created_date', False, 'timestamp with time zone', 'now()', False, "Date on which record is inserted"),
            ],
            'indexes': [],
            'keys': {},
        },
        'REF_COLUMN_MAPPING': {
            'columns': [
                ('column_map_key', True, 'bigserial', '', False, 'Primary key for the table'),
                ('phase', False, 'smallint', '', True, 'The phase in the pipeline where this mapping/transformation occurs'),
                ('source_table', False, 'varchar(50)', '', False, 'name of the source table. could also be csv or json'),
                ('source_column', False, 'varchar(256)', '', True, 'name of the source column'),
                ('target_table', False, 'varchar(50)', '', True, 'name of the target table'),
                ('target_column', False, 'varchar(50)', '', True, 'Name of the target column'),
                ('transformation_rule', False, 'varchar(50)', '', True, 'Name of the table to look for transformation or validation actions'),
                ('stored_proc_name', False, 'varchar(256)', '', True, 'Name of stored procedure to use during this transformation'),
                ('stored_proc_created_date', False, 'timestamp with time zone', '', True, 'Date when the stored procedure was added'),
                ('created_date', False, 'timestamp with time zone', 'now()', False, 'Date on which record is inserted')
            ],
            'indexes': [],
            'keys': {},
        },
        'MASTER_METADATA': {
            'columns': [
                #('column name', 'is a primary key', 'type', 'default value', 'Nullalbe', 'Comments')
                ('metadata_sid', True, 'bigserial', '', False, 'Primary key for the table'),
                ('tenant_code', False, 'varchar(10)', '', False, 'the code for the tenant'),
                ('tenant_name', False, 'varchar(255)', '', True, 'the name of the tenant'),
                ('udl_tenant_schema', False, 'varchar(255)', '', True, 'the name of the target schema'),
                ('target_db_host', False, 'varchar(255)', '', False, 'the host where the target schema is located'),
                ('target_db_name', False, 'varchar(255)', '', False, 'the name of the target database'),
                ('target_schema_name', False, 'varchar(255)', '', False, 'name of the target schema'),
                ('target_schema_port', False, 'smallint', '5432', False, 'the port to connect to'),
                ('target_schema_user_name', False, 'varchar(255)', '', False, 'username for target schema'),
                ('target_schema_passwd', False, 'varchar(255)', '', False, 'password for target schema'),
                ('created_date', False, 'timestamp with time zone', 'now()', False, 'Date that the record was adddd'),
            ],
            'indexes': [],
            'keys': {},
        }
    },
    'SEQUENCES': {
        # This are for sequences that is not associated with any specific tables for our usage
        # (sequance_name, start, increment, option, quote)
        'GLOBAL_REC_SEQ': ('GLOBAL_REC_SEQ', 1, 1, True, 'Global record id sequences. form 1 to 2^63 -1 on postgresql')
    }
}


def _parse_args():
    '''
    private method to parse command line options when call from shell. We use it to setup/teardown database
    automatically by configuration (this helps jenkins/Continous Integration)
    '''
    parser = argparse.ArgumentParser('database')
    parser.add_argument('--config_file', dest='config_file',
                        help="full path to configuration file for UDL2, default is /opt/wgen/edware-udl/etc/udl2_conf.py")
    parser.add_argument('--action', dest='action', required=False,
                        help="'setup' for setting up udl2 database. " +
                             "'teardown' for tear down udl2 database")
    args = parser.parse_args()
    return (parser, args)


def _create_conn_engine(udl2_conf):
    '''
    private method to create database connections via database_util
    @param udl2_conf: The configuration dictionary for databases
    '''
    (conn, engine) = connect_db(udl2_conf['db_driver'],
                                udl2_conf['db_user'],
                                udl2_conf['db_pass'],
                                udl2_conf['db_host'],
                                udl2_conf['db_port'],
                                udl2_conf['db_name'])
    return (conn, engine)


def map_sql_type_to_sqlalchemy_type(sql_type):
    '''
    map sql data type in configuration file into what SQLAlchemy type is.
    @param sql_type: sql data type
    '''
    mapped_type = None
    sql_type_mapped_type = {
        'timestamp': TIMESTAMP,
        'timestamp with time zone': TIMESTAMP(True),
        'bigint': BIGINT,
        'smallint': SMALLINT,
        'bigserial': BIGINT,
        'varchar': VARCHAR,
        'double': FLOAT,
        'json': TEXT,
        'text': TEXT,
        'bool': BOOLEAN,
        'interval': Interval,
        'time': Time
    }
    try:
        mapped_type = sql_type_mapped_type[sql_type]
    except Exception as e:
        if sql_type[0:7] == 'varchar':
            length = int(sql_type[7:].replace('(', '').replace(')', ''))
            mapped_type = VARCHAR(length)
    return mapped_type


def map_tuple_to_sqlalchemy_column(ddl_tuple):
    '''
    create a SQLAlchemy Column object from UDL_METADATA column
    @param ddl_tuple: column definition in UDL_METADATA
    '''
    column = Column(ddl_tuple[0],
                    map_sql_type_to_sqlalchemy_type(ddl_tuple[2]),
                    primary_key=ddl_tuple[1],
                    nullable=ddl_tuple[4],
                    server_default=(text(ddl_tuple[3]) if (ddl_tuple[3] != '') else None),
                    doc=ddl_tuple[5],)
    # print(column)
    return column


def create_table_keys(key_ddl_dict, schema):
    '''
    Take a dictionary of key lists. Will check for 'foreign' and 'unique' in the list
    and create sqlalchemy ForeignKeys objects and UniqueKey objects, respectively
    @param key_ddl_dict: A dictionary containing key information. Each value should be a list of tuples.
    the unique key tuple will contain any number of columns that constitute the unique combination. ('col1', 'col2', ...)
    the foreign key tuple will contain the column in the current table and
    the table and column in the other table. ie: ('col1', 'table2.col2')
    @type key_ddl_dict: dict
    @return: A list of foreign and unique keys
    @rtype: list
    '''
    key_list = []
    unique_keys = key_ddl_dict.get('unique', [])
    foreign_keys = key_ddl_dict.get('foreign', [])

    for uk_tup in unique_keys:
        ukc = UniqueConstraint(*uk_tup)
        key_list.append(ukc)

    for fk_tup in foreign_keys:
        foreign_column = schema + '.' + fk_tup[1]
        fk_name = "%s-%s" % (fk_tup[0], foreign_column)
        fkc = ForeignKeyConstraint([fk_tup[0]], [foreign_column], name=fk_name, use_alter=True)
        key_list.append(fkc)

    return key_list


def create_table(metadata, table_name):
    '''
    create a table from UDL_METADATA definitions
    @param udl2_conf: The configuration dictionary for udl
    @param metadata: SQLAlchemy Metadata object
    @param scheam: Schema name where the table is located in UDL2 schema
    @param table_name: Table name for the table to be created, it must be defined in UDL_METADATA
    '''
    #print('create table metadata %s' % table_name)
    column_ddl = UDL_METADATA['TABLES'][table_name]['columns']
    key_ddl = UDL_METADATA['TABLES'][table_name]['keys']
    arguments = [table_name, metadata]

    for c_ddl in column_ddl:
        #print(c_ddl)
        column = map_tuple_to_sqlalchemy_column(c_ddl)
        arguments.append(column)

    # create unique and foreign table keys, Add to arguments
    # arguments += create_table_keys(key_ddl, schema)

    table = Table(*tuple(arguments))

    return table


def drop_table(udl2_conf, schema, table_name):
    '''
    drop a table
    @param udl2_conf: The configuration dictionary for
    @param scheam: Schema name where the table is located in UDL2 schema
    @param table_name: Table name for the table to be created, it must be defined in UDL_METADATA
    '''
    print('drop table %s.%s' % (schema, table_name))
    sql = text("DROP TABLE \"%s\".\"%s\" CASCADE" % (schema, table_name))
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to drop table %s.%s" % (schema, table_name)
    execute_queries(conn, [sql], except_msg)


def create_sequence(connection, metadata, schema, seq_name):
    '''
    create a sequence from UDL_METADATA definitions
    @param udl2_conf: The configuration dictionary for udl
    @param metadata: SQLAlchemy Metadata object
    @param schema: Schema name where the table is located in UDL2 schema
    @param seq_name: sequence name for the sequence to be created, it must be defined in UDL_METADATA
    '''
    print('create global sequence')
    sequence_ddl = UDL_METADATA['SEQUENCES'][seq_name]
    sequence = Sequence(name=sequence_ddl[0],
                        start=sequence_ddl[1],
                        increment=sequence_ddl[2],
                        schema=schema,
                        optional=sequence_ddl[3],
                        quote=sequence_ddl[4],
                        metadata=metadata)
    connection.execute(CreateSequence(sequence))

    #except_msg = "fail to create sequence %s.%s" % (schema, seq_name)
    #execute_queries(conn, [sql], except_msg)
    return sequence


def drop_sequence(udl2_conf, schema, seq_name):
    '''
    drop schemas according to configuration file
    @param udl2_conf: The configuration dictionary for udl
    @param schema: Schema name where the table is located in UDL2 schema
    @param seq_name: sequence name for the sequence to be created, it must be defined in UDL_METADATA
    '''
    print('drop global sequences')
    sql = text("DROP SEQUENCE \"%s\".\"%s\" CASCADE" % (schema, seq_name))
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to drop sequence %s.%s" % (schema, seq_name)
    execute_queries(conn, [sql], except_msg)


#def create_udl2_schema(udl2_conf):
#    '''
#    create schemas according to configuration file
#    @param udl2_conf: The configuration dictionary for
#    '''
#    print('create udl2 staging schema')
#    sql = text("CREATE SCHEMA \"%s\"" % udl2_conf['staging_schema'])
#    (conn, engine) = _create_conn_engine(udl2_conf)
#    except_msg = "fail to create schema %s" % udl2_conf['staging_schema']
#    execute_queries(conn, [sql], except_msg)


def drop_udl2_schema(udl2_conf):
    '''
    drop schemas according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    print('drop udl2 staging schema')
    sql = text("DROP SCHEMA \"%s\" CASCADE" % udl2_conf['staging_schema'])
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to drop udl2 schema %s" % udl2_conf['staging_schema']
    execute_queries(conn, [sql], except_msg)


def create_udl2_tables(udl2_conf):
    '''
    create tables in schema according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    # engine = (_get_db_url(udl2_conf))
    udl2_metadata = generate_udl2_metadata(udl2_conf['staging_schema'])
    print("create tables")

    (conn, engine) = _create_conn_engine(udl2_conf)

    # Use metadata to create tables
    udl2_metadata.create_all(engine)


def drop_udl2_tables(udl2_conf):
    '''
    drop tables according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    print("drop tables")
    for table, definition in UDL_METADATA['TABLES'].items():
        drop_table(udl2_conf, udl2_conf['staging_schema'], table)


def create_udl2_sequence(connection, schema_name, udl2_metadata):
    '''
    create sequences according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    # (conn, engine) = _create_conn_engine(udl2_conf['udl2_db'])
    #udl2_metadata = MetaData()
    print("create sequences")
    for sequence, definition in UDL_METADATA['SEQUENCES'].items():
        create_sequence(connection, udl2_metadata, schema_name, sequence)


def drop_udl2_sequences(udl2_conf):
    '''
    drop sequences according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    print("drop sequences")
    for seq, definition in UDL_METADATA['SEQUENCES'].items():
        drop_sequence(udl2_conf, udl2_conf['staging_schema'], seq)


def create_foreign_data_wrapper_extension(udl2_conf):
    '''
    create foreign data wrapper extension according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    print('create foreign data wrapper extension')
    sql = "CREATE EXTENSION IF NOT EXISTS file_fdw WITH SCHEMA %s" % (udl2_conf['csv_schema'])
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to create foreign data wrapper extension"
    execute_queries(conn, [sql], except_msg)


def drop_foreign_data_wrapper_extension(udl2_conf):
    '''
    drop foreign data wrapper extension according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    print('drop foreign data wrapper extension')
    sql = "DROP EXTENSION IF EXISTS file_fdw CASCADE"
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to drop foreign data wrapper extension"
    execute_queries(conn, [sql], except_msg)


def create_dblink_extension(udl2_conf):
    '''
    create dblink extension according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    print('create dblink extension')
    sql = "CREATE EXTENSION IF NOT EXISTS dblink WITH SCHEMA %s" % (udl2_conf['db_schema'])
    print(sql)
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to create dblink extension"
    execute_queries(conn, [sql], except_msg)


def drop_dblink_extension(udl2_conf):
    '''
    drop dblink extension according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    print('drop dblink extension')
    sql = "DROP EXTENSION IF EXISTS dblink CASCADE"
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to drop dblink extension"
    execute_queries(conn, [sql], except_msg)


def create_foreign_data_wrapper_server(udl2_conf):
    '''
    create server for foreign data wrapper according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    print('create foreign data wrapper server')
    sql = "CREATE SERVER %s FOREIGN DATA WRAPPER file_fdw" % (udl2_conf['fdw_server'])
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to create foreign data wrapper server"
    execute_queries(conn, [sql], except_msg)


def drop_foreign_data_wrapper_server(udl2_conf):
    '''
    drop server for foreign data wrapper according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    print('drop foreign data wrapper server')
    sql = "DROP SERVER IF EXISTS %s CASCADE" % (udl2_conf['fdw_server'])
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to drop foreign data wrapper server"
    execute_queries(conn, [sql], except_msg)


def load_fake_record_in_star_schema(udl2_conf):
    '''
    load two fake records into dim_int_hier and dim_section for integration table to create
    star schema from integration table
    @param udl2_conf: The configuration dictionary for
    '''
    print('load fake record')
    (conn, engine) = _create_conn_engine(udl2_conf)
    sqls = [
        """
        INSERT INTO "{schema_name}"."dim_section"(
            section_rec_id, section_guid, section_name, grade, class_name,
            subject_name, state_code, district_guid, school_guid, from_date,
            to_date, most_recent)
        VALUES (1, 'fake_value', 'fake_value', 'fake_value', 'fake_value',
            'fake_value', 'FA', 'fake_value', 'fake_value', '99999999',
            '00000000', False);
        """.format(schema_name=udl2_conf['db_schema']),
        """
        INSERT INTO "{schema_name}"."dim_inst_hier"(
            inst_hier_rec_id, state_name, state_code, district_guid, district_name,
            school_guid, school_name, school_category, from_date, to_date,
            most_recent)
        VALUES (-1, 'fake_value', 'FA', 'fake_value', 'fake_value',
            'fake_value', 'fake_value', 'fake_value', '99999999', '00000000',
            False);
        """.format(schema_name=udl2_conf['db_schema']),
    ]
    except_msg = "fail to drop foreign data wrapper server"
    execute_queries(conn, sqls, except_msg)


def load_reference_data(udl2_conf):
    '''
    load the reference data into the referenct tables
    @param udl2_conf: The configuration dictionary for
    '''
    (conn, engine) = _create_conn_engine(udl2_conf)
    ref_table_info = ref_table_data.ref_table_conf
    populate_ref_column_map(ref_table_info, engine, conn, udl2_conf['reference_schema'], udl2_conf['ref_table_name'])


def load_stored_proc(udl2_conf):
    '''
    Generate and load the stored procedures to be used for transformations and
    validations into the database.
    @param udl2_conf: The configuration dictionary for
    '''

    (conn, engine) = _create_conn_engine(udl2_conf)
    populate_stored_proc(engine, conn, udl2_conf['reference_schema'], udl2_conf['ref_table_name'])


###
# NEW METHODS TO MAKE METADATA USAGE SIMPLER
###

def create_udl2_schema(engine, connection, schema_name, bind=None):
    """

    :param engine:
    :param connection:
    :param schema_name:
    :param bind:
    :return:
    """
    metadata = generate_udl2_metadata(schema_name, bind=bind)
    connection.execute(CreateSchema(metadata.schema))
    metadata.create_all(bind=engine)
    return metadata


def generate_udl2_metadata(schema_name=None, bind=None):
    """

    :param schema_name:
    :param bind:
    :return:
    """
    metadata = MetaData(schema=schema_name, bind=bind)

    # add tables to metadata
    for table, definition in UDL_METADATA['TABLES'].items():
        create_table(metadata, table)

    return metadata


####
## END NEW METHODS
####

def setup_udl2_schema(udl2_conf):
    '''
    create whole udl2 database schema according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    # Create schema, tables and sequences
    (udl2_db_conn, udl2_db_engine) = _create_conn_engine(udl2_conf['udl2_db'])
    udl2_schema_name = udl2_conf['udl2_db']['db_schema']
    udl2_metadata = create_udl2_schema(udl2_db_engine, udl2_db_conn, udl2_schema_name)
    create_udl2_sequence(udl2_db_conn, udl2_schema_name, udl2_metadata)

    # create db_link and fdw
    create_dblink_extension(udl2_conf['target_db'])
    create_dblink_extension(udl2_conf['udl2_db'])
    create_foreign_data_wrapper_extension(udl2_conf['udl2_db'])
    create_foreign_data_wrapper_server(udl2_conf['udl2_db'])

    # load data and stored procedures
    load_fake_record_in_star_schema(udl2_conf['target_db'])
    load_reference_data(udl2_conf['udl2_db'])
    load_stored_proc(udl2_conf['udl2_db'])


def teardown_udl2_schema(udl2_conf):
    '''
    drop whole udl2 database schema according to configuration file
    @param udl2_conf: The configuration dictionary for
    '''
    drop_udl2_sequences(udl2_conf['udl2_db'])
    drop_udl2_tables(udl2_conf['udl2_db'])
    drop_foreign_data_wrapper_server(udl2_conf['udl2_db'])
    drop_foreign_data_wrapper_extension(udl2_conf['udl2_db'])
    drop_dblink_extension(udl2_conf['udl2_db'])
    drop_udl2_schema(udl2_conf['udl2_db'])
    drop_dblink_extension(udl2_conf['target_db'])


def main():
    '''
    create or drop udl2 database objects according to command line.
    The purpose for this script is to enable clean up whole database artifacts or create
    whole database artifacts without problem. Since UDL uses databases to clean data. Database object
    in UDL can be dropped or recreated at will for changes. So we can verifiy system
    '''
    (parser, args) = _parse_args()
    if args.config_file is None:
        config_path_file = UDL2_DEFAULT_CONFIG_PATH_FILE
    else:
        config_path_file = args.config_file
    udl2_conf = imp.load_source('udl2_conf', config_path_file)
    from udl2_conf import udl2_conf

    if args.action is None:
        parser.print_help()
    if args.action == 'setup':
        setup_udl2_schema(udl2_conf)
    elif args.action == 'teardown':
        teardown_udl2_schema(udl2_conf)

if __name__ == '__main__':
    main()
