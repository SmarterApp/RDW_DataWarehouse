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

from edudl2.fileexpander import file_expander
__author__ = 'sravi'

import unittest
import os


class TestFileExpander(unittest.TestCase):

    def setUp(self):
        self.test_file_name = '/tmp/some_file.tar.gz'

    def tearDown(self):
        # cleanup
        if os.path.isfile(self.test_file_name):
            os.remove(self.test_file_name)

    def test__is_file_exists_for_invalid_file(self):
        result = file_expander._is_file_exists(self.test_file_name)

        self.assertFalse(result)

    def test__is_file_exists_for_valid_file(self):
        open(self.test_file_name, 'w')
        self.assertTrue(os.path.isfile(self.test_file_name))
        result = file_expander._is_file_exists(self.test_file_name)
        self.assertTrue(result)

    def test__verify_valid_tar_file_contents(self):
        self.assertTrue(file_expander._verify_tar_file_contents(['test.csv', 'test.json']))

    def test__verify_missing_json(self):
        self.assertFalse(file_expander._verify_tar_file_contents(['test.csv']))

    def test__verify_missing_csv(self):
        self.assertFalse(file_expander._verify_tar_file_contents(['test.json']))

    def test__verify_missing_json_and_csv(self):
        self.assertFalse(file_expander._verify_tar_file_contents(['test.doc']))

    def test__verify_more_than_two_files(self):
        self.assertFalse(file_expander._verify_tar_file_contents(['test.json', 'test.csv', 'test2.csv']))

    def test__verify_two_files_with_missing_csv(self):
        self.assertFalse(file_expander._verify_tar_file_contents(['test.json', 'test.doc']))
