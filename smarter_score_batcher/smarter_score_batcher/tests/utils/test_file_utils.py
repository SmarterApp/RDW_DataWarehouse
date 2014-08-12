'''
Created on Aug 12, 2014

@author: tosako
'''
import unittest
import tempfile
import uuid
import os
from smarter_score_batcher.utils.file_utils import file_writer, csv_file_writer
import hashlib
import csv


class Test(unittest.TestCase):

    def setUp(self):
        self.__temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.__temp_dir.cleanup()

    def test_file_writer_utf8(self):
        target = os.path.join(self.__temp_dir.name, str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()))
        russian = 'На берегу пустынных волн'
        mode = 0o750
        written = file_writer(target, russian, mode)
        self.assertTrue(written)
        m1 = hashlib.md5()
        m1.update(bytes(russian, 'utf-8'))
        d1 = m1.digest()
        m2 = hashlib.md5()
        with open(target, 'rb') as f:
            m2.update(f.read())
        d2 = m2.digest()
        self.assertEqual(d1, d2)

    def test_file_writer_ascii(self):
        target = os.path.join(self.__temp_dir.name, str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()))
        russian = 'Waves on the shore of the desert'
        written = file_writer(target, russian)
        self.assertTrue(written)
        m1 = hashlib.md5()
        m1.update(bytes(russian, 'utf-8'))
        d1 = m1.digest()
        m2 = hashlib.md5()
        with open(target, 'rb') as f:
            m2.update(f.read())
        d2 = m2.digest()
        self.assertEqual(d1, d2)

    def test_csv_file_writer_ascii(self):
        target = os.path.join(self.__temp_dir.name, str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()))
        rows = []
        new_rows = []
        for i in range(5):
            row = [str(i), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())]
            rows.append(row)
        written = csv_file_writer(target, rows)
        self.assertTrue(written)
        with open(target) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                new_rows.append(row)
        self.assertEqual(len(rows), len(rows))
        for i in range(len(rows)):
            self.assertListEqual(rows[i], new_rows[i])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
