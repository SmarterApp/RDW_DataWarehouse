'''
Created on May 10, 2013

@author: ejen
'''
from sqlalchemy.schema import MetaData, CreateSchema, CreateTable, CreateSequence
from sqlalchemy import Table, Column, Index, Sequence
from sqlalchemy import SmallInteger, String, Date, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.types import *
from sqlalchemy.engine import create_engine
from sqlalchemy.sql.expression import func, text
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.sql import text
import imp
import argparse
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from udl2_util.database_util import connect_db, execute_queries

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
                ('record_sid', True, 'bigserial', '', False, "Sequential Auto-increment"),
                ('batch_id', False, 'bigint', '', False, "Batch ID which caused the record insert"),
                ('substr_test', False, 'varchar(256)', '', False, "mock data for test type conversion during staging to integration"),
                ('number_test', False, 'varchar(256)', '', False, "mock data for test type conversion during staging to integration"),
            ],
            'indexes': [],
            'keys': [],
        },
        'INT_MOCK_LOAD': {
            'columns': [
                ('record_sid', True, 'bigserial', '', False, "Sequential Auto-increment"),
                ('batch_id', False, 'bigint', '', False, "Batch ID which caused the record insert"),
                ('substr_test', False, 'varchar(256)', '', False, "mock data for test type conversion during staging to integration"),
                ('number_test', False, 'varchar(256)', '', False, "mock data for test type conversion during staging to integration"),
            ],
            'indexes': [],
            'keys': [],
        },
        'UDL_BATCH': {
            'columns': [
                ('batch_sid', True, 'bigserial', '', False, ""),
                ('batch_user_status', False, 'varchar(50)', '', True, ""),
                ('job_status', False, 'varchar(50)', '', True, ""),
                ('task_id', False, 'varchar(255)', '', True, ""),
                ('task_status_url', False, 'varchar(255)', '', True, ""),
                ('user_sid', False, 'bigint', '', True, ""),
                ('user_email', False, 'varchar(255)', '', True, ""),
                ('src_file_name', False, 'varchar(255)', '', True, ""),
                ('source_folder', False, 'varchar(120)', '', True, ""),
                ('parent_file_type', False, 'varchar(80)', '', True, ""),
                ('src_file_type', False, 'varchar(80)', '', True, ""),
                ('process_instruction', False, 'json', '', True, ""),
                ('etl_stg_target', False, 'varchar(127)', '', True, ""),
                ('etl_int_src', False, 'varchar(127)', '', True, ""),
                ('etl_int_target', False, 'varchar(127)', '', True, ""),
                ('etl_hist_src', False, 'varchar(127)', '', True, ""),
                ('etl_hist_target', False, 'varchar(127)', '', True, ""),
                ('etl_err_src', False, 'varchar(127)', '', True, ""),
                ('error_file_path', False, 'varchar(250)', '', True, ""),
                ('archive_name', False, 'varchar(120)', '', True, ""),
                ('created_date', False, 'timestamp', 'now()', True, ""),
                ('mod_date', False, 'timestamp', 'now()', True, ""),
            ],
            'keys': [],
            'indexes': [],
        },
        'STG_SBAC_ASMT': {
            'columns': [
                ('record_sid', True, 'bigserial', '', False, "Sequential Auto-increment"),
                ('batch_id', False, 'bigint', '', False, "Batch ID which caused the record insert"),
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
            'keys': [],
        },
        'STG_SBAC_ASMT_OUTCOME': {
            'columns': [
                ('record_sid', True, 'bigserial', '', False, "Sequential Auto-increment"),
                ('batch_id', False, 'bigint', '', False, "Batch ID which caused the record insert"),
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
                ('date_assessed', False, 'varchar(256)', '', True, "Date on which student was assessed"),
                ('score_asmt', False, 'varchar(256)', '', True, "Assessment Score"),
                ('score_asmt_min', False, 'varchar(256)', '', True, "Assessment Score - Minimum"),
                ('score_asmt_max', False, 'varchar(256)', '', True, "Assessment Score - Maximum"),
                ('score_perf_level', False, 'varchar(256)', '', True, "Performance Level"),
                ('score_claim_1', False, 'varchar(256)', '', True, "Claim 1 Score"),
                ('score_claim_1_min', False, 'varchar(256)', '', True, "Claim 1 Score - Minimum"),
                ('score_claim_1_max', False, 'varchar(256)', '', True, "Claim 1 Score - Maximum"),
                ('score_claim_2', False, 'varchar(256)', '', True, "Claim 2 Score"),
                ('score_claim_2_min', False, 'varchar(256)', '', True, "Claim 2 Score - Minimum"),
                ('score_claim_2_max', False, 'varchar(256)', '', True, "Claim 2 Score - Maximum"),
                ('score_claim_3', False, 'varchar(256)', '', True, "Claim 3 Score"),
                ('score_claim_3_min', False, 'varchar(256)', '', True, "Claim 3 Score - Minimum"),
                ('score_claim_3_max', False, 'varchar(256)', '', True, "Claim 3 Score - Maximum"),
                ('score_claim_4', False, 'varchar(256)', '', True, "Claim 4 Score"),
                ('score_claim_4_min', False, 'varchar(256)', '', True, "Claim 4 Score - Minimum"),
                ('score_claim_4_max', False, 'varchar(256)', '', True, "Claim 4 Score - Maximum"),
                ('guid_staff', False, 'varchar(256)', '', True, "Staff GUID"),
                ('name_staff_first', False, 'varchar(256)', '', True, "Staff First Name"),
                ('name_staff_middle', False, 'varchar(256)', '', True, "Staff Middle Name"),
                ('name_staff_last', False, 'varchar(256)', '', True, "Staff Last Name"),
                ('type_staff', False, 'varchar(256)', '', True, "User Type - Staff, Teacher"),
                ('created_date', False, 'timestamp', 'now()', False, "Date on which record is inserted"),
            ],
            'indexes': [],
            'keys': []
        },
        'ERR_LIST': {
            'columns': [
                ('record_sid', False, 'bigint', '', False, "Foreign Key references to staging tables"),
                ('batch_id', False, 'bigint', '', False, "Batch ID which caused the record insert"),
                ('err_code', False, 'bigint', '', True, "Error Code"),
                ('err_source', False, 'bigint', '', True, "Pipeline Stage that inserted this error."),
                ('created_date', False, 'timestamp', 'now()', False, "Date on which record is inserted"),
            ],
            'indexes': [],
            'keys': [],
        },
        'INT_SBAC_ASMT': {
            'columns': [
                ('record_sid', True, 'bigserial', '', False, "Sequential Auto-increment"),
                ('batch_id', False, 'bigint', '', False, "Batch ID which caused the record insert"),
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
                ('name_perf_lvl_1', False, 'varchar(256)', '', True, "Performance Level 1"),
                ('name_perf_lvl_2', False, 'varchar(256)', '', True, "Performance Level 2"),
                ('name_perf_lvl_3', False, 'varchar(256)', '', True, "Performance Level 3"),
                ('name_perf_lvl_4', False, 'varchar(256)', '', True, "Performance Level 4"),
                ('name_perf_lvl_5', False, 'varchar(256)', '', True, "Performance Level 5"),
                ('score_cut_point_1', False, 'smallint', '', True, "Cutpoint 1"),
                ('score_cut_point_2', False, 'smallint', '', True, "Cutpoint 2"),
                ('score_cut_point_3', False, 'smallint', '', True, "Cutpoint 3"),
                ('score_cut_point_4', False, 'smallint', '', True, "Cutpoint 4"),
                ('created_date', False, 'timestamp with time zone', 'now()', False, "Date on which record is inserted"),
            ],
            'indexes': [],
            'keys': [],
        },
        'INT_SBAC_ASMT_OUTCOME': {
            'columns': [
                ('record_sid', True, 'bigserial', '', False, "Sequential Auto-increment"),
                ('batch_id', False, 'bigint', '', False, "Batch ID which caused the record insert"),
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
                ('score_claim_2', False, 'smallint', '', True, "Claim 2 Score"),
                ('score_claim_2_min', False, 'smallint', '', True, "Claim 2 Score - Minimum"),
                ('score_claim_2_max', False, 'smallint', '', True, "Claim 2 Score - Maximum"),
                ('score_claim_3', False, 'smallint', '', True, "Claim 3 Score"),
                ('score_claim_3_min', False, 'smallint', '', True, "Claim 3 Score - Minimum"),
                ('score_claim_3_max', False, 'smallint', '', True, "Claim 3 Score - Maximum"),
                ('score_claim_4', False, 'smallint', '', True, "Claim 4 Score"),
                ('score_claim_4_min', False, 'smallint', '', True, "Claim 4 Score - Minimum"),
                ('score_claim_4_max', False, 'smallint', '', True, "Claim 4 Score - Maximum"),
                ('guid_staff', False, 'varchar(50)', '', True, "Staff GUID"),
                ('name_staff_first', False, 'varchar(256)', '', True, "Staff First Name"),
                ('name_staff_middle', False, 'varchar(256)', '', True, "Staff Middle Name"),
                ('name_staff_last', False, 'varchar(256)', '', True, "Staff Last Name"),
                ('type_staff', False, 'varchar(10)', '', True, "User Type - Staff, Teacher"),
                ('created_date', False, 'timestamp with time zone', 'now()', False, "Date on which record is inserted"),
            ],
            'indexes': [],
            'keys': [],
        }
    },
    'SEQUENCES': {
        # This are for sequences that is not associated with any specific tables for our usage
        # (sequance_name, start, increment, option, quote)
        'GLOBAL_REC_SEQ': ('GLOBAL_REC_SEQ', 1, 1, True, 'Global record id sequences. form 1 to 2^63 -1 on postgresql')
    }
}


def _parse_args():
    parser = argparse.ArgumentParser('database')
    parser.add_argument('--config_file', dest='config_file',
                        help="full path to configuration file for UDL2, default is /opt/wgen/edware-udl/etc/udl2_conf.py")
    parser.add_argument('--action', dest='action', required=False,
                        help="'setup' for setting up udl2 database. " +
                             "'teardown' for tear down udl2 database")
    args = parser.parse_args()
    return (parser, args)


def _create_conn_engine(udl2_conf):
    (conn, engine) = connect_db(udl2_conf['udl2_db']['db_driver'],
                                udl2_conf['udl2_db']['db_user'],
                                udl2_conf['udl2_db']['db_pass'],
                                udl2_conf['udl2_db']['db_host'],
                                udl2_conf['udl2_db']['db_port'],
                                udl2_conf['udl2_db']['db_name'])
    return (conn, engine)


def map_sql_type_to_sqlalchemy_type(sql_type):
    mapped_type = None
    sql_type_mapped_type = {
        'timestamp': TIMESTAMP,
        'timestamp with time zone': TIMESTAMP(True),
        'bigint': BIGINT,
        'smallint': SMALLINT,
        'bigserial': BIGINT,
        'varchar': VARCHAR,
        'double': FLOAT,
        'json': TEXT
    }
    try:
        mapped_type = sql_type_mapped_type[sql_type]
    except Exception as e:
        if sql_type[0:7] == 'varchar':
            length = int(sql_type[7:].replace('(', '').replace(')', ''))
            mapped_type = VARCHAR(length)
    return mapped_type


def map_tuple_to_sqlalchemy_column(ddl_tuple):
    column = Column(ddl_tuple[0],
                    map_sql_type_to_sqlalchemy_type(ddl_tuple[2]),
                    primary_key=ddl_tuple[1],
                    nullable=ddl_tuple[4],
                    server_default=(text(ddl_tuple[3]) if (ddl_tuple[3] != '') else None),
                    doc=ddl_tuple[5],)
   # print(column)
    return column


def create_table(udl2_conf, metadata, schema, table_name):
    print('create table %s.%s' % (schema, table_name))
    column_ddl = UDL_METADATA['TABLES'][table_name]['columns']
    arguments = [table_name, metadata]

    for c_ddl in column_ddl:
        #print(c_ddl)
        column = map_tuple_to_sqlalchemy_column(c_ddl)
        arguments.append(column)
    table = Table(*tuple(arguments), **{'schema': schema})
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to create table %s.%s" % (schema, table_name)
    try:
        table.create(engine)
    except Exception:
        print(except_msg)
    return table


def drop_table(udl2_conf, schema, table_name):
    print('drop table %s.%s' % (schema, table_name))
    sql = text("DROP TABLE \"%s\".\"%s\" CASCADE" % (schema, table_name))
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to drop table %s.%s" % (schema, table_name)
    execute_queries(conn, [sql], except_msg)


def create_sequence(udl2_conf, metadata, schema, seq_name):
    print('create global sequence')
    sequence_ddl = UDL_METADATA['SEQUENCES'][seq_name]
    sequence = Sequence(name=sequence_ddl[0],
                        start=sequence_ddl[1],
                        increment=sequence_ddl[2],
                        schema=schema,
                        optional=sequence_ddl[3],
                        quote=sequence_ddl[4],
                        metadata=metadata)
    sql = CreateSequence(sequence)
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to create sequence %s.%s" % (schema, seq_name)
    execute_queries(conn, [sql], except_msg)
    return sequence


def drop_sequence(udl2_conf, schema, seq_name):
    print('drop global sequences')
    sql = text("DROP SEQUENCE \"%s\".\"%s\" CASCADE" % (schema, seq_name))
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to drop sequence %s.%s" % (schema, seq_name)
    execute_queries(conn, [sql], except_msg)


def create_udl2_schema(udl2_conf):
    print('create udl2 staging schema')
    sql = text("CREATE SCHEMA \"%s\"" % udl2_conf['udl2_db']['staging_schema'])
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to create schema %s" % udl2_conf['udl2_db']['staging_schema']
    execute_queries(conn, [sql], except_msg)


def drop_udl2_schema(udl2_conf):
    print('drop udl2 staging schema')
    sql = text("DROP SCHEMA \"%s\" CASCADE" % udl2_conf['udl2_db']['staging_schema'])
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to drop udl2 schema %s" % udl2_conf['udl2_db']['staging_schema']
    execute_queries(conn, [sql], except_msg)


def create_udl2_tables(udl2_conf):
    #engine = (_get_db_url(udl2_conf))
    udl2_metadata = MetaData()
    print("create tables")
    for table, definition in UDL_METADATA['TABLES'].items():
        create_table(udl2_conf, udl2_metadata, udl2_conf['udl2_db']['staging_schema'], table)


def drop_udl2_tables(udl2_conf):
    print("drop tables")
    for table, definition in UDL_METADATA['TABLES'].items():
        drop_table(udl2_conf, udl2_conf['udl2_db']['staging_schema'], table)


def create_udl2_sequence(udl2_conf):
    #(conn, engine) = _create_conn_engine(udl2_conf)
    udl2_metadata = MetaData()
    print("create sequences")
    for sequence, definition in UDL_METADATA['SEQUENCES'].items():
        create_sequence(udl2_conf, udl2_metadata, udl2_conf['udl2_db']['staging_schema'], sequence)


def drop_udl2_sequences(udl2_conf):
    print("drop sequences")
    for seq, definition in UDL_METADATA['SEQUENCES'].items():
        drop_sequence(udl2_conf, udl2_conf['udl2_db']['staging_schema'], seq)


def create_foreign_data_wrapper_extension(udl2_conf):
    print('create foreign data wrapper extension')
    sql = "CREATE EXTENSION IF NOT EXISTS file_fdw WITH SCHEMA %s" % (udl2_conf['udl2_db']['csv_schema'])
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to create foreign data wrapper extension"
    execute_queries(conn, [sql], except_msg)


def drop_foreign_data_wrapper_extension(udl2_conf):
    print('drop foreign data wrapper extension')
    sql = "DROP EXTENSION IF EXISTS file_fdw CASCADE"
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to drop foreign data wrapper extension"
    execute_queries(conn, [sql], except_msg)


def create_dblink_extension(udl2_conf):
    print('create dblink extension')
    sql = "CREATE EXTENSION IF NOT EXISTS dblink WITH SCHEMA %s" % (udl2_conf['udl2_db']['csv_schema'])
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to create dblink extension"
    execute_queries(conn, [sql], except_msg)


def drop_dblink_extension(udl2_conf):
    print('drop dblink extension')
    sql = "DROP EXTENSION IF EXISTS dblink CASCADE"
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to drop dblink extension"
    execute_queries(conn, [sql], except_msg)


def create_foreign_data_wrapper_server(udl2_conf):
    print('create foreign data wrapper server')
    sql = "CREATE SERVER %s FOREIGN DATA WRAPPER file_fdw" % (udl2_conf['udl2_db']['fdw_server'])
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to create foreign data wrapper server"
    execute_queries(conn, [sql], except_msg)


def drop_foreign_data_wrapper_server(udl2_conf):
    print('drop foreign data wrapper server')
    sql = "DROP SERVER IF EXISTS %s CASCADE" % (udl2_conf['udl2_db']['fdw_server'])
    (conn, engine) = _create_conn_engine(udl2_conf)
    except_msg = "fail to drop foreign data wrapper server"
    execute_queries(conn, [sql], except_msg)


def setup_udl2_schema(udl2_conf):
    create_udl2_schema(udl2_conf)
    create_dblink_extension(udl2_conf)
    create_foreign_data_wrapper_extension(udl2_conf)
    create_foreign_data_wrapper_server(udl2_conf)
    create_udl2_tables(udl2_conf)
    create_udl2_sequence(udl2_conf)


def teardown_udl2_schema(udl2_conf):
    drop_udl2_sequences(udl2_conf)
    drop_udl2_tables(udl2_conf)
    drop_foreign_data_wrapper_server(udl2_conf)
    drop_foreign_data_wrapper_extension(udl2_conf)
    drop_dblink_extension(udl2_conf)
    drop_udl2_schema(udl2_conf)


def main():
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
