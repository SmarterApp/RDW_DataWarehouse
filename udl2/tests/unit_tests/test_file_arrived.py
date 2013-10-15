__author__ = 'swimberly'

import unittest
import os

from udl2 import message_keys as mk
from filearrived import file_arrived


class TestFileArrived(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test__get_tenant_name_regular_directory(self):
        dir_name = '/home/person1/arrivals/ri/some_file.tgz'
        expected = 'ri'
        result = file_arrived._get_tenant_name(dir_name)

        self.assertEqual(result, expected)

    def test__get_tenant_name_no_directory(self):
        dir_name = 'shortstring'
        expected = ''
        result = file_arrived._get_tenant_name(dir_name)

        self.assertEqual(result, expected)

    def test__create_directory_paths_length(self):
        tenant_name = 'bob'
        batch_guid = 'guid123'
        result = file_arrived._create_directory_paths(tenant_name, batch_guid)

        self.assertEqual(len(result), 5)

    def test__create_directory_paths_dir_name(self):
        tenant_name = 'bob'
        batch_guid = 'guid123'
        result = file_arrived._create_directory_paths(tenant_name, batch_guid)

        dir_ending = os.path.split(result[mk.ARRIVED])[-1]
        expected = {
            mk.ARRIVED: '/opt/wgen/edware-udl/zones/landing/work/bob/arrived/' + dir_ending,
            mk.DECRYPTED: '/opt/wgen/edware-udl/zones/landing/work/bob/decrypted/' + dir_ending,
            mk.EXPANDED: '/opt/wgen/edware-udl/zones/landing/work/bob/expanded/' + dir_ending,
            mk.SUBFILES: '/opt/wgen/edware-udl/zones/landing/work/bob/subfiles/' + dir_ending,
            mk.HISTORY: '/opt/wgen/edware-udl/zones/landing/history/bob/' + dir_ending
        }

        self.assertDictEqual(expected, result)

    def test__create_batch_directories(self):
        pass

    def test__move_file_to_work_and_history(self):
        pass

    def test_move_file_from_arrivals(self):
        pass

