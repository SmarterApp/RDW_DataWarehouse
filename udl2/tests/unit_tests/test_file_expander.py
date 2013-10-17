__author__ = 'sravi'

import unittest
import os

from fileexpander import file_expander


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
