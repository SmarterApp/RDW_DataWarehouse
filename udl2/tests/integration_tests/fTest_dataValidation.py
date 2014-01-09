import unittest
import imp
# config file is outside of the src folder. To access config file default file is created inside udl2 module
from udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from sqlalchemy import create_engine
from udl2 import database


class UniuqeCount(unittest.TestCase):

    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = imp.load_source('udl2_conf', config_path)
        from udl2_conf import udl2_conf
        self.udl2_conf = udl2_conf
        self.udl2_connection, self.udl2_engine = database._create_conn_engine(self.udl2_conf['udl2_db'])
        self.target_connection, self.target_engine = database._create_conn_engine(self.udl2_conf['target_db'])

    def tearDown(self):
        self.udl2_connection.close()
        self.target_connection.close()

    def test_unique_dist(self):
        # count unique district from staging table
        stg_district_count = self.udl2_connection.execute('select count(DISTINCT (guid_district)) as district_count from udl2."INT_SBAC_ASMT_OUTCOME"')
        stg_district_count_result = stg_district_count.fetchone()
        stg_dist_count = stg_district_count_result[0]
        #Count unique district from dim_inst_hier table
        dim_district_count = self.target_connection.execute('select count(DISTINCT (district_guid)) as district_count from edware.dim_inst_hier')
        dim_district_count_result = dim_district_count.fetchone()
        # Due to fake data in dim_inst_hier table, remove 1 row.
        dim_dist_count = dim_district_count_result[0] - 1
        print(dim_dist_count)
        assert stg_dist_count == dim_dist_count, "No. of districts are not equal in staging table and in dim_inst_hier table(star schema)"
        #Count unique district from fact_asmt_outcome table
        fact_district_count = self.target_connection.execute('select count(DISTINCT (district_guid)) as district_count from edware.fact_asmt_outcome')
        fact_district_count_result = fact_district_count.fetchone()
        assert stg_district_count_result == (fact_district_count_result), "No. of districts are not equal in staging table and in fact_asmt_outcome table(star schema)"

    def test_unique_school(self):
        # count unique school from staging table
        stg_school_count = self.udl2_connection.execute('select count(DISTINCT (guid_school)) as school_count from udl2."INT_SBAC_ASMT_OUTCOME"')
        stg_school_count_result = stg_school_count.fetchone()
        stg_school_count_new = stg_school_count_result[0]
        #Count unique school from dim_inst_hier table
        dim_school_count = self.target_connection.execute('select count(DISTINCT (school_guid)) as school_count from edware.dim_inst_hier')
        dim_school_count_result = dim_school_count.fetchone()
        # Due to fake data in dim_inst_hier ,removing 1 row
        dim_school_count_new = dim_school_count_result[0] - 1
        assert stg_school_count_new == dim_school_count_new, "No. of schools are not equal in staging table and in dim_inst_hier table(star schema)"
        #Count unique school from fact_asmt_outcome table
        fact_school_count = self.target_connection.execute('select count(DISTINCT (school_guid)) as school_count from edware.fact_asmt_outcome')
        fact_school_count_result = fact_school_count.fetchone()
        assert stg_school_count_result == fact_school_count_result, "No. of schools are not equal in staging table and in fact_asmt_outcome table(star schema)"

    def test_unique_state(self):
        # count unique state from staging table
        stg_state_count = self.udl2_connection.execute('select count(DISTINCT (code_state)) as state_count from udl2."INT_SBAC_ASMT_OUTCOME"')
        stg_state_count_result = stg_state_count.fetchone()
        stg_state_count_new = stg_state_count_result[0]
        #Count unique students from dim_inst_hier table
        dim_state_count = self.target_connection.execute('select count(DISTINCT (state_code)) as state_count from edware.dim_inst_hier')
        dim_state_count_result = dim_state_count.fetchone()
        # Due to fake data in dim_inst_hier, removing 1 row
        dim_state_count_new = dim_state_count_result[0] - 1
        assert stg_state_count_new == dim_state_count_new, "No. of states are not equal in staging table and in dim_inst_hier table(star schema)"
        #Count unique state from fact_asmt_outcome table
        fact_state_count = self.target_connection.execute('select count(DISTINCT (state_code)) as state_count from edware.fact_asmt_outcome')
        fact_state_count_result = fact_state_count.fetchone()
        assert stg_state_count_result == fact_state_count_result, "No. of states are not equal in staging table and in fact_asmt_outcome table(star schema)"

    def test_unique_asmt(self):
        #count unique asmt_guid from stg/INT SBAC_ASMT_OUTCOME table(s)
        stg_asmt_count = self.udl2_connection.execute('select count(DISTINCT (guid_asmt)) as assessment_count from udl2."INT_SBAC_ASMT_OUTCOME"')
        stg_asmt_count_result = stg_asmt_count.fetchone()
        #Count unique students from dim_asmt table
        dim_asmt_count = self.target_connection.execute('select count(DISTINCT (asmt_guid)) as assessment_count from edware.dim_asmt')
        dim_asmt_count_result = dim_asmt_count.fetchone()
        assert stg_asmt_count_result == dim_asmt_count_result, "No. of asmt_guid are not equal in staging table and in dim_asmt table(star schema)"
        #Count unique asmt from fact_asmt_outcome table
        #fact_asmt_count = self.target_connection.execute('select count(DISTINCT(asmt_guid)) as assessment_count from edware.fact_asmt_outcome')
        #fact_asmt_count_result = fact_asmt_count.fetchone()
        #assert stg_asmt_count_result == fact_asmt_count_result, "No. of asmt_guid are not equal in staging table and in fact_asmt_outcome table(star schema)"

# #     def test_unique_staff(self):
#         # Count unique staff_guid from stg/INT SBAC_ASMT_OUTCOME table(s)
#         stg_staff_count = self.udl2_connection.execute('select count (DISTINCT (guid_staff)) as staff_count from udl2."INT_SBAC_ASMT_OUTCOME" where type_staff = \'Teacher\'')
#         stg_staff_count_result = stg_staff_count.fetchone()
#         #Count unique students from dim_staff table
#         dim_staff_count = self.target_connection.execute('select count (DISTINCT (staff_guid)) as staff_count from edware.dim_staff where hier_user_type = \'Teacher\'')
#         dim_staff_count_result = dim_staff_count.fetchone()
#         assert stg_staff_count_result == dim_staff_count_result, "No. of staff_guid are not equal in staging table and in dim_staff table(star schema)"
#         #Count unique staff from fact_asmt_outcome table
#         fact_staff_count = self.target_connection.execute('select count(DISTINCT(teacher_guid)) as teacher_count from edware.fact_asmt_outcome')
#         fact_staff_count_result = fact_staff_count.fetchone()
#         assert stg_staff_count_result == fact_staff_count_result, "No. of staff_guid are not equal in staging table and in fact_asmt_outcome table(star schema)"

    def test_unique_student(self):
        #Count unique students from stg/INT SBAC_ASMT_OUTCOME table(s)
        stg_student_count = self.udl2_connection.execute('select count (DISTINCT (guid_student)) as student_count from udl2."INT_SBAC_ASMT_OUTCOME"')
        stg_student_count_result = stg_student_count.fetchone()
        #Count unique students from dim_student table
        dim_student_count = self.target_connection.execute('select count (DISTINCT (student_guid)) as student_count from edware.dim_student')
        dim_student_count_result = dim_student_count.fetchone()
        assert stg_student_count_result == dim_student_count_result, "No. of student_guid are not equal in staging table and in dim_student table(star schema)"
        #Count unique student from fact_asmt_outcome table
        fact_student_count = self.target_connection.execute('select count(DISTINCT(student_guid)) as student_count from edware.fact_asmt_outcome')
        fact_student_count_result = fact_student_count.fetchone()
        assert stg_student_count_result == fact_student_count_result, "No. of students are not equal in staging table and in fact_asmt_outcome table(star schema)"
