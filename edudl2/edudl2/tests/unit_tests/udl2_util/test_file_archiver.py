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

'''
Created on Mar 22, 2015

@author: tosako
'''
import unittest
import tempfile
import os
from edudl2.udl2_util.file_archiver import archive_files
from unittest.mock import patch
from boto.exception import S3CreateError


class Test(unittest.TestCase):

    def setUp(self):
        self.__files = ['file1.tar.gz.gpg', 'file2.tar.gz.gpg', os.path.join('abc', 'file3.tar.gz.gpg'), os.path.join('abc', 'file4.tar.gz.gpg'), os.path.join('abc', 'efg', 'file5.tar.gz.gpg'), os.path.join('abc', 'efg', 'file6.tar.gz.gpg')]
        self.__src_files = []
        self.__dest_files = []
        self.__prefix = '1234'
        self.__tmp_dir = tempfile.TemporaryDirectory()
        self.__src_dir = os.path.join(self.__tmp_dir.name, 'arrival')
        self.__backup_dir = os.path.join(self.__tmp_dir.name, 'backup')
        for file in self.__files:
            filename = os.path.join(self.__tmp_dir.name, 'arrival', file)
            self.__src_files.append(filename)
            self.__dest_files.append(os.path.join(self.__prefix, self.__prefix, file))
            dirname = os.path.dirname(filename)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            open(os.path.join(filename), 'w').close()

    def tearDown(self):
        self.__tmp_dir.cleanup()

    @patch('edudl2.udl2_util.file_archiver.time.strftime')
    @patch('edudl2.udl2_util.file_archiver.S3_buckup.archive')
    @patch('edudl2.udl2_util.file_archiver.S3_buckup.__init__')
    def test_archive_files_ok(self, mock_S3_buckup, mock_archive, mock_strftime):
        mock_strftime.return_value = self.__prefix
        mock_S3_buckup.return_value = None
        mock_archive.return_value = True
        rtn = archive_files(self.__src_dir, 's3_bucket', 1, prefix=self.__prefix, backup_of_backup=self.__backup_dir)
        self.assertTrue(rtn)
        self.assertFalse(os.path.exists(self.__backup_dir))
        arg_list = mock_archive.call_args_list
        self.assertEqual(6, len(arg_list))
        for arg in arg_list:
            args, kwargs = arg
            (src_file, dest_file) = args
            self.assertIn(src_file, self.__src_files)
            self.assertIn(dest_file, self.__dest_files)

    @patch('edudl2.udl2_util.file_archiver.time.strftime')
    @patch('edudl2.udl2_util.file_archiver.S3_buckup.archive')
    @patch('edudl2.udl2_util.file_archiver.S3_buckup.__init__')
    def test_archive_file_s3_not_available(self, mock_S3_buckup, mock_archive, mock_strftime):
        mock_strftime.return_value = self.__prefix
        mock_S3_buckup.side_effect = S3CreateError(403, '')
        rtn = archive_files(self.__src_dir, 's3_bucket', 1, prefix=self.__prefix, backup_of_backup=self.__backup_dir)
        self.assertFalse(rtn)
        arg_list = mock_archive.call_args_list
        self.assertEqual(0, len(arg_list))
        self.assertTrue(os.path.exists(self.__backup_dir))
        backup_filenames = []
        for dirpath, dirs, files in os.walk(self.__backup_dir):
            for filename in files:
                fname = os.path.abspath(os.path.join(dirpath, filename))
                backup_filenames.append(fname[len(self.__backup_dir) + 1:])
        self.assertEqual(6, len(backup_filenames))
        for file in backup_filenames:
            self.assertIn(file, self.__dest_files)

    @patch('edudl2.udl2_util.file_archiver.time.strftime')
    @patch('edudl2.udl2_util.file_archiver.S3_buckup.archive')
    @patch('edudl2.udl2_util.file_archiver.S3_buckup.__init__')
    def test_archive_file_from_backup_file(self, mock_S3_buckup, mock_archive, mock_strftime):
        mock_S3_buckup.return_value = None
        mock_archive.return_value = True
        mock_strftime.return_value = self.__prefix
        rtn = archive_files(os.path.join(self.__tmp_dir.name, 'arrival'), 's3_bucket', 1, prefix=self.__prefix, backup_of_backup=self.__src_dir)
        self.assertTrue(rtn)
        arg_list = mock_archive.call_args_list
        self.assertEqual(6, len(arg_list))
        for arg in arg_list:
            args, kwargs = arg
            (src_file, dest_file) = args
            self.assertIn(src_file, self.__src_files)
            self.assertIn(dest_file, self.__dest_files)

    @patch('edudl2.udl2_util.file_archiver.S3_buckup.archive')
    @patch('edudl2.udl2_util.file_archiver.S3_buckup.__init__')
    def test_archive_file_backup_to_backup(self, mock_S3_buckup, mock_archive):
        mock_S3_buckup.return_value = None
        mock_archive.return_value = False
        rtn = archive_files(self.__src_dir, 's3_bucket', 1, prefix=self.__prefix, backup_of_backup=self.__backup_dir)
        self.assertFalse(rtn)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
