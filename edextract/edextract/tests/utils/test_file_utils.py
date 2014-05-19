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
