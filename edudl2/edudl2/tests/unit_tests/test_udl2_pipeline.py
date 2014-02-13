from edudl2.udl2.udl2_pipeline import get_pipeline_chain
__author__ = 'swimberly'

import unittest
from celery import chain

MESSAGE_KEYS = ['start_timestamp', 'landing_zone_work_dir', 'load_type', 'batch_table',
                'parts', 'guid_batch', 'input_file_path']


class TestUDL2Pipeline(unittest.TestCase):

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
