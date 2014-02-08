from edudl2.file_finder.file_finder import find_files_in_directories,\
    create_extension
__author__ = 'swimberly'

import unittest
import os
import shutil
import time


TEST_FILE_DIR = '/tmp/test_file_finder'


class TestFileFinder(unittest.TestCase):

    def setUp(self):
        # TODO:  Make a temp directory w/ tempdir
        os.mkdir(TEST_FILE_DIR)
        self.test_files = ['zzzzzz.txt', 'jjjjjjj.jpg', 'aaaaaaa.txt']
        for file in self.test_files:
            with open(os.path.join(TEST_FILE_DIR, file), 'w'):
                pass
            time.sleep(1)

    def tearDown(self):
        shutil.rmtree(TEST_FILE_DIR)

    def test_find_files_in_directories(self):
        ordered_files = find_files_in_directories([TEST_FILE_DIR])
        expected_list = [os.path.join(TEST_FILE_DIR, x) for x in self.test_files]

        self.assertListEqual(ordered_files, expected_list)

    def test_find_files_in_directories_limited_num(self):
        ordered_files = find_files_in_directories([TEST_FILE_DIR], 1)
        expected_list = [os.path.join(TEST_FILE_DIR, x) for x in self.test_files[:1]]

        self.assertListEqual(ordered_files, expected_list)

    def test_find_files_in_directories_file_ext_1(self):
        ordered_files = find_files_in_directories([TEST_FILE_DIR], 1, 'jpg')
        expected_list = [os.path.join(TEST_FILE_DIR, x) for x in self.test_files[1:2]]

        self.assertListEqual(ordered_files, expected_list)

    def test_find_files_in_directories_file_ext_2(self):
        ordered_files = find_files_in_directories([TEST_FILE_DIR], 1, '.jpg')
        expected_list = [os.path.join(TEST_FILE_DIR, x) for x in self.test_files[1:2]]

        self.assertListEqual(ordered_files, expected_list)

    def test_find_files_in_directories_file_ext_3(self):
        ordered_files = find_files_in_directories([TEST_FILE_DIR], 1, '*.jpg')
        expected_list = [os.path.join(TEST_FILE_DIR, x) for x in self.test_files[1:2]]

        self.assertListEqual(ordered_files, expected_list)

    def test_find_files_in_directories_file_ext_4(self):
        ordered_files = find_files_in_directories([TEST_FILE_DIR], 0, '*jpg')
        expected_list = [os.path.join(TEST_FILE_DIR, x) for x in self.test_files[1:2]]

        self.assertListEqual(ordered_files, expected_list)

    def test_find_files_in_directories_file_ext_5(self):
        ordered_files = find_files_in_directories([TEST_FILE_DIR], 1, '*.jp')
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
