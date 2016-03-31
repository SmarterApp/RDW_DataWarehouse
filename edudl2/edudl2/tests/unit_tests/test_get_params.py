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

__author__ = 'ablum'

import os
import shutil
import tempfile
from edudl2.get_params import get_params
from edudl2.udl2.defaults import UDL2_DEFAULT_CONFIG_PATH_FILE
from edudl2.udl2_util.config_reader import read_ini_file
from edudl2.tests.unit_tests import UDLUnitTestCase


class TestGetParam(UDLUnitTestCase):

    def setUp(self):
        try:
            config_path = dict(os.environ)['UDL2_CONF']
        except Exception:
            config_path = UDL2_DEFAULT_CONFIG_PATH_FILE
        udl2_conf = read_ini_file(config_path)
        if isinstance(udl2_conf, tuple):
            self.conf = udl2_conf[0]
        else:
            self.conf = udl2_conf
        self.test_expanded_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_expanded_dir)

    def test_get_callback_params_from_valid_loadtype(self):
        shutil.copy(os.path.join(self.data_dir, 'test_valid_content_type.json'), self.test_expanded_dir)
        student_reg_guid, reg_system_id, callback_url, emailnotification = get_params.get_callback_params_for_studentregistration(self.test_expanded_dir)
        self.assertEqual('009a34ee-4609-4b13-8ca2-ed1bc0386afb', student_reg_guid)
        self.assertEqual('800b3654-4406-4a90-9591-be84b67054df', reg_system_id)
        self.assertEqual('StateTestReg.gov/StuReg/CallBack', callback_url)
        self.assertIsNone(emailnotification)

    def test_get_callback_params_from_invalid_loadtype(self):
        shutil.copy(os.path.join(self.data_dir, 'test_valid_content_type.json'), self.test_expanded_dir)
        callback_url, emailnotification = get_params.get_callback_params_for_assessment(self.test_expanded_dir)
        self.assertEqual(None, callback_url)
        self.assertEqual(None, emailnotification)

    def test_academic_year_param(self):
        shutil.copy(os.path.join(self.data_dir, 'test_valid_content_type.json'), self.test_expanded_dir)
        academic_year = get_params.get_academic_year_param(self.test_expanded_dir)
        self.assertEquals(2015, academic_year)
