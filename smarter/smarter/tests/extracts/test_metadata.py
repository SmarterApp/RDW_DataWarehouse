'''
Created on Dec 5, 2013

@author: dip
'''
import unittest
from smarter.reports.helpers.constants import Constants
from smarter.extracts.metadata import get_metadata_file_name, get_asmt_metadata
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    UnittestEdcoreDBConnection, get_unittest_tenant_name
from pyramid.testing import DummyRequest
from pyramid.registry import Registry
from pyramid import testing
from edauth.tests.test_helper.create_session import create_test_session
from edauth.security.user import RoleRelation
from pyramid.security import Allow
import edauth


class TestMetadata(Unittest_with_edcore_sqlite):

    def setUp(self):
        self.reg = Registry()
        self.reg.settings = {'extract.work_zone_base_dir': '/tmp/work_zone',
                             'pickup.gatekeeper.t1': '/t/acb',
                             'pickup.gatekeeper.t2': '/a/df',
                             'pickup.gatekeeper.y': '/a/c',
                             'pickup.sftp.hostname': 'hostname.local.net',
                             'pickup.sftp.user': 'myUser',
                             'pickup.sftp.private_key_file': '/home/users/myUser/.ssh/id_rsa'}
        # Set up user context
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with unittest_with_sqlite
        self.__config = testing.setUp(registry=self.reg, request=self.__request, hook_zca=False)
        defined_roles = [(Allow, 'STATE_EDUCATION_ADMINISTRATOR_1', ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        # Set up context security
        dummy_session = create_test_session(['STATE_EDUCATION_ADMINISTRATOR_1'])
        dummy_session.set_user_context([RoleRelation("STATE_EDUCATION_ADMINISTRATOR_1", get_unittest_tenant_name(), "NC", "228", "242")])
        self.__config.testing_securitypolicy(dummy_session)

    def tearDown(self):
        # reset the registry
        testing.tearDown()

    def test_get_metadata_file_name(self):
        params = {Constants.STATECODE: 'UT',
                  Constants.ASMTGUID: 'abc',
                  Constants.ASMTGRADE: '5',
                  Constants.ASMTSUBJECT: 'dd',
                  Constants.ASMTTYPE: 'bb'}
        filename = get_metadata_file_name(params)
        self.assertEqual(filename, 'METADATA_ASMT_UT_GRADE_5_DD_BB_abc.json')

    def test_get_asmt_metadata_query(self):
        asmt_guid = '20'
        query = get_asmt_metadata('NC', asmt_guid)
        self.assertIsNotNone(query)
        self.assertIn('dim_asmt.asmt_guid', str(query._whereclause))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
