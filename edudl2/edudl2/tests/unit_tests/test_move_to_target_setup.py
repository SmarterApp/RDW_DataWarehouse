__author__ = 'smuhit'

import unittest
import os
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2_util.config_reader import read_ini_file
from edudl2.udl2 import message_keys as mk
from edudl2.move_to_target.move_to_target_setup import get_table_and_column_mapping
from collections import OrderedDict


class TestMoveToTargetSetup(unittest.TestCase):

    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE

        conf_tup = read_ini_file(config_path)
        self.udl2_conf = conf_tup[0]

    def test_get_table_and_column_mapping(self):
        conf = {
            mk.SOURCE_DB_SCHEMA: self.udl2_conf['udl2_db']['integration_schema'],
            mk.REF_TABLE: self.udl2_conf['udl2_db']['sr_ref_table_name'],
            mk.PHASE: 4
        }
        expected_table_map = {'fact_student_reg': 'INT_SBAC_STU_REG_META'}
        expected_column_map = {'fact_student_reg': OrderedDict([('student_reg_rec_id', 'nextval(\'"GLOBAL_REC_SEQ"\')'), ('dmg_sts_ecd', 'dmg_sts_ecd'), ('enrl_grade', 'grade_enrolled'), ('language_code', 'code_language'), ('external_student_ssid', 'external_ssid_student'), ('student_guid', 'guid_student'), ('student_middle_name', 'name_student_middle'), ('us_school_entry_date', 'us_school_entry_date'), ('extract_date', 'extract_date'), ('state_code', 'code_state'), ('dmg_eth_blk', 'dmg_eth_blk'), ('dmg_prg_504', 'dmg_prg_504'), ('school_guid', 'guid_school'), ('dmg_eth_wht', 'dmg_eth_wht'), ('lep_entry_date', 'lep_entry_date'), ('dmg_eth_ami', 'dmg_eth_ami'), ('dmg_prg_iep', 'dmg_prg_iep'), ('district_name', 'name_district'), ('lep_exit_date', 'lep_exit_date'), ('dmg_eth_hsp', 'dmg_eth_hsp'), ('student_reg_guid', 'guid_registration'), ('dmg_prg_lep', 'dmg_prg_lep'), ('state_name', 'name_state'), ('dmg_eth_pcf', 'dmg_eth_pcf'), ('t3_program_type', 't3_program_type'), ('district_guid', 'guid_district'), ('gender', 'gender_student'), ('eng_prof_lvl', 'eng_prof_lvl'), ('prim_disability_type', 'prim_disability_type'), ('dmg_sts_mig', 'dmg_sts_mig'), ('dmg_eth_asn', 'dmg_eth_asn'), ('student_last_name', 'name_student_last'), ('student_dob', 'dob_student'), ('school_name', 'name_school'), ('academic_year', 'academic_year'), ('confirm_code', 'code_confirm'), ('reg_system_id', 'test_reg_id'), ('batch_guid', 'guid_batch'), ('student_first_name', 'name_student_first'), ('dmg_multi_race', 'dmg_multi_race')])}
        table_map, column_map = get_table_and_column_mapping(conf)
        self.assertEqual(table_map, expected_table_map)
        self.assertEqual(column_map, expected_column_map)
