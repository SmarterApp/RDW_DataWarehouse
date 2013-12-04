'''
Created on Nov 7, 2013

@author: dip
'''
import unittest
from edextract.tasks.extract import archive, generate
import tempfile
import os
import shutil
from zipfile import ZipFile
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite


class TestExtractTask(Unittest_with_stats_sqlite):

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

    def test_generate(self):
        pass

    def test_archive(self):
        open(self.__tmp_zip, 'wb').write(archive('req_id', self.__tmp_dir))
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
        zipfile.close()

    def test_start_generate(self):
        # we probably can only test failure cases
        # test tenant is
        try:
            result = generate(tenant=None, request_id='0', public_key_id='swimberly',
                              task_id='1', query='select 0 from dual', output_file='/tmp/unittest.csv.gz.pgp')
            self.assertEqual(result, False)
        except Exception as e:
            self.assertEqual(True, True)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
