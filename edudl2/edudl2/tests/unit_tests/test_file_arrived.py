# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

__author__ = 'swimberly'

import unittest
import os
import tempfile
from edudl2.filearrived import file_arrived
from edudl2.udl2 import message_keys as mk
from edudl2.udl2.celery import udl2_conf

WORK = udl2_conf['zones']['work']
HIST = udl2_conf['zones']['history']


class TestFileArrived(unittest.TestCase):

    def test_create_directory_paths_length(self):
        tenant_name = 'bob'
        batch_guid = 'guid123'
        result = file_arrived.create_directory_paths(tenant_name, batch_guid)

        self.assertEqual(len(result), 5)

    def test_create_directory_paths_dir_name(self):
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

    def test_create_batch_directories(self):
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

    def test_move_file_to_work(self):
        incoming_file = '/tmp/udl2_test1.txt'
        arrived_dir = '/tmp/udl2_test_arrived'
        os.mkdir(arrived_dir)
        open(incoming_file, 'w')
        self.assertTrue(os.path.isfile(incoming_file))
        file_arrived.move_file_to_work(incoming_file, arrived_dir)

        self.assertFalse(os.path.isfile(incoming_file))
        self.assertTrue(os.path.isfile(os.path.join(arrived_dir, 'udl2_test1.txt')))

        # cleanup
        os.remove(os.path.join(arrived_dir, 'udl2_test1.txt'))
        os.rmdir(arrived_dir)

    def test_move_file_from_arrivals(self):
        batch_guid = 'guid1234'
        with tempfile.TemporaryDirectory() as tmpdir:
            arrivals_dir = tmpdir + '/arrivals'
            work_dir = tmpdir + '/work'
            history_dir = tmpdir + '/history'
            file_drop = arrivals_dir + '/ca/user/file_drop'
            os.mkdir(arrivals_dir)
            os.mkdir(work_dir)
            os.mkdir(history_dir)
            udl2_conf['zones']['arrivals'] = arrivals_dir
            udl2_conf['zones']['work'] = work_dir
            udl2_conf['zones']['history'] = history_dir
            os.makedirs(file_drop)
            tmpfile = tempfile.NamedTemporaryFile(dir=file_drop, delete=False)
            result1 = file_arrived.move_file_from_arrivals(tmpfile.name, batch_guid, 'ca')
            self.assertEqual(len(result1), 5)
