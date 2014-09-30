__author__ = 'tshewchuk'

import os
import shutil
import tempfile
from edudl2.get_load_type import get_load_type
from edudl2.tests.unit_tests import UDLUnitTestCase


class TestGetLoadType(UDLUnitTestCase):

    def setUp(self):
        self.test_expanded_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_expanded_dir)

    def test_get_load_type_from_valid_content(self):
        shutil.copy(os.path.join(self.data_dir, 'test_valid_content_type.json'), self.test_expanded_dir)
        value = get_load_type.get_load_type(self.test_expanded_dir)
        self.assertEqual('studentregistration', value)

    def test_get_load_type_from_invalid_content_json(self):
        shutil.copy(os.path.join(self.data_dir, 'test_invalid_content_type.json'), self.test_expanded_dir)
        self.assertRaises(ValueError, get_load_type.get_load_type, self.test_expanded_dir)
