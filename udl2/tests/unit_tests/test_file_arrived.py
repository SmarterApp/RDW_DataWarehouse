__author__ = 'swimberly'

import unittest
import os

from udl2 import message_keys as mk
from filearrived import file_arrived
from udl2.celery import udl2_conf

WORK = udl2_conf['zones']['work']
HIST = udl2_conf['zones']['history']


class TestFileArrived(unittest.TestCase):

    def test__get_tenant_name_regular_directory(self):
        dir_name = '/home/person1/arrivals/ri/some_user/file_drop/some_file.tgz'
        expected = 'ri'
        result = file_arrived.get_tenant_name(dir_name, -4)

        self.assertEqual(result, expected)

    def test__create_directory_paths_length(self):
        tenant_name = 'bob'
        batch_guid = 'guid123'
        result = file_arrived.create_directory_paths(tenant_name, batch_guid)

        self.assertEqual(len(result), 5)

    def test__create_directory_paths_dir_name(self):
        tenant_name = 'bob'
        batch_guid = 'guid123'
        result = file_arrived.create_directory_paths(tenant_name, batch_guid)

        dir_ending = os.path.split(result[mk.ARRIVED])[-1]
        expected = {
            mk.ARRIVED: os.path.join(WORK, 'bob', 'arrived', dir_ending),
            mk.DECRYPTED: os.path.join(WORK, 'bob', 'decrypted', dir_ending),
            mk.EXPANDED: os.path.join(WORK, 'bob', 'expanded', dir_ending),
            mk.SUBFILES: os.path.join(WORK, 'bob', 'subfiles', dir_ending),
            mk.HISTORY: os.path.join(HIST, 'bob', dir_ending),
        }

        self.assertDictEqual(expected, result)

    def test__create_batch_directories(self):
        directories = {
            'dir1': '/tmp/udl2_test1',
            'dir2': '/tmp/udl2_test2/',
            'dir3': '/tmp/udl2_test3'
        }

        for directory in directories.values():
            self.assertFalse(os.path.isdir(directory))

        file_arrived.create_batch_directories(directories)

        for directory in directories.values():
            self.assertTrue(os.path.isdir(directory))
            os.rmdir(directory)

    def test__move_file_to_work_and_history(self):
        incoming_file = '/tmp/udl2_test1.txt'
        arrived_dir = '/tmp/udl2_test_arrived'
        history_dir = '/tmp/udl2_test_history'
        os.mkdir(arrived_dir)
        os.mkdir(history_dir)
        open(incoming_file, 'w')
        self.assertTrue(os.path.isfile(incoming_file))
        file_arrived.move_file_to_work_and_history(incoming_file, arrived_dir, history_dir)

        self.assertFalse(os.path.isfile(incoming_file))
        self.assertTrue(os.path.isfile(os.path.join(arrived_dir, 'udl2_test1.txt')))
        self.assertTrue(os.path.isfile(os.path.join(history_dir, 'udl2_test1.txt')))

        # cleanup
        os.remove(os.path.join(arrived_dir, 'udl2_test1.txt'))
        os.remove(os.path.join(history_dir, 'udl2_test1.txt'))
        os.rmdir(arrived_dir)
        os.rmdir(history_dir)

    def test_move_file_from_arrivals(self):
        incoming_file = '/tmp/udl2_test1.txt'
        batch_guid = 'guid1234'
        open(incoming_file, 'w')

        result1, result2 = file_arrived.move_file_from_arrivals(incoming_file, batch_guid, -2)
        self.assertEqual(len(result1), 5)
        self.assertEqual(result2, 'tmp')

        # cleanup
        os.remove(os.path.join(result1[mk.ARRIVED], 'udl2_test1.txt'))
        os.remove(os.path.join(result1[mk.HISTORY], 'udl2_test1.txt'))
        for directory in result1.values():
            os.rmdir(directory)
