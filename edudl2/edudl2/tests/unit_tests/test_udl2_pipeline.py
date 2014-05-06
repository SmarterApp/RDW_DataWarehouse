from edudl2.udl2.udl2_pipeline import get_pipeline_chain
from edudl2.udl2.celery import udl2_conf, udl2_flat_conf
from edudl2.database.udl2_connector import get_udl_connection, initialize_all_db
__author__ = 'swimberly'

import unittest
from celery import chain
from edudl2.udl2.constants import Constants

MESSAGE_KEYS = ['landing_zone_work_dir', 'load_type', 'parts', 'guid_batch', 'input_file_path']


class TestUDL2Pipeline(unittest.TestCase):

    def setUp(self):
        initialize_all_db(udl2_conf, udl2_flat_conf)
        self.udl_connector = get_udl_connection()
        batch_table = self.udl_connector.get_table(Constants.UDL2_BATCH_TABLE)
        self.udl_connector.execute(batch_table.delete())

    def test_get_pipeline_chain_check_type(self):
        arch_file = 'path_to_some_file'
        load_type = 'some_load_type'
        file_part = 12
        batc_guid = '1234-s5678'
        pipeline_chain = get_pipeline_chain(arch_file, load_type, file_part, batc_guid)
        self.assertIsInstance(pipeline_chain, chain)

    def test_get_pipeline_chain_check_msg(self):
        arch_file = 'path_to_some_file'
        load_type = 'some_load_type'
        file_part = 12
        batc_guid = '1234-s5678'
        pipeline_chain = get_pipeline_chain(arch_file, load_type, file_part, batc_guid)

        msg = pipeline_chain.tasks[0].args[0]

        for mk in MESSAGE_KEYS:
            self.assertIn(mk, msg)

    def test_get_pipeline_chain_check_msg_values(self):
        arch_file = 'path_to_some_file'
        load_type = 'some_load_type'
        file_part = 12
        batc_guid = '1234-s5678'
        pipeline_chain = get_pipeline_chain(arch_file, load_type, file_part, batc_guid)

        msg = pipeline_chain.tasks[0].args[0]
        self.assertEqual(msg['guid_batch'], batc_guid)
        self.assertEqual(msg['parts'], file_part)
        self.assertEqual(msg['input_file_path'], arch_file)
        self.assertEqual(msg['load_type'], load_type)


if __name__ == '__main__':
    unittest.main()
