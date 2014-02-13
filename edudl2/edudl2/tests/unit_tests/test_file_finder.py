from edudl2.file_finder.file_finder import find_files_in_directories,\
    create_extension
import tempfile
import time
__author__ = 'swimberly'

import unittest
import os
import shutil


class TestFileFinder(unittest.TestCase):

    def setUp(self):
        self.create_data()

    def create_data(self, wait=0):
        self.__temp_dir = tempfile.mkdtemp()
        self.test_files = ['zzzzzz.txt', 'jjjjjjj.jpg', 'aaaaaaa.txt']
        for file in self.test_files:
            with open(os.path.join(self.__temp_dir, file), 'w') as f:
                f.write('test')
                time.sleep(wait)

    def tearDown(self):
        shutil.rmtree(self.__temp_dir)

    def test_find_files_in_directories(self):
        ordered_files = find_files_in_directories([self.__temp_dir])
        expected_list = [os.path.join(self.__temp_dir, x) for x in self.test_files]
        self.assertEqual(len(ordered_files), len(expected_list))
        for f in ordered_files:
            self.assertIn(f, expected_list)

    def test_find_files_in_directories_limited_num(self):
        shutil.rmtree(self.__temp_dir)
        self.create_data(1)
        ordered_files = find_files_in_directories([self.__temp_dir], 1)
        expected_list = [os.path.join(self.__temp_dir, x) for x in self.test_files[:1]]

        self.assertListEqual(ordered_files, expected_list)

    def test_find_files_in_directories_file_ext_1(self):
        ordered_files = find_files_in_directories([self.__temp_dir], 1, 'jpg')
        expected_list = [os.path.join(self.__temp_dir, x) for x in self.test_files[1:2]]

        self.assertListEqual(ordered_files, expected_list)

    def test_find_files_in_directories_file_ext_2(self):
        ordered_files = find_files_in_directories([self.__temp_dir], 1, '.jpg')
        expected_list = [os.path.join(self.__temp_dir, x) for x in self.test_files[1:2]]

        self.assertListEqual(ordered_files, expected_list)

    def test_find_files_in_directories_file_ext_3(self):
        ordered_files = find_files_in_directories([self.__temp_dir], 1, '*.jpg')
        expected_list = [os.path.join(self.__temp_dir, x) for x in self.test_files[1:2]]

        self.assertListEqual(ordered_files, expected_list)

    def test_find_files_in_directories_file_ext_4(self):
        ordered_files = find_files_in_directories([self.__temp_dir], 0, '*jpg')
        expected_list = [os.path.join(self.__temp_dir, x) for x in self.test_files[1:2]]

        self.assertListEqual(ordered_files, expected_list)

    def test_find_files_in_directories_file_ext_5(self):
        ordered_files = find_files_in_directories([self.__temp_dir], 1, '*.jp')
        expected_list = []

        self.assertListEqual(ordered_files, expected_list)

    def test_create_extension_1(self):
        result = create_extension('txt')
        self.assertEqual(result, '*.txt')

    def test_create_extension_2(self):
        result = create_extension('.txt')
        self.assertEqual(result, '*.txt')

    def test_create_extension_3(self):
        result = create_extension('*.txt')
        self.assertEqual(result, '*.txt')
if __name__ == '__main__':
    unittest.main()
