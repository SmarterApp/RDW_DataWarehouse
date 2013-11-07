'''
Created on Nov 7, 2013

@author: tosako
'''
import unittest
import tempfile
import os
import shutil
from edextract.utils.file_archiver import archive_files
from zipfile import ZipFile


class Test(unittest.TestCase):

    def setUp(self):
        self.__files = ['a.txt', 'b.txt', 'c.txt']
        self.__tmp_dir = tempfile.mkdtemp('file_archiver_test')
        self.__tmp_zip = os.path.join(tempfile.mkdtemp('zip'), 'test.zip')
        for file in self.__files:
            with open(os.path.join(self.__tmp_dir, file), "w") as f:
                f.write('hello ' + file)

    def tearDown(self):
        shutil.rmtree(self.__tmp_dir)
        shutil.rmtree(os.path.dirname(self.__tmp_zip))

    def test_archive_files(self):
        archive_files(self.__tmp_zip, self.__tmp_dir)

        zipfile = ZipFile(self.__tmp_zip, "r")
        namelist = zipfile.namelist()
        self.assertEqual(3, len(namelist))
        self.assertIn('a.txt', namelist)
        self.assertIn('b.txt', namelist)
        self.assertIn('c.txt', namelist)

        file_a = zipfile.read('a.txt')
        self.assertEqual(b'hello a.txt', file_a)
        file_b = zipfile.read('b.txt')
        self.assertEqual(b'hello b.txt', file_b)
        file_c = zipfile.read('c.txt')
        self.assertEqual(b'hello c.txt', file_c)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
