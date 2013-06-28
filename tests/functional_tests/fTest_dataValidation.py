import unittest
import imp
# config file is outside of the src folder. To access config file default file is created inside udl2 module
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from sqlalchemy import create_engine


config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
udl2_conf = imp.load_source('udl2_conf', config_path)
from udl2_conf import udl2_conf


#udl2 database connection from config file
udl2_driver = udl2_conf['udl2_db']['db_driver']
udl2_pass = udl2_conf['udl2_db']['db_pass']
udl2_host = udl2_conf['udl2_db']['db_host']
udl2_port = udl2_conf['udl2_db']['db_port']
udl2_user = udl2_conf['udl2_db']['db_user']
udl2_name = udl2_conf['udl2_db']['db_name']


#target database connection from config file
target_driver = udl2_conf['target_db']['db_driver']
target_pass = udl2_conf['target_db']['db_pass']
target_host = udl2_conf['target_db']['db_host']
target_port = udl2_conf['target_db']['db_port']
target_user = udl2_conf['target_db']['db_user']
target_name = udl2_conf['target_db']['db_database']

# connection string for udl2 & target db
udl2_db_connection_str = "%s://%s:%s@%s:%s/%s" % (udl2_driver, udl2_user, udl2_pass, udl2_host, udl2_port, udl2_name)
target_db_connection_str = "%s://%s:%s@%s:%s/%s" % (target_driver, target_user, target_pass, target_host, target_port, target_name)

# DB connection -->udl2 db
udl2_engine = create_engine(udl2_db_connection_str)
udl2_connection = udl2_engine.connect()

# DB connection -->target db
target_engine = create_engine(target_db_connection_str)
target_connection = target_engine.connect()


class UniuqeCount(unittest.TestCase):

    def test_unique_dist(self):
        # count unique district from staging table
        stg_district_count = udl2_connection.execute('select count(DISTINCT (guid_district)) as district_count from udl2."INT_SBAC_ASMT_OUTCOME"')
        stg_district_count_result = stg_district_count.fetchone()
        #Count unique district from dim_inst_hier table
        dim_district_count = target_connection.execute('select count(DISTINCT (district_guid)) as district_count from edware.dim_inst_hier')
        dim_district_count_result = dim_district_count.fetchone()
        assert stg_district_count_result == dim_district_count_result, "No. of districts are not equal in staging table and in dim_inst_hier table(star schema)"
        #Count unique district from fact_asmt_outcome table
        fact_district_count = target_connection.execute('select count(DISTINCT (district_guid)) as district_count from edware.fact_asmt_outcome')
        fact_district_count_result = fact_district_count.fetchone()
        assert stg_district_count_result == fact_district_count_result, "No. of districts are not equal in staging table and in fact_asmt_outcome table(star schema)"

    def test_unique_school(self):
        # count unique school from staging table
        stg_school_count = udl2_connection.execute('select count(DISTINCT (guid_school)) as school_count from udl2."INT_SBAC_ASMT_OUTCOME"')
        stg_school_count_result = stg_school_count.fetchone()
        #Count unique school from dim_inst_hier table
        dim_school_count = target_connection.execute('select count(DISTINCT (school_guid)) as school_count from edware.dim_inst_hier')
        dim_school_count_result = dim_school_count.fetchone()
        assert stg_school_count_result == dim_school_count_result, "No. of schools are not equal in staging table and in dim_inst_hier table(star schema)"
        #Count unique school from fact_asmt_outcome table
        fact_school_count = target_connection.execute('select count(DISTINCT (school_guid)) as school_count from edware.fact_asmt_outcome')
        fact_school_count_result = fact_school_count.fetchone()
        assert stg_school_count_result == fact_school_count_result, "No. of schools are not equal in staging table and in fact_asmt_outcome table(star schema)"

    def test_unique_state(self):
        # count unique state from staging table
        stg_state_count = udl2_connection.execute('select count(DISTINCT (code_state)) as state_count from udl2."INT_SBAC_ASMT_OUTCOME"')
        stg_state_count_result = stg_state_count.fetchone()
        #Count unique students from dim_inst_hier table
        dim_state_count = target_connection.execute('select count(DISTINCT (state_code)) as state_count from edware.dim_inst_hier')
        dim_state_count_result = dim_state_count.fetchone()
        assert stg_state_count_result == dim_state_count_result, "No. of states are not equal in staging table and in dim_inst_hier table(star schema)"
        #Count unique state from fact_asmt_outcome table
        fact_state_count = target_connection.execute('select count(DISTINCT (state_code)) as state_count from edware.fact_asmt_outcome')
        fact_state_count_result = fact_state_count.fetchone()
        assert stg_state_count_result == fact_state_count_result, "No. of states are not equal in staging table and in fact_asmt_outcome table(star schema)"

    def test_unique_asmt(self):
        #count unique asmt_guid from stg/INT SBAC_ASMT_OUTCOME table(s)
        stg_asmt_count = udl2_connection.execute('select count(DISTINCT (guid_asmt)) as assessment_count from udl2."INT_SBAC_ASMT_OUTCOME"')
        stg_asmt_count_result = stg_asmt_count.fetchone()
        #Count unique students from dim_asmt table
        dim_asmt_count = target_connection.execute('select count(DISTINCT (asmt_guid)) as assessment_count from edware.dim_asmt')
        dim_asmt_count_result = dim_asmt_count.fetchone()
        assert stg_asmt_count_result == dim_asmt_count_result, "No. of asmt_guid are not equal in staging table and in dim_asmt table(star schema)"
        #Count unique asmt from fact_asmt_outcome table
        #fact_asmt_count = target_connection.execute('select count(DISTINCT(asmt_guid)) as assessment_count from edware.fact_asmt_outcome')
        #fact_asmt_count_result = fact_asmt_count.fetchone()
        #assert stg_asmt_count_result == fact_asmt_count_result, "No. of asmt_guid are not equal in staging table and in fact_asmt_outcome table(star schema)"

    def test_unique_staff(self):
        # Count unique staff_guid from stg/INT SBAC_ASMT_OUTCOME table(s)
        stg_staff_count = udl2_connection.execute('select count (DISTINCT (guid_staff)) as staff_count from udl2."INT_SBAC_ASMT_OUTCOME" where type_staff = \'Teacher\'')
        stg_staff_count_result = stg_staff_count.fetchone()
        #Count unique students from dim_staff table
        dim_staff_count = target_connection.execute('select count (DISTINCT (staff_guid)) as staff_count from edware.dim_staff where hier_user_type = \'Teacher\'')
        dim_staff_count_result = dim_staff_count.fetchone()
        assert stg_staff_count_result == dim_staff_count_result, "No. of staff_guid are not equal in staging table and in dim_staff table(star schema)"
        #Count unique staff from fact_asmt_outcome table
        fact_staff_count = target_connection.execute('select count(DISTINCT(teacher_guid)) as teacher_count from edware.fact_asmt_outcome')
        fact_staff_count_result = fact_staff_count.fetchone()
        assert stg_staff_count_result == fact_staff_count_result, "No. of staff_guid are not equal in staging table and in fact_asmt_outcome table(star schema)"

    def test_unique_student(self):
        #Count unique students from stg/INT SBAC_ASMT_OUTCOME table(s)
        stg_student_count = udl2_connection.execute('select count (DISTINCT (guid_student)) as student_count from udl2."INT_SBAC_ASMT_OUTCOME"')
        stg_student_count_result = stg_student_count.fetchone()
        #Count unique students from dim_student table
        dim_student_count = target_connection.execute('select count (DISTINCT (student_guid)) as student_count from edware.dim_student')
        dim_student_count_result = dim_student_count.fetchone()
        assert stg_student_count_result == dim_student_count_result, "No. of student_guid are not equal in staging table and in dim_student table(star schema)"
        #Count unique student from fact_asmt_outcome table
        fact_student_count = target_connection.execute('select count(DISTINCT(student_guid)) as student_count from edware.fact_asmt_outcome')
        fact_student_count_result = fact_student_count.fetchone()
        assert stg_student_count_result == fact_student_count_result, "No. of students are not equal in staging table and in fact_asmt_outcome table(star schema)"
