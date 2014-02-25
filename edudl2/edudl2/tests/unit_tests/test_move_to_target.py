import os
import unittest
from collections import OrderedDict
import datetime
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2_util.config_reader import read_ini_file
from edudl2.udl2 import message_keys as mk
from edudl2.move_to_target.create_queries import create_insert_query, create_multi_table_select_insert_query
from edudl2.move_to_target.move_to_target import calculate_spend_time_as_second,\
    create_queries_for_move_to_fact_table
from edudl2.move_to_target.move_to_target_conf import get_move_to_target_conf


class TestMoveToTarget(unittest.TestCase):

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

    def tearDown(self,):
        pass

    def test_create_queries_for_move_to_fact_table(self):
        guid_batch = '8866c6d5-7e5e-4c54-bf4e-775abc4021b2'
        conf = generate_conf(guid_batch, self.conf)
        source_table = 'INT_SBAC_ASMT_OUTCOME'
        target_table = 'fact_asmt_outcome'
        column_mapping = get_expected_column_mapping(target_table)
        # give value for 2 foreign keys
        column_mapping['asmt_rec_id'] = '100'
        column_mapping['section_rec_id'] = '1'
        column_types = get_expected_column_types_for_fact_table(target_table)

        expected_query_1 = 'ALTER TABLE \"edware\".\"{target_table}\" DISABLE TRIGGER ALL'.format(target_table=target_table)
        expected_query_2 = get_expected_insert_query_for_fact_table(conf[mk.SOURCE_DB_HOST], conf[mk.SOURCE_DB_PORT], target_table, column_mapping['asmt_rec_id'],
                                                                    column_mapping['section_rec_id'], guid_batch,
                                                                    conf[mk.SOURCE_DB_NAME], conf[mk.SOURCE_DB_USER], conf[mk.SOURCE_DB_PASSWORD])
        expected_query_3 = get_expected_update_inst_hier_rec_id_query(target_table)
        expected_query_4 = get_expected_update_student_rec_id_query(target_table)
        expected_query_5 = 'ALTER TABLE \"edware\".\"{target_table}\" ENABLE TRIGGER ALL'.format(target_table=target_table)
        expected_value = [expected_query_1, expected_query_2, expected_query_3, expected_query_4, expected_query_5]
        actual_value = create_queries_for_move_to_fact_table(conf, source_table, target_table, column_mapping, column_types)
        self.maxDiff = None
        self.assertEqual(len(expected_value), len(actual_value))
        for i in range(len(expected_value)):
            self.assertEqual(expected_value[i].strip(), actual_value[i].strip())

    def test_create_insert_query_for_dim_table(self):
        guid_batch = '8866c6d5-7e5e-4c54-bf4e-775abc4021b2'
        conf = generate_conf(guid_batch, self.conf)
        target_table, source_table = ('dim_inst_hier', 'INT_SBAC_ASMT_OUTCOME')
        column_mapping = get_expected_column_mapping(target_table)
        column_types = get_expected_column_types_for_dim_inst_hier(target_table)
        actual_value = create_insert_query(conf, source_table, target_table, column_mapping, column_types, True, 'C')
        expected_value = get_expected_insert_query_for_dim_inst_hier(conf[mk.SOURCE_DB_HOST], conf[mk.SOURCE_DB_PORT], target_table, guid_batch,
                                                                     conf[mk.SOURCE_DB_NAME], conf[mk.SOURCE_DB_USER], conf[mk.SOURCE_DB_PASSWORD])
        self.assertEqual(expected_value, actual_value)

    def test_create_insert_query_for_sr_target_table(self):
        guid_batch = '8866c6d5-7e5e-4c54-bf4e-775abc4021b2'
        conf = generate_conf(guid_batch, self.conf)
        target_table = 'student_reg'
        column_mappings = get_expected_column_mapping(target_table)
        column_types = get_expected_column_types_for_student_reg(target_table)
        actual_value = create_multi_table_select_insert_query(conf, target_table, column_mappings, column_types, True)
        expected_value = get_expected_insert_query_for_student_reg(conf[mk.SOURCE_DB_HOST], conf[mk.SOURCE_DB_PORT], target_table, guid_batch,
                                                                   conf[mk.SOURCE_DB_NAME], conf[mk.SOURCE_DB_USER], conf[mk.SOURCE_DB_PASSWORD])
        self.assertEqual(expected_value, actual_value)

    def test_calculate_spend_time_as_second(self):
        start_time = datetime.datetime(2013, 5, 10, 16, 34, 33)
        finish_time = datetime.datetime(2013, 5, 10, 16, 40, 0)
        expected_value = 327.0
        actual_value = calculate_spend_time_as_second(start_time, finish_time)
        self.assertEqual(expected_value, actual_value)


def generate_conf(guid_batch, udl2_conf):
    '''
    Return all needed configuration information
    '''
    conf = {  # add guid_batch from msg
              mk.GUID_BATCH: guid_batch,

              # source schema
              mk.SOURCE_DB_SCHEMA: udl2_conf['udl2_db']['integration_schema'],
              # source database setting
              mk.SOURCE_DB_HOST: udl2_conf['udl2_db']['db_host'],
              mk.SOURCE_DB_PORT: udl2_conf['udl2_db']['db_port'],
              mk.SOURCE_DB_USER: udl2_conf['udl2_db']['db_user'],
              mk.SOURCE_DB_NAME: udl2_conf['udl2_db']['db_database'],
              mk.SOURCE_DB_PASSWORD: udl2_conf['udl2_db']['db_pass'],

              # target schema
              mk.TARGET_DB_SCHEMA: udl2_conf['target_db']['db_schema'],
              # target database setting
              mk.TARGET_DB_HOST: udl2_conf['target_db']['db_host'],
              mk.TARGET_DB_PORT: udl2_conf['target_db']['db_port'],
              mk.TARGET_DB_USER: udl2_conf['target_db']['db_user'],
              mk.TARGET_DB_NAME: udl2_conf['target_db']['db_database'],
              mk.TARGET_DB_PASSWORD: udl2_conf['target_db']['db_pass'],
              mk.MOVE_TO_TARGET: get_move_to_target_conf()}
    return conf


def get_expected_column_types_for_fact_table(table_name):
    column_names = list(get_expected_column_mapping(table_name).keys())
    column_types = ['asmnt_outcome_rec_id bigint', 'asmt_rec_id bigint', 'student_guid character varying(50)',
                    'teacher_guid character varying(50)', 'state_code character varying(2)', 'district_guid character varying(50)',
                    'school_guid character varying(50)', 'section_guid character varying(50)', 'inst_hier_rec_id bigint',
                    'section_rec_id bigint', 'where_taken_id character varying(50)', 'where_taken_name character varying(256)',
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


def get_expected_insert_query_for_fact_table(host_name, port, table_name, asmt_rec_id, section_rec_id, guid_batch, dbname, user, password):
    return 'INSERT INTO "edware"."{table_name}"(asmnt_outcome_rec_id,asmt_rec_id,student_guid,teacher_guid,state_code,district_guid,'\
           'school_guid,section_guid,inst_hier_rec_id,section_rec_id,where_taken_id,where_taken_name,asmt_grade,enrl_grade,date_taken,'\
           'date_taken_day,date_taken_month,date_taken_year,asmt_score,asmt_score_range_min,asmt_score_range_max,asmt_perf_lvl,'\
           'asmt_claim_1_score,asmt_claim_1_score_range_min,asmt_claim_1_score_range_max,asmt_claim_2_score,asmt_claim_2_score_range_min,'\
           'asmt_claim_2_score_range_max,asmt_claim_3_score,asmt_claim_3_score_range_min,asmt_claim_3_score_range_max,asmt_claim_4_score,'\
           'asmt_claim_4_score_range_min,asmt_claim_4_score_range_max,status,most_recent,batch_guid) '\
           ' SELECT * FROM dblink(\'host={host} port={port} dbname={dbname} user={user} password={password}\', \'SELECT nextval(\'\'"GLOBAL_REC_SEQ"\'\'), * FROM '\
           '(SELECT {asmt_rec_id},guid_student,guid_staff,code_state,guid_district,guid_school,\'\'\'\',-1,{section_rec_id},guid_asmt_location,name_asmt_location,grade_asmt,'\
           'grade_enrolled,date_assessed,date_taken_day,date_taken_month,date_taken_year,score_asmt,score_asmt_min,score_asmt_max,score_perf_level,'\
           'score_claim_1,score_claim_1_min,score_claim_1_max,score_claim_2,score_claim_2_min,score_claim_2_max,score_claim_3,score_claim_3_min,score_claim_3_max,'\
           'score_claim_4,score_claim_4_min,score_claim_4_max,\'\'\'\',True,guid_batch '\
           'FROM "udl2"."INT_SBAC_ASMT_OUTCOME" WHERE op = \'\'C\'\' AND guid_batch=\'\'{guid_batch}\'\') as y\') AS t(asmnt_outcome_rec_id bigint,asmt_rec_id bigint,student_guid character varying(50),'\
           'teacher_guid character varying(50),state_code character varying(2),district_guid character varying(50),school_guid character varying(50),'\
           'section_guid character varying(50),inst_hier_rec_id bigint,section_rec_id bigint,where_taken_id character varying(50),where_taken_name character varying(256),'\
           'asmt_grade character varying(10),enrl_grade character varying(10),date_taken character varying(8),date_taken_day smallint,date_taken_month smallint,'\
           'date_taken_year smallint,asmt_score smallint,asmt_score_range_min smallint,asmt_score_range_max smallint,asmt_perf_lvl smallint,asmt_claim_1_score smallint,'\
           'asmt_claim_1_score_range_min smallint,asmt_claim_1_score_range_max smallint,asmt_claim_2_score smallint,asmt_claim_2_score_range_min smallint,'\
           'asmt_claim_2_score_range_max smallint,asmt_claim_3_score smallint,asmt_claim_3_score_range_min smallint,asmt_claim_3_score_range_max smallint,'\
           'asmt_claim_4_score smallint,asmt_claim_4_score_range_min smallint,asmt_claim_4_score_range_max smallint,'\
           'status character varying(2),most_recent boolean,batch_guid character varying(50));'.format(host=host_name, port=port, table_name=table_name, asmt_rec_id=asmt_rec_id,
                                                                                                       section_rec_id=section_rec_id, guid_batch=guid_batch,
                                                                                                       dbname=dbname, user=user, password=password)


def get_expected_update_inst_hier_rec_id_query(table_name):
    return 'UPDATE "edware"."{table_name}" SET inst_hier_rec_id=dim.dim_inst_hier_rec_id FROM '\
        '(SELECT inst_hier_rec_id AS dim_inst_hier_rec_id, district_guid AS dim_district_guid,school_guid AS dim_school_guid,state_code AS dim_state_code '\
        'FROM "edware"."dim_inst_hier") dim WHERE inst_hier_rec_id=-1 AND district_guid=dim_district_guid AND '\
        'school_guid=dim_school_guid AND state_code=dim_state_code'.format(table_name=table_name)


def get_expected_update_student_rec_id_query(table_name):
    return 'UPDATE "edware"."{table_name}" SET student_rec_id=dim.dim_student_rec_id FROM '\
        '(SELECT student_rec_id AS dim_student_rec_id, student_guid AS dim_student_guid ' \
        'FROM "edware"."dim_student") dim WHERE student_rec_id=-1 AND student_guid=dim_student_guid'.format(table_name=table_name)


def get_expected_column_types_for_dim_inst_hier(table_name):
    column_names = list(get_expected_column_mapping(table_name).keys())
    column_types = ['inst_hier_rec_id bigint', 'state_name character varying(32)', 'state_code character varying(2)', 'district_guid character varying(50)',
                    'district_name character varying(256)', 'school_guid character varying(50)', 'school_name character varying(256)',
                    'school_category character varying(20)', 'from_date character varying(8)', 'to_date character varying(8)', 'most_recent boolean']
    column_name_type_map = OrderedDict()
    for i in range(len(column_names)):
        column_name_type_map[column_names[i]] = column_types[i]
    return column_name_type_map


def get_expected_insert_query_for_dim_inst_hier(host_name, port, table_name, guid_batch, dbname, user, password):
    return 'INSERT INTO \"edware\"."{table_name}"(inst_hier_rec_id,state_name,state_code,district_guid,district_name,'\
           'school_guid,school_name,school_category,from_date,to_date,most_recent)  SELECT * FROM '\
           'dblink(\'host={host} port={port} dbname={dbname} user={user} password={password}\', \'SELECT nextval(\'\'"GLOBAL_REC_SEQ"\'\'), '\
           '* FROM (SELECT DISTINCT name_state,code_state,guid_district,name_district,guid_school,name_school,type_school,'\
           'to_char(CURRENT_TIMESTAMP, \'\'yyyymmdd\'\'),\'\'99991231\'\',True FROM "udl2"."INT_SBAC_ASMT_OUTCOME" WHERE op = \'\'C\'\' AND guid_batch=\'\'{guid_batch}\'\') as y\') '\
           'AS t(inst_hier_rec_id bigint,state_name character varying(32),state_code character varying(2),district_guid character varying(50),'\
           'district_name character varying(256),school_guid character varying(50),school_name character varying(256),'\
           'school_category character varying(20),from_date character varying(8),to_date character varying(8),'\
           'most_recent boolean);'.format(host=host_name, port=port, table_name=table_name, guid_batch=guid_batch, dbname=dbname, user=user, password=password)


def get_expected_column_types_for_student_reg(table_name):
    column_types = {'INT_SBAC_STU_REG':
                    ['student_reg_rec_id bigint', 'batch_guid character varying(36)', 'state_name character varying(50)',
                     'state_code character varying(2)', 'district_guid character varying(30)', 'district_name character varying(60)',
                     'school_guid character varying(30)', 'school_name character varying(60)', 'student_guid character varying(30)',
                     'external_student_ssid character varying(50)', 'student_first_name character varying(35)',
                     'student_middle_name character varying(35)', 'student_last_name character varying(35)', 'gender character varying(6)',
                     'student_dob character varying(10)', 'enrl_grade character varying(10)', 'dmg_eth_hsp boolean', 'dmg_eth_ami boolean',
                     'dmg_eth_asn boolean', 'dmg_eth_blk boolean', 'dmg_eth_pcf boolean', 'dmg_eth_wht boolean', 'dmg_prg_iep boolean',
                     'dmg_prg_lep boolean', 'dmg_prg_504 boolean', 'dmg_sts_ecd boolean', 'dmg_sts_mig boolean', 'dmg_multi_race boolean',
                     'confirm_code character varying(35)', 'language_code character varying(3)', 'eng_prof_lvl character varying(20)',
                     'us_school_entry_date character varying(10)', 'lep_entry_date character varying(10)',
                     'lep_exit_date character varying(10)', 't3_program_type character varying(27)',
                     'prim_disability_type character varying(3)'],
                    'INT_SBAC_STU_REG_META':
                    ['student_reg_guid character varying(50)', 'academic_year smallint', 'extract_date character varying(10)',
                     'reg_system_id character varying(50)']
                    }
    column_names = {}
    column_name_type_map = {}
    for source_table in get_expected_column_mapping(table_name).keys():
        column_names[source_table] = list(get_expected_column_mapping(table_name)[source_table].keys())
        column_name_type_map[source_table] = OrderedDict()
        for i in range(len(column_names[source_table])):
            column_name_type_map[source_table][column_names[source_table][i]] = column_types[source_table][i]
    return column_name_type_map


def get_expected_insert_query_for_student_reg(host_name, port, table_name, guid_batch, dbname, user, password):
    return 'INSERT INTO "edware"."student_reg"(student_reg_rec_id,batch_guid,state_name,state_code,district_guid,district_name,'\
           'school_guid,school_name,student_guid,external_student_ssid,student_first_name,student_middle_name,student_last_name,'\
           'gender,student_dob,enrl_grade,dmg_eth_hsp,dmg_eth_ami,dmg_eth_asn,dmg_eth_blk,dmg_eth_pcf,dmg_eth_wht,dmg_prg_iep,'\
           'dmg_prg_lep,dmg_prg_504,dmg_sts_ecd,dmg_sts_mig,dmg_multi_race,confirm_code,language_code,eng_prof_lvl,'\
           'us_school_entry_date,lep_entry_date,lep_exit_date,t3_program_type,prim_disability_type,student_reg_guid,'\
           'academic_year,extract_date,reg_system_id) SELECT * FROM dblink(\'host={host} port={port} '\
           'dbname={dbname} user={user} password={password}\', \'SELECT nextval(\'\'"GLOBAL_REC_SEQ"\'\'), * '\
           'FROM (SELECT DISTINCT int_sbac_stu_reg.guid_batch,int_sbac_stu_reg.name_state,int_sbac_stu_reg.code_state,'\
           'int_sbac_stu_reg.guid_district,int_sbac_stu_reg.name_district,int_sbac_stu_reg.guid_school,'\
           'int_sbac_stu_reg.name_school,int_sbac_stu_reg.guid_student,int_sbac_stu_reg.external_ssid_student,'\
           'int_sbac_stu_reg.name_student_first,int_sbac_stu_reg.name_student_middle,int_sbac_stu_reg.name_student_last,'\
           'int_sbac_stu_reg.gender_student,int_sbac_stu_reg.dob_student,int_sbac_stu_reg.grade_enrolled,'\
           'int_sbac_stu_reg.dmg_eth_hsp,int_sbac_stu_reg.dmg_eth_ami,int_sbac_stu_reg.dmg_eth_asn,'\
           'int_sbac_stu_reg.dmg_eth_blk,int_sbac_stu_reg.dmg_eth_pcf,int_sbac_stu_reg.dmg_eth_wht,'\
           'int_sbac_stu_reg.dmg_prg_iep,int_sbac_stu_reg.dmg_prg_lep,int_sbac_stu_reg.dmg_prg_504,'\
           'int_sbac_stu_reg.dmg_sts_ecd,int_sbac_stu_reg.dmg_sts_mig,int_sbac_stu_reg.dmg_multi_race,'\
           'int_sbac_stu_reg.code_confirm,int_sbac_stu_reg.code_language,int_sbac_stu_reg.eng_prof_lvl,'\
           'int_sbac_stu_reg.us_school_entry_date,int_sbac_stu_reg.lep_entry_date,int_sbac_stu_reg.lep_exit_date,'\
           'int_sbac_stu_reg.t3_program_type,int_sbac_stu_reg.prim_disability_type,int_sbac_stu_reg_meta.guid_registration,'\
           'int_sbac_stu_reg_meta.academic_year,int_sbac_stu_reg_meta.extract_date,int_sbac_stu_reg_meta.test_reg_id '\
           'FROM "udl2"."INT_SBAC_STU_REG" int_sbac_stu_reg,"udl2"."INT_SBAC_STU_REG_META" int_sbac_stu_reg_meta '\
           'WHERE int_sbac_stu_reg.guid_batch=\'\'{guid_batch}\'\') as y\') AS t(student_reg_rec_id bigint,'\
           'batch_guid character varying(36),state_name character varying(50),state_code character varying(2),'\
           'district_guid character varying(30),district_name character varying(60),school_guid character varying(30),'\
           'school_name character varying(60),student_guid character varying(30),external_student_ssid character varying(50),'\
           'student_first_name character varying(35),student_middle_name character varying(35),'\
           'student_last_name character varying(35),gender character varying(6),student_dob character varying(10),'\
           'enrl_grade character varying(10),dmg_eth_hsp boolean,dmg_eth_ami boolean,dmg_eth_asn boolean,dmg_eth_blk boolean,'\
           'dmg_eth_pcf boolean,dmg_eth_wht boolean,dmg_prg_iep boolean,dmg_prg_lep boolean,dmg_prg_504 boolean,'\
           'dmg_sts_ecd boolean,dmg_sts_mig boolean,dmg_multi_race boolean,confirm_code character varying(35),'\
           'language_code character varying(3),eng_prof_lvl character varying(20),us_school_entry_date character varying(10),'\
           'lep_entry_date character varying(10),lep_exit_date character varying(10),t3_program_type character varying(27),'\
           'prim_disability_type character varying(3),student_reg_guid character varying(50),academic_year smallint,'\
           'extract_date character varying(10),reg_system_id character varying(50));'.format(host=host_name, port=port, table_name=table_name,
                                                                                             guid_batch=guid_batch,
                                                                                             dbname=dbname, user=user,
                                                                                             password=password)


def get_expected_column_mapping(target_table):
    '''
    This column mapping is used in moving data from integration tables to target
    Key -- target table name, e.g. dim_asmt
    Value -- ordered dictionary: (column_in_target_table, column_in_source_table), e.g. 'asmt_guid': 'guid_asmt'
    '''

    column_map_integration_to_target = {'dim_asmt': OrderedDict([('asmt_rec_id', 'nextval(\'"GLOBAL_REC_SEQ"\')'),
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
                                                                 ('asmt_claim_1_score_weight', 'score_claim_1_weight'),
                                                                 ('asmt_claim_2_score_min', 'score_claim_2_min'),
                                                                 ('asmt_claim_2_score_max', 'score_claim_2_max'),
                                                                 ('asmt_claim_2_score_weight', 'score_claim_2_weight'),
                                                                 ('asmt_claim_3_score_min', 'score_claim_3_min'),
                                                                 ('asmt_claim_3_score_max', 'score_claim_3_max'),
                                                                 ('asmt_claim_3_score_weight', 'score_claim_3_weight'),
                                                                 ('asmt_claim_4_score_min', 'score_claim_4_min'),
                                                                 ('asmt_claim_4_score_max', 'score_claim_4_max'),
                                                                 ('asmt_claim_4_score_weight', 'score_claim_4_weight'),
                                                                 ('asmt_cut_point_1', 'score_cut_point_1'),
                                                                 ('asmt_cut_point_2', 'score_cut_point_2'),
                                                                 ('asmt_cut_point_3', 'score_cut_point_3'),
                                                                 ('asmt_cut_point_4', 'score_cut_point_4'),
                                                                 ('asmt_custom_metadata', 'NULL'),
                                                                 ('from_date', "TO_CHAR(CURRENT_TIMESTAMP, 'yyyymmdd')"),
                                                                 ('to_date', "'99991231'"),
                                                                 ('most_recent', 'TRUE'),
                                                                 ]),

                                        'dim_inst_hier': OrderedDict([('inst_hier_rec_id', 'nextval(\'"GLOBAL_REC_SEQ"\')'),
                                                                      ('state_name', 'name_state'),
                                                                      ('state_code', 'code_state'),
                                                                      ('district_guid', 'guid_district'),
                                                                      ('district_name', 'name_district'),
                                                                      ('school_guid', 'guid_school'),
                                                                      ('school_name', 'name_school'),
                                                                      ('school_category', 'type_school'),
                                                                      ('from_date', "to_char(CURRENT_TIMESTAMP, 'yyyymmdd')"),
                                                                      ('to_date', "'99991231'"),
                                                                      ('most_recent', 'True'),
                                                                      ]),
                                        'dim_student': OrderedDict([('student_rec_id', 'nextval(\'"GLOBAL_REC_SEQ"\')'),
                                                                    ('student_guid', 'guid_student'),
                                                                    ('first_name', 'name_student_first'),
                                                                    ('middle_name', 'name_student_middle'),
                                                                    ('last_name', 'name_student_last'),
                                                                    ('address_1', 'address_student_line1'),
                                                                    ('address_2', 'address_student_line2'),
                                                                    ('city', 'address_student_city'),
                                                                    ('zip_code', 'address_student_zip'),
                                                                    ('gender', 'gender_student'),
                                                                    ('email', 'email_student'),
                                                                    ('dob', 'dob_student'),
                                                                    # TODO: the fake value for 'section_guid' will be replaced by reading from conf
                                                                    ('section_guid', '\'\''),
                                                                    ('grade', 'grade_enrolled'),
                                                                    ('state_code', 'code_state'),
                                                                    ('district_guid', 'guid_district'),
                                                                    ('school_guid', 'guid_school'),
                                                                    ('from_date', "to_char(CURRENT_TIMESTAMP, 'yyyymmdd')"),
                                                                    ('to_date', "'99991231'"),
                                                                    ('most_recent', 'True'),
                                                                    ]),

                                        'dim_staff': OrderedDict([('staff_rec_id', 'nextval(\'"GLOBAL_REC_SEQ"\')'),
                                                                  ('staff_guid', 'guid_staff'),
                                                                  ('first_name', 'name_staff_first'),
                                                                  ('middle_name', 'name_staff_middle'),
                                                                  ('last_name', 'name_staff_last'),
                                                                  # TODO: the fake value for 'section_guid' will be replaced by reading from conf
                                                                  ('section_guid', '\'\''),
                                                                  ('hier_user_type', 'type_staff'),
                                                                  ('state_code', 'code_state'),
                                                                  ('district_guid', 'guid_district'),
                                                                  ('school_guid', 'guid_school'),
                                                                  ('from_date', "to_char(CURRENT_TIMESTAMP, 'yyyymmdd')"),
                                                                  ('to_date', "'99991231'"),
                                                                  ('most_recent', 'True'),
                                                                  ]),

                                        'fact_asmt_outcome': OrderedDict([('asmnt_outcome_rec_id', 'nextval(\'"GLOBAL_REC_SEQ"\')'),
                                                                          ('asmt_rec_id', None),
                                                                          ('student_guid', 'guid_student'),
                                                                          ('teacher_guid', 'guid_staff'),
                                                                          ('state_code', 'code_state'),
                                                                          ('district_guid', 'guid_district'),
                                                                          ('school_guid', 'guid_school'),
                                                                          ('section_guid', '\'\''),
                                                                          ('inst_hier_rec_id', '-1'),
                                                                          ('section_rec_id', None),
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
                                                                          ]),

                                        'student_reg':
                                            OrderedDict([
                                                ('INT_SBAC_STU_REG',
                                                 OrderedDict([('student_reg_rec_id', 'nextval(\'"GLOBAL_REC_SEQ"\')'),
                                                              ('batch_guid', 'guid_batch'),
                                                              ('state_name', 'name_state'),
                                                              ('state_code', 'code_state'),
                                                              ('district_guid', 'guid_district'),
                                                              ('district_name', 'name_district'),
                                                              ('school_guid', 'guid_school'),
                                                              ('school_name', 'name_school'),
                                                              ('student_guid', 'guid_student'),
                                                              ('external_student_ssid', 'external_ssid_student'),
                                                              ('student_first_name', 'name_student_first'),
                                                              ('student_middle_name', 'name_student_middle'),
                                                              ('student_last_name', 'name_student_last'),
                                                              ('gender', 'gender_student'),
                                                              ('student_dob', 'dob_student'),
                                                              ('enrl_grade', 'grade_enrolled'),
                                                              ('dmg_eth_hsp', 'dmg_eth_hsp'),
                                                              ('dmg_eth_ami', 'dmg_eth_ami'),
                                                              ('dmg_eth_asn', 'dmg_eth_asn'),
                                                              ('dmg_eth_blk', 'dmg_eth_blk'),
                                                              ('dmg_eth_pcf', 'dmg_eth_pcf'),
                                                              ('dmg_eth_wht', 'dmg_eth_wht'),
                                                              ('dmg_prg_iep', 'dmg_prg_iep'),
                                                              ('dmg_prg_lep', 'dmg_prg_lep'),
                                                              ('dmg_prg_504', 'dmg_prg_504'),
                                                              ('dmg_sts_ecd', 'dmg_sts_ecd'),
                                                              ('dmg_sts_mig', 'dmg_sts_mig'),
                                                              ('dmg_multi_race', 'dmg_multi_race'),
                                                              ('confirm_code', 'code_confirm'),
                                                              ('language_code', 'code_language'),
                                                              ('eng_prof_lvl', 'eng_prof_lvl'),
                                                              ('us_school_entry_date', 'us_school_entry_date'),
                                                              ('lep_entry_date', 'lep_entry_date'),
                                                              ('lep_exit_date', 'lep_exit_date'),
                                                              ('t3_program_type', 't3_program_type'),
                                                              ('prim_disability_type', 'prim_disability_type')
                                                             ])
                                                ),
                                                ('INT_SBAC_STU_REG_META',
                                                 OrderedDict([('student_reg_guid', 'guid_registration'),
                                                              ('academic_year', 'academic_year'),
                                                              ('extract_date', 'extract_date'),
                                                              ('reg_system_id', 'test_reg_id'),
                                                              ])
                                                )
                                            ])
                                        }
    return column_map_integration_to_target[target_table]

if __name__ == '__main__':
    unittest.main()
