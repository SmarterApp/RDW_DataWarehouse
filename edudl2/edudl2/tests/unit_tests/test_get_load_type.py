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
