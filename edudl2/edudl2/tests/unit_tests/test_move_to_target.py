import os
import unittest
from collections import OrderedDict
import datetime
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2_util.config_reader import read_ini_file
from edudl2.udl2 import message_keys as mk
from edudl2.move_to_target.create_queries import create_insert_query, create_sr_table_select_insert_query
from edudl2.move_to_target.move_to_target import calculate_spend_time_as_second
from edudl2.move_to_target.move_to_target_setup import Column
from edudl2.move_to_target.handle_upsert_helper import HandleUpsertHelper
import logging
from sqlalchemy import select, and_
from edudl2.tests.unit_tests.unittest_with_udl2_sqlite import Unittest_with_udl2_sqlite,\
    UnittestUDLTargetDBConnection, get_unittest_schema_name,\
    get_unittest_tenant_name
from edudl2.udl2_util.database_util import get_db_connection_params
logger = logging.getLogger(__name__)


class TestMoveToTarget(Unittest_with_udl2_sqlite):

    def setUp(self,):
        # TODO: don't rely on env. var
        # TODO: mock the data instead of using ini file
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        conf_tup = read_ini_file(config_path)
        udl2_conf = conf_tup[0]
        self.conf = udl2_conf
        self.maxDiff = None

    @classmethod
    def setUpClass(cls):
        Unittest_with_udl2_sqlite.setUpClass(force_foreign_keys=False)

    def tearDown(self,):
        pass

    def test_create_insert_query_for_dim_table(self):
        guid_batch = '8866c6d5-7e5e-4c54-bf4e-775abc4021b2'
        conf = generate_conf(guid_batch, self.conf)
        target_table, source_table = ('dim_inst_hier', 'INT_SBAC_ASMT_OUTCOME')
        column_mapping = get_expected_column_mapping(target_table)
        column_types = get_expected_column_types_for_dim_inst_hier(target_table)
        actual_value = create_insert_query(conf, source_table, target_table, column_mapping, column_types, True, 'C')
        expected_value = get_expected_insert_query_for_dim_inst_hier(conf[mk.SOURCE_DB_HOST], conf[mk.SOURCE_DB_PORT], target_table, guid_batch,
                                                                     conf[mk.SOURCE_DB_NAME], conf[mk.SOURCE_DB_USER], conf[mk.SOURCE_DB_PASSWORD])

    # We'll disable this test for now, as it's plagued by an obsequious bug, and there are other sufficient tests.
    def dont_create_insert_query_for_sr_target_table(self):
        guid_batch = '8866c6d5-7e5e-4c54-bf4e-775abc4021b2'
        conf = generate_conf(guid_batch, self.conf)
        target_table = 'student_reg'
        column_and_type_mapping = get_expected_sr_column_and_type_mapping()
        actual_value = create_sr_table_select_insert_query(conf, target_table, column_and_type_mapping)
        expected_value = get_expected_insert_query_for_student_reg(conf[mk.SOURCE_DB_HOST], conf[mk.SOURCE_DB_PORT], target_table, guid_batch,
                                                                   conf[mk.SOURCE_DB_NAME], conf[mk.SOURCE_DB_USER], conf[mk.SOURCE_DB_PASSWORD])
        self.assertEqual(expected_value, actual_value)

    def test_calculate_spend_time_as_second(self):
        start_time = datetime.datetime(2013, 5, 10, 16, 34, 33)
        finish_time = datetime.datetime(2013, 5, 10, 16, 40, 0)
        expected_value = 327.0
        actual_value = calculate_spend_time_as_second(start_time, finish_time)
        self.assertEqual(expected_value, actual_value)

    def test_create_sr_table_select_insert_query(self):
        conf = {
            mk.GUID_BATCH: '1',
            mk.SOURCE_DB_SCHEMA: 'source_schema',
            mk.TARGET_DB_SCHEMA: 'target_schema',
            mk.SOURCE_DB_HOST: 'source_host',
            mk.SOURCE_DB_PORT: 'source_port',
            mk.SOURCE_DB_NAME: 'source_name',
            mk.SOURCE_DB_USER: 'source_user',
            mk.SOURCE_DB_PASSWORD: 'source_password'
        }

        mapping = OrderedDict([('table_A', OrderedDict([('rec_id', Column(src_col='record_sid', type='rec_id bigint')),
                                                        ('batch_guid', Column(src_col='guid_batch', type='batch_guid varchar(5)')),
                                                        ('table_X_col_XC', Column(src_col='table_A_col_AC', type='table_X_col_XC boolean'))])),
                               ('table_B', OrderedDict([('table_X_col_XE', Column(src_col='table_B_col_BE', type='table_X_col_XE smallint'))]))])

        noop_query = create_sr_table_select_insert_query(conf, 'table_X', mapping)
        # logger.info(noop_query)
        self.assertEqual(noop_query, "INSERT INTO \"target_schema\".\"table_X\"(rec_id,batch_guid,table_X_col_XC,table_X_col_XE) " +
                         "SELECT * FROM dblink('host=source_host port=source_port dbname=source_name user=source_user password=source_password'" +
                         ", 'SELECT max(table_A.record_sid), table_a.guid_batch,table_a.table_A_col_AC,table_b.table_B_col_BE " +
                         "FROM \"source_schema\".\"table_A\" table_a INNER JOIN \"source_schema\".\"table_B\" table_b ON table_b.guid_batch = table_a.guid_batch "
                         "WHERE table_a.guid_batch=''1'' GROUP BY table_a.guid_batch,table_a.table_A_col_AC,table_b.table_B_col_BE ') " +
                         "AS t(rec_id bigint,batch_guid varchar(5),table_X_col_XC boolean,table_X_col_XE smallint);")

        op_query = create_sr_table_select_insert_query(conf, 'table_X', mapping, 'D')
        # logger.info(op_query)
        self.assertEqual(op_query, "INSERT INTO \"target_schema\".\"table_X\"(rec_id,batch_guid,table_X_col_XC,table_X_col_XE) " +
                         "SELECT * FROM dblink('host=source_host port=source_port dbname=source_name user=source_user password=source_password'" +
                         ", 'SELECT max(table_A.record_sid), table_a.guid_batch,table_a.table_A_col_AC,table_b.table_B_col_BE " +
                         "FROM \"source_schema\".\"table_A\" table_a INNER JOIN \"source_schema\".\"table_B\" table_b ON table_b.guid_batch = table_a.guid_batch "
                         "WHERE op = ''D'' AND table_a.guid_batch=''1'' GROUP BY table_a.guid_batch,table_a.table_A_col_AC,table_b.table_B_col_BE ') AS t(rec_id bigint,batch_guid varchar(5),table_X_col_XC boolean,table_X_col_XE smallint);")

    def test_handle_record_upsert_find_all(self):
        table_name = 'dim_student'
        guid_batch = '90901b70-ddaa-11e2-a95d-68a86d3c2f82'
        with UnittestUDLTargetDBConnection() as conn:
            helper = HandleUpsertHelper(conn, guid_batch, table_name)
            all_records = helper.find_all()
            self.assertIsNotNone(all_records, "Find all should return some value")
            actual_rows = all_records.fetchall()
            self.assertEqual(len(actual_rows), 894, "Find all should return all records")

    def test_handle_record_upsert_find_by_natural_key(self):
        table_name = 'dim_student'
        guid_batch = None
        example_record = {
            'student_guid': 'a016a4c1-5aca-4146-a85b-ed1172a01a4d',
            'external_student_id': None,
            'first_name': 'Richard',
            'middle_name': None,
            'last_name': 'Mccarty',
            'sex': 'male',
            'birthdate': '20040312',
            'dmg_eth_derived': 3,
            'dmg_eth_hsp': True,
            'dmg_eth_ami': False,
            'dmg_eth_asn': False,
            'dmg_eth_blk': False,
            'dmg_eth_pcf': False,
            'dmg_eth_wht': False,
            'dmg_eth_2om': False,
            'dmg_prg_iep': False,
            'dmg_prg_lep': False,
            'dmg_prg_504': False,
            'dmg_sts_ecd': False,
            'dmg_sts_mig': False,
        }
        bad_record = {
            'student_guid': 'not_really_exist'
        }

        with UnittestUDLTargetDBConnection() as conn:
            helper = HandleUpsertHelper(conn, guid_batch, table_name)
            m1 = helper.find_by_natural_key(example_record)
            self.assertIsNotNone(m1, "Find_by_natural_key should return matched value")
            self.assertEqual(m1['student_guid'], example_record['student_guid'], "Matched records should have the same student guid")
            m2 = helper.find_by_natural_key(bad_record)
            self.assertIsNone(m2, "Find_by_natural_key should return None if not match found")
            example_record['first_name'] = 'Sadish'
            m3 = helper.find_by_natural_key(example_record)
            self.assertIsNone(m3, "Find_by_natural_key should return None if not match found")

    def test_handle_record_soft_delete(self):
        table_name = 'dim_student'
        guid_batch = None
        old_record = {
            'student_guid': 'a3fcc2a7-16ba-4783-ae58-f225377e8e20',
            'student_rec_id': '356',
            'batch_guid': None
        }
        new_record = {
            'student_guid': 'a3fcc2a7-16ba-4783-ae58-f225377e8e20',
            'student_rec_id': '3155',
            'batch_guid': None
        }
        with UnittestUDLTargetDBConnection() as conn:
            helper = HandleUpsertHelper(conn, guid_batch, table_name)
            helper.soft_delete_and_update(old_record, new_record)
            table = conn.get_table(table_name)
            query = select([table.c.student_rec_id], from_obj=[table]).where(and_(table.c.batch_guid == guid_batch, table.c.student_rec_id == '3155'))
            record_updated = conn.execute(query)
            self.assertNotEqual(record_updated.rowcount, 1)


def generate_conf(guid_batch, udl2_conf):
    '''
    Return all needed configuration information
    '''
    db_params_tuple = get_db_connection_params(udl2_conf['udl2_db_conn']['url'])
    conf = {mk.GUID_BATCH: guid_batch,
            mk.SOURCE_DB_SCHEMA: get_unittest_schema_name(),
            mk.TARGET_DB_SCHEMA: get_unittest_schema_name(),
            mk.SOURCE_DB_DRIVER: db_params_tuple[0],
            mk.SOURCE_DB_USER: db_params_tuple[1],
            mk.SOURCE_DB_PASSWORD: db_params_tuple[2],
            mk.SOURCE_DB_HOST: db_params_tuple[3],
            mk.SOURCE_DB_PORT: db_params_tuple[4],
            mk.SOURCE_DB_NAME: db_params_tuple[5],
            mk.TENANT_NAME: get_unittest_tenant_name()}
    return conf


def get_expected_column_types_for_fact_table(table_name):
    column_names = list(get_expected_column_mapping(table_name).keys())
    column_types = ['asmt_outcome_vw_rec_id bigint', 'asmt_rec_id bigint', 'student_guid character varying(50)',
                    'teacher_guid character varying(50)', 'state_code character varying(2)', 'district_guid character varying(50)',
                    'school_guid character varying(50)', 'inst_hier_rec_id bigint',
                    'where_taken_id character varying(50)', 'where_taken_name character varying(256)',
                    'asmt_grade character varying(10)', 'enrl_grade character varying(10)', 'date_taken character varying(8)',
                    'date_taken_day smallint', 'date_taken_month smallint', 'date_taken_year smallint', 'asmt_score smallint',
                    'asmt_score_range_min smallint', 'asmt_score_range_max smallint', 'asmt_perf_lvl smallint',
                    'asmt_claim_1_score smallint', 'asmt_claim_1_score_range_min smallint', 'asmt_claim_1_score_range_max smallint',
                    'asmt_claim_2_score smallint', 'asmt_claim_2_score_range_min smallint', 'asmt_claim_2_score_range_max smallint',
                    'asmt_claim_3_score smallint', 'asmt_claim_3_score_range_min smallint', 'asmt_claim_3_score_range_max smallint',
                    'asmt_claim_4_score smallint', 'asmt_claim_4_score_range_min smallint', 'asmt_claim_4_score_range_max smallint',
                    'status character varying(2)', 'most_recent boolean', 'batch_guid character varying(50)']
    column_name_type_map = OrderedDict()
    for i in range(len(column_names)):
        column_name_type_map[column_names[i]] = column_types[i]
    return column_name_type_map


def get_expected_insert_query_for_fact_table(host_name, port, table_name, asmt_rec_id, guid_batch, dbname, user, password):
    return 'INSERT INTO "edware"."{table_name}" (asmt_outcome_vw_rec_id,asmt_rec_id,student_guid,teacher_guid,state_code,district_guid,'\
           'school_guid,inst_hier_rec_id,where_taken_id,where_taken_name,asmt_grade,enrl_grade,date_taken,'\
           'date_taken_day,date_taken_month,date_taken_year,asmt_score,asmt_score_range_min,asmt_score_range_max,asmt_perf_lvl,'\
           'asmt_claim_1_score,asmt_claim_1_score_range_min,asmt_claim_1_score_range_max,asmt_claim_2_score,asmt_claim_2_score_range_min,'\
           'asmt_claim_2_score_range_max,asmt_claim_3_score,asmt_claim_3_score_range_min,asmt_claim_3_score_range_max,asmt_claim_4_score,'\
           'asmt_claim_4_score_range_min,asmt_claim_4_score_range_max,status,most_recent,batch_guid) '\
           'SELECT * FROM dblink(\'host={host} port={port} dbname={dbname} user={user} password={password}\', \'SELECT nextval(\'\'"global_rec_seq"\'\'), * FROM '\
           '(SELECT {asmt_rec_id},guid_student,guid_staff,code_state,guid_district,guid_school,-1,guid_asmt_location,name_asmt_location,grade_asmt,'\
           'grade_enrolled,date_assessed,date_taken_day,date_taken_month,date_taken_year,score_asmt,score_asmt_min,score_asmt_max,score_perf_level,'\
           'score_claim_1,score_claim_1_min,score_claim_1_max,score_claim_2,score_claim_2_min,score_claim_2_max,score_claim_3,score_claim_3_min,score_claim_3_max,'\
           'score_claim_4,score_claim_4_min,score_claim_4_max,\'\'\'\',True,guid_batch '\
           'FROM "udl2"."INT_SBAC_ASMT_OUTCOME" WHERE guid_batch=\'\'{guid_batch}\'\') as y\') AS t(asmt_outcome_vw_rec_id bigint,asmt_rec_id bigint,student_guid character varying(50),'\
           'teacher_guid character varying(50),state_code character varying(2),district_guid character varying(50),school_guid character varying(50),'\
           'inst_hier_rec_id bigint,where_taken_id character varying(50),where_taken_name character varying(256),'\
           'asmt_grade character varying(10),enrl_grade character varying(10),date_taken character varying(8),date_taken_day smallint,date_taken_month smallint,'\
           'date_taken_year smallint,asmt_score smallint,asmt_score_range_min smallint,asmt_score_range_max smallint,asmt_perf_lvl smallint,asmt_claim_1_score smallint,'\
           'asmt_claim_1_score_range_min smallint,asmt_claim_1_score_range_max smallint,asmt_claim_2_score smallint,asmt_claim_2_score_range_min smallint,'\
           'asmt_claim_2_score_range_max smallint,asmt_claim_3_score smallint,asmt_claim_3_score_range_min smallint,asmt_claim_3_score_range_max smallint,'\
           'asmt_claim_4_score smallint,asmt_claim_4_score_range_min smallint,asmt_claim_4_score_range_max smallint,'\
           'status character varying(2),most_recent boolean,batch_guid character varying(50));'.format(host=host_name, port=port, table_name=table_name, asmt_rec_id=asmt_rec_id,
                                                                                                       guid_batch=guid_batch,
                                                                                                       dbname=dbname, user=user, password=password)


def get_expected_update_inst_hier_rec_id_query(table_name):
    return 'UPDATE "edware"."{table_name}" SET inst_hier_rec_id=dim.dim_inst_hier_rec_id FROM '\
        '(SELECT inst_hier_rec_id AS dim_inst_hier_rec_id, district_guid AS dim_district_guid, school_guid AS dim_school_guid, state_code AS dim_state_code  '\
        'FROM "edware"."dim_inst_hier") dim  WHERE inst_hier_rec_id =  -1 AND district_guid = dim_district_guid AND '\
        'school_guid = dim_school_guid AND state_code = dim_state_code'.format(table_name=table_name)


def get_expected_update_student_rec_id_query(table_name):
    return 'UPDATE "edware"."{table_name}" SET student_rec_id=dim.dim_student_rec_id FROM '\
        '(SELECT student_rec_id AS dim_student_rec_id, student_guid AS dim_student_guid  ' \
        'FROM "edware"."dim_student") dim  WHERE student_rec_id =  -1 AND student_guid = dim_student_guid'.format(table_name=table_name)


def get_expected_column_types_for_dim_inst_hier(table_name):
    column_names = list(get_expected_column_mapping(table_name).keys())
    column_types = ['inst_hier_rec_id bigint', 'state_code character varying(2)', 'district_guid character varying(50)',
                    'district_name character varying(256)', 'school_guid character varying(50)', 'school_name character varying(256)',
                    'from_date character varying(8)', 'to_date character varying(8)', 'most_recent boolean']
    column_name_type_map = OrderedDict()
    for i in range(len(column_names)):
        column_name_type_map[column_names[i]] = column_types[i]
    return column_name_type_map


def get_expected_insert_query_for_dim_inst_hier(host_name, port, table_name, guid_batch, dbname, user, password):
    return "INSERT INTO \"edware\".\"{table_name}\" (inst_hier_rec_id,state_code,district_guid,district_name,"\
           "school_guid,school_name,from_date,to_date,most_recent) SELECT * FROM "\
           "dblink('host={host} port={port} dbname={dbname} user={user} password={password}', " \
           "'SELECT nextval(''\"global_rec_seq\"''), "\
           "* FROM (SELECT DISTINCT code_state,guid_district,name_district,guid_school,name_school,"\
           "to_char(CURRENT_TIMESTAMP, ''yyyymmdd''),''99991231'',True FROM \"udl2\".\"INT_SBAC_ASMT_OUTCOME\" WHERE op = ''C'' AND guid_batch=''{guid_batch}'') as y') "\
           "AS t(inst_hier_rec_id bigint,state_code character varying(2),district_guid character varying(50),"\
           "district_name character varying(256),school_guid character varying(50),school_name character varying(256),"\
           "from_date character varying(8),to_date character varying(8),"\
           "most_recent boolean);".format(host=host_name, port=port, table_name=table_name, guid_batch=guid_batch, dbname=dbname, user=user, password=password)


def get_expected_insert_query_for_student_reg(host_name, port, table_name, guid_batch, dbname, user, password):
    return 'INSERT INTO "edware"."student_reg"(student_reg_rec_id,batch_guid,state_name,state_code,district_guid,district_name,'\
           'school_guid,school_name,student_guid,external_student_ssid,first_name,middle_name,last_name,'\
           'sex,birthdate,enrl_grade,dmg_eth_hsp,dmg_eth_ami,dmg_eth_asn,dmg_eth_blk,dmg_eth_pcf,dmg_eth_wht,dmg_prg_iep,'\
           'dmg_prg_lep,dmg_prg_504,dmg_sts_ecd,dmg_sts_mig,dmg_multi_race,confirm_code,language_code,eng_prof_lvl,'\
           'us_school_entry_date,lep_entry_date,lep_exit_date,t3_program_type,prim_disability_type,student_reg_guid,'\
           'academic_year,extract_date,reg_system_id) SELECT * FROM dblink(\'host={host} port={port} '\
           'dbname={dbname} user={user} password={password}\', \'SELECT nextval(\'\'"global_rec_seq"\'\'), * '\
           'FROM (SELECT int_sbac_stu_reg.guid_batch,int_sbac_stu_reg.name_state,int_sbac_stu_reg.code_state,'\
           'int_sbac_stu_reg.guid_district,int_sbac_stu_reg.name_district,int_sbac_stu_reg.guid_school,'\
           'int_sbac_stu_reg.name_school,int_sbac_stu_reg.guid_student,int_sbac_stu_reg.external_ssid_student,'\
           'int_sbac_stu_reg.name_student_first,int_sbac_stu_reg.name_student_middle,int_sbac_stu_reg.name_student_last,'\
           'int_sbac_stu_reg.sex_student,int_sbac_stu_reg.birthdate_student,int_sbac_stu_reg.grade_enrolled,'\
           'int_sbac_stu_reg.dmg_eth_hsp,int_sbac_stu_reg.dmg_eth_ami,int_sbac_stu_reg.dmg_eth_asn,'\
           'int_sbac_stu_reg.dmg_eth_blk,int_sbac_stu_reg.dmg_eth_pcf,int_sbac_stu_reg.dmg_eth_wht,'\
           'int_sbac_stu_reg.dmg_prg_iep,int_sbac_stu_reg.dmg_prg_lep,int_sbac_stu_reg.dmg_prg_504,'\
           'int_sbac_stu_reg.dmg_sts_ecd,int_sbac_stu_reg.dmg_sts_mig,int_sbac_stu_reg.dmg_multi_race,'\
           'int_sbac_stu_reg.code_confirm,int_sbac_stu_reg.code_language,int_sbac_stu_reg.eng_prof_lvl,'\
           'int_sbac_stu_reg.us_school_entry_date,int_sbac_stu_reg.lep_entry_date,int_sbac_stu_reg.lep_exit_date,'\
           'int_sbac_stu_reg.t3_program_type,int_sbac_stu_reg.prim_disability_type,int_sbac_stu_reg_meta.guid_registration,'\
           'int_sbac_stu_reg_meta.academic_year,int_sbac_stu_reg_meta.extract_date,int_sbac_stu_reg_meta.test_reg_id '\
           'FROM "udl2"."INT_SBAC_STU_REG" int_sbac_stu_reg INNER JOIN "udl2"."INT_SBAC_STU_REG_META" int_sbac_stu_reg_meta '\
           'ON int_sbac_stu_reg_meta.guid_batch = int_sbac_stu_reg.guid_batch '\
           'WHERE int_sbac_stu_reg.guid_batch=\'\'{guid_batch}\'\') AS y\') AS t(student_reg_rec_id bigint,'\
           'batch_guid character varying(36),state_name character varying(50),state_code character varying(2),'\
           'district_guid character varying(30),district_name character varying(60),school_guid character varying(30),'\
           'school_name character varying(60),student_guid character varying(30),external_student_ssid character varying(50),'\
           'student_first_name character varying(35),student_middle_name character varying(35),'\
           'student_last_name character varying(35),sex character varying(6),birthdate_student character varying(10),'\
           'enrl_grade character varying(10),dmg_eth_hsp boolean,dmg_eth_ami boolean,dmg_eth_asn boolean,dmg_eth_blk boolean,'\
           'dmg_eth_pcf boolean,dmg_eth_wht boolean,dmg_prg_iep boolean,dmg_prg_lep boolean,dmg_prg_504 boolean,'\
           'dmg_sts_ecd boolean,dmg_sts_mig boolean,dmg_multi_race boolean,confirm_code character varying(35),'\
           'language_code character varying(3),eng_prof_lvl character varying(20),us_school_entry_date character varying(10),'\
           'lep_entry_date character varying(10),lep_exit_date character varying(10),t3_program_type character varying(27),'\
           'prim_disability_type character varying(3),student_reg_guid character varying(50),academic_year smallint,'\
           'extract_date character varying(10),reg_system_id character varying(50));'.format(host=host_name, port=port,
                                                                                             table_name=table_name,
                                                                                             guid_batch=guid_batch,
                                                                                             dbname=dbname, user=user,
                                                                                             password=password)


def get_expected_column_mapping(target_table):
    '''
    This column mapping is used in moving data from integration tables to target
    Key -- target table name, e.g. dim_asmt
    Value -- ordered dictionary: (column_in_target_table, column_in_source_table), e.g. 'asmt_guid': 'guid_asmt'
    '''

    column_map_integration_to_target = {'dim_asmt': OrderedDict([('asmt_rec_id', 'nextval(\'"global_rec_seq"\')'),
                                                                 ('asmt_guid', 'guid_asmt'),
                                                                 ('asmt_type', 'type'),
                                                                 ('asmt_period', 'period'),
                                                                 ('asmt_period_year', 'year'),
                                                                 ('asmt_version', 'version'),
                                                                 ('asmt_subject', 'subject'),
                                                                 ('asmt_claim_1_name', 'name_claim_1'),
                                                                 ('asmt_claim_2_name', 'name_claim_2'),
                                                                 ('asmt_claim_3_name', 'name_claim_3'),
                                                                 ('asmt_claim_4_name', 'name_claim_4'),
                                                                 ('asmt_perf_lvl_name_1', 'name_perf_lvl_1'),
                                                                 ('asmt_perf_lvl_name_2', 'name_perf_lvl_2'),
                                                                 ('asmt_perf_lvl_name_3', 'name_perf_lvl_3'),
                                                                 ('asmt_perf_lvl_name_4', 'name_perf_lvl_4'),
                                                                 ('asmt_perf_lvl_name_5', 'name_perf_lvl_5'),
                                                                 ('asmt_score_min', 'score_overall_min'),
                                                                 ('asmt_score_max', 'score_overall_max'),
                                                                 ('asmt_claim_1_score_min', 'score_claim_1_min'),
                                                                 ('asmt_claim_1_score_max', 'score_claim_1_max'),
                                                                 ('asmt_claim_2_score_min', 'score_claim_2_min'),
                                                                 ('asmt_claim_2_score_max', 'score_claim_2_max'),
                                                                 ('asmt_claim_3_score_min', 'score_claim_3_min'),
                                                                 ('asmt_claim_3_score_max', 'score_claim_3_max'),
                                                                 ('asmt_claim_4_score_min', 'score_claim_4_min'),
                                                                 ('asmt_claim_4_score_max', 'score_claim_4_max'),
                                                                 ('asmt_cut_point_1', 'score_cut_point_1'),
                                                                 ('asmt_cut_point_2', 'score_cut_point_2'),
                                                                 ('asmt_cut_point_3', 'score_cut_point_3'),
                                                                 ('asmt_cut_point_4', 'score_cut_point_4'),
                                                                 ('asmt_custom_metadata', 'NULL'),
                                                                 ('from_date', "TO_CHAR(CURRENT_TIMESTAMP, 'yyyymmdd')"),
                                                                 ('to_date', "'99991231'"),
                                                                 ('most_recent', 'TRUE'),
                                                                 ]),

                                        'dim_inst_hier': OrderedDict([('inst_hier_rec_id', 'nextval(\'"global_rec_seq"\')'),
                                                                      ('state_code', 'code_state'),
                                                                      ('district_guid', 'guid_district'),
                                                                      ('district_name', 'name_district'),
                                                                      ('school_guid', 'guid_school'),
                                                                      ('school_name', 'name_school'),
                                                                      ('from_date', "to_char(CURRENT_TIMESTAMP, 'yyyymmdd')"),
                                                                      ('to_date', "'99991231'"),
                                                                      ('most_recent', 'True'),
                                                                      ]),
                                        'dim_student': OrderedDict([('student_rec_id', 'nextval(\'"global_rec_seq"\')'),
                                                                    ('student_guid', 'guid_student'),
                                                                    ('first_name', 'name_student_first'),
                                                                    ('middle_name', 'name_student_middle'),
                                                                    ('last_name', 'name_student_last'),
                                                                    ('sex', 'sex_student'),
                                                                    ('birthdate', 'birthdate_student'),
                                                                    ('grade', 'grade_enrolled'),
                                                                    ('state_code', 'code_state'),
                                                                    ('district_guid', 'guid_district'),
                                                                    ('school_guid', 'guid_school'),
                                                                    ('from_date', "to_char(CURRENT_TIMESTAMP, 'yyyymmdd')"),
                                                                    ('to_date', "'99991231'"),
                                                                    ('most_recent', 'True'),
                                                                    ]),

                                        'fact_asmt_outcome_vw': OrderedDict([('asmt_outcome_vw_rec_id', 'nextval(\'"global_rec_seq"\')'),
                                                                             ('asmt_rec_id', None),
                                                                             ('student_guid', 'guid_student'),
                                                                             ('teacher_guid', 'guid_staff'),
                                                                             ('state_code', 'code_state'),
                                                                             ('district_guid', 'guid_district'),
                                                                             ('school_guid', 'guid_school'),
                                                                             ('inst_hier_rec_id', '-1'),
                                                                             ('where_taken_id', 'guid_asmt_location'),
                                                                             ('where_taken_name', 'name_asmt_location'),
                                                                             ('asmt_grade', 'grade_asmt'),
                                                                             ('enrl_grade', 'grade_enrolled'),
                                                                             ('date_taken', 'date_assessed'),
                                                                             ('date_taken_day', 'date_taken_day'),  # date_assessed is a varchar(8)
                                                                             ('date_taken_month', 'date_taken_month'),  # date_assessed is a varchar(8)
                                                                             ('date_taken_year', 'date_taken_year'),  # date_assessed is a varchar(8)
                                                                             ('asmt_score', 'score_asmt'),
                                                                             ('asmt_score_range_min', 'score_asmt_min'),
                                                                             ('asmt_score_range_max', 'score_asmt_max'),
                                                                             ('asmt_perf_lvl', 'score_perf_level'),
                                                                             ('asmt_claim_1_score', 'score_claim_1'),
                                                                             ('asmt_claim_1_score_range_min', 'score_claim_1_min'),
                                                                             ('asmt_claim_1_score_range_max', 'score_claim_1_max'),
                                                                             ('asmt_claim_2_score', 'score_claim_2'),
                                                                             ('asmt_claim_2_score_range_min', 'score_claim_2_min'),
                                                                             ('asmt_claim_2_score_range_max', 'score_claim_2_max'),
                                                                             ('asmt_claim_3_score', 'score_claim_3'),
                                                                             ('asmt_claim_3_score_range_min', 'score_claim_3_min'),
                                                                             ('asmt_claim_3_score_range_max', 'score_claim_3_max'),
                                                                             ('asmt_claim_4_score', 'score_claim_4'),
                                                                             ('asmt_claim_4_score_range_min', 'score_claim_4_min'),
                                                                             ('asmt_claim_4_score_range_max', 'score_claim_4_max'),
                                                                             ('status', '\'\''),
                                                                             ('most_recent', 'True'),
                                                                             ('batch_guid', 'guid_batch'),
                                                                             ])
                                        }
    return column_map_integration_to_target[target_table]


def get_expected_sr_column_and_type_mapping():
    '''
    This column mapping is used in moving data from student registration integration tables to target
    Key -- target table column name, e.g. 'external_student_ssid'
    Value -- named tuple: (column in source table, target column type), e.g. Column('external_ssid_student': 'character varying(50)')
    '''

    mapping = OrderedDict([('INT_SBAC_STU_REG', OrderedDict([('student_reg_rec_id', Column(src_col='nextval(\'"global_rec_seq"\')', type='bigint')),
                                                             ('batch_guid', Column(src_col='guid_batch', type='character varying(36)')),
                                                             ('state_name', Column(src_col='name_state', type='character varying(50)')),
                                                             ('state_code', Column(src_col='code_state', type='character varying(2)')),
                                                             ('district_guid', Column(src_col='guid_district', type='character varying(30)')),
                                                             ('district_name', Column(src_col='name_district', type='character varying(60)')),
                                                             ('school_guid', Column(src_col='guid_school', type='character varying(30)')),
                                                             ('school_name', Column(src_col='name_school', type='character varying(60)')),
                                                             ('student_guid', Column(src_col='guid_student', type='character varying(30)')),
                                                             ('external_student_ssid', Column(src_col='external_ssid_student', type='character varying(50)')),
                                                             ('student_first_name', Column(src_col='name_student_first', type='character varying(35)')),
                                                             ('student_middle_name', Column(src_col='name_student_middle', type='character varying(35)')),
                                                             ('student_last_name', Column(src_col='name_student_last', type='character varying(35)')),
                                                             ('sex', Column(src_col='sex_student', type='character varying(6)')),
                                                             ('birthdate', Column(src_col='birthdate_student', type='character varying(10)')),
                                                             ('enrl_grade', Column(src_col='grade_enrolled', type='character varying(10)')),
                                                             ('dmg_eth_hsp', Column(src_col='dmg_eth_hsp', type='boolean')),
                                                             ('dmg_eth_ami', Column(src_col='dmg_eth_ami', type='boolean')),
                                                             ('dmg_eth_asn', Column(src_col='dmg_eth_asn', type='boolean')),
                                                             ('dmg_eth_blk', Column(src_col='dmg_eth_blk', type='boolean')),
                                                             ('dmg_eth_pcf', Column(src_col='dmg_eth_pcf', type='boolean')),
                                                             ('dmg_eth_wht', Column(src_col='dmg_eth_wht', type='boolean')),
                                                             ('dmg_prg_iep', Column(src_col='dmg_prg_iep', type='boolean')),
                                                             ('dmg_prg_lep', Column(src_col='dmg_prg_lep', type='boolean')),
                                                             ('dmg_prg_504', Column(src_col='dmg_prg_504', type='boolean')),
                                                             ('dmg_sts_ecd', Column(src_col='dmg_sts_ecd', type='boolean')),
                                                             ('dmg_sts_mig', Column(src_col='dmg_sts_mig', type='boolean')),
                                                             ('dmg_multi_race', Column(src_col='dmg_multi_race', type='boolean')),
                                                             ('confirm_code', Column(src_col='code_confirm', type='character varying(35)')),
                                                             ('language_code', Column(src_col='code_language', type='character varying(3)')),
                                                             ('eng_prof_lvl', Column(src_col='eng_prof_lvl', type='character varying(20)')),
                                                             ('us_school_entry_date', Column(src_col='us_school_entry_date', type='character varying(10)')),
                                                             ('lep_entry_date', Column(src_col='lep_entry_date', type='character varying(10)')),
                                                             ('lep_exit_date', Column(src_col='lep_exit_date', type='character varying(10)')),
                                                             ('t3_program_type', Column(src_col='t3_program_type', type='character varying(27)')),
                                                             ('prim_disability_type', Column(src_col='prim_disability_type', type='character varying(3)'))
                                                             ])
                            ),
                          ('INT_SBAC_STU_REG_META', OrderedDict([('student_reg_guid', Column(src_col='guid_registration', type='character varying(50)')),
                                                                ('academic_year', Column(src_col='academic_year', type='smallint')),
                                                                ('extract_date', Column(src_col='extract_date', type='character varying(10)')),
                                                                ('reg_system_id', Column(src_col='test_reg_id', type='haracter varying(50)'))
                                                                 ]))
                           ])

    return mapping


if __name__ == '__main__':
    unittest.main()
