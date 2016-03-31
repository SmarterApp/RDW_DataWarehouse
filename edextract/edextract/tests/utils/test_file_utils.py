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
Created on Nov 12, 2013

@author: dip
'''
import unittest
import os
import shutil
from edextract.utils.file_utils import prepare_path
import tempfile


class Test_FileUtils(unittest.TestCase):

    def setUp(self):
        self.__temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.__temp_dir, ignore_errors=True)

    def test_prepare_path(self):
        file_name = os.path.join(self.__temp_dir, 'a', 'b', 'c', 'test.csv.gpg')
        # make sure directory does not exist first.
        shutil.rmtree(os.path.dirname(file_name), ignore_errors=True)
        prepare_path(file_name)
        self.assertTrue(os.access(os.path.dirname(file_name), os.R_OK))


if __name__ == "__main__":
    unittest.main()
