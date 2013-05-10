from sqlalchemy.schema import MetaData, CreateSchema, CreateTable
from sqlalchemy import Table, Column, Index
from sqlalchemy import SmallInteger, String, Date, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy.types import *
from sqlalchemy.engine import create_engine
from sqlalchemy.sql.expression import func, text
from sqlalchemy.dialects.postgresql import *
import imp
import argparse
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE

#
# We use a list of columns for table.
# for each column ('column name', 'is a primary key', 'type', 'default value', 'Nullalbe', 'Comments')

UDL_TABLE_METADATA = { 
    'UDL_BATCH': {'columns':
        [
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
        ('create_date', False, 'timestamp', 'now()', True, ""),
        ('mod_date', False, 'timestamp', 'now()', True, ""),
        ],
        'keys' : [],
        'indexes':[],    
    },
    'STG_SBAC_ASMT': {'columns' : [
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
        ('name_pref_lvl_1', False, 'varchar(256)', '', True, "Performance Level 1"),
        ('name_pref_lvl_2', False, 'varchar(256)', '', True, "Performance Level 2"),
        ('name_pref_lvl_3', False, 'varchar(256)', '', True, "Performance Level 3"),
        ('name_pref_lvl_4', False, 'varchar(256)', '', True, "Performance Level 4"),
        ('name_pref_lvl_5', False, 'varchar(256)', '', True, "Performance Level 5"),
        ('score_cut_point_1', False, 'varchar(256)', '', True, "Cutpoint 1"),
        ('score_cut_point_2', False, 'varchar(256)', '', True, "Cutpoint 2"),
        ('score_cut_point_3', False, 'varchar(256)', '', True, "Cutpoint 3"),
        ('score_cut_point_4', False, 'varchar(256)', '', True, "Cutpoint 4"),
        ('create_date', False, 'timestamp', 'now()', False, "Date on which record is inserted"),
        ],
        'indexes':[],
        'keys':[],
    },
    'STG_SBAC_ASMT_OUTCOME': {'columns' : [
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
        ('create_date', False, 'timestamp', 'now()', False, "Date on which record is inserted"),   
        ],
        'indexes': [],
        'keys': []
    },
    'ERR_LIST': {'columns' :
        [
        ('record_sid', True, 'bigserial', '', False, "Sequential Auto-increment"),
        ('batch_id', False, 'bigint', '', False, "Batch ID which caused the record insert"),
        ('err_code', False, 'bigint', '', True, "Error Code"),
        ('err_source', False, 'bigint', '', True, "Pipeline Stage that inserted this error."),
        ('create_date', False, 'timestamp', 'now()', False, "Date on which record is inserted"),
        ],
        'indexes':[],
        'keys':[],
    }
}


def map_sql_type_to_sqlalchemy_type(sql_type):
    mapped_type = None
    sql_type_mapped_type = {
        'timestamp': TIMESTAMP,
        'bigint' : BIGINT,
        'bigserial': BIGINT,
        'varchar': VARCHAR,
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
        primary_key = ddl_tuple[1],
        nullable = ddl_tuple[4],
        server_default = ( text(ddl_tuple[3]) if (ddl_tuple[3] != '') else None ),
        doc = ddl_tuple[5],
    )
   # print(column)
    return column


def create_table(metadata, schema, table_name):
    column_ddl = UDL_TABLE_METADATA[table_name]['columns']
    arguments = [table_name, metadata]
    
    for c_ddl in column_ddl:
        #print(c_ddl)
        column = map_tuple_to_sqlalchemy_column(c_ddl)
        arguments.append(column)
    table = Table(*tuple(arguments), **{'schema':schema})
    return table


def _parse_args():
    parser = argparse.ArgumentParser('database')
    parser.add_argument('--config_file', dest='config_file')
    args = parser.parse_args()
    return args


def _get_db_url(udl2_conf):
    return "postgresql://%s:%s@%s/%s" % (udl2_conf['postgresql']['db_user'],
                                         udl2_conf['postgresql']['db_pass'],
                                         udl2_conf['postgresql']['db_host'],
                                         udl2_conf['postgresql']['db_database'])


def _create_engine(db_url):
    return create_engine(db_url)


def create_schema(udl2_conf, schema):
    pass


def create_foreign_data_wrapper_extension(udl2_conf):
    pass

def create_foreign_data_wrapper_server(udl2_conf):
    pass


if __name__ == '__main__':
    args = _parse_args()
    if args.config_file is None:
        config_path_file = UDL2_DEFAULT_CONFIG_PATH_FILE
    else:
        config_path_file = args.config_file
    udl2_conf = imp.load_source('udl2_conf', config_path_file)
    from udl2_conf import udl2_conf
        
    engine = _create_engine(_get_db_url(udl2_conf))
    udl2_metadata = MetaData()
    
    for table, definitions in UDL_TABLE_METADATA.items():
        print(table)
        tbl_err_list = create_table(udl2_metadata, udl2_conf['udl2_db']['staging_schema'], table)
        print(tbl_err_list)
        print(CreateTable(tbl_err_list))