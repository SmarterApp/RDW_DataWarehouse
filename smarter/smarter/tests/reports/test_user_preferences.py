'''
Created on Aug 5, 2013

@author: dawu
'''
import unittest
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    get_unittest_tenant_name
from edapi.tests.dummy import DummyRequest
from beaker.util import parse_cache_config_options
from beaker.cache import CacheManager
from pyramid.testing import DummyRequest
from pyramid import testing
from pyramid.security import Allow
from smarter.reports.user_preferences import get_district_level_context_names,\
    get_names, get_user_close_context
import edauth
from smarter_common.security.constants import RolesConstants
from edcore.security.tenant import set_tenant_map
from smarter.security.roles.default import DefaultRole  # @UnusedImport
from smarter.security.roles.pii import PII  # @UnusedImport
from edauth.security.user import RoleRelation
from edauth.security.session import Session


class TestCustomMetaData(Unittest_with_edcore_sqlite):

    def setUp(self):
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.shortlived'
        }
        CacheManager(**parse_cache_config_options(cache_opts))

        self.__request = DummyRequest()
        # Must set hook_zca to false to work with unittest_with_sqlite
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        defined_roles = [(Allow, RolesConstants.PII, ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        set_tenant_map({get_unittest_tenant_name(): 'NC'})
        # Set up context security
        dummy_session = Session()
        dummy_session.set_user_context([RoleRelation(RolesConstants.PII, get_unittest_tenant_name(), "NC", "228", "242")])
        dummy_session.set_uid('a5ddfe12-740d-4487-9179-de70f6ac33be')

        self.__config.testing_securitypolicy(dummy_session.get_user())

    def tearDown(self):
        # reset the registry
        testing.tearDown()

    def test_get_district_level_context_names(self):
        tenant = get_unittest_tenant_name()
        results = get_district_level_context_names(tenant, 'NC', '228')
        self.assertEqual('Sunset School District', results['name'])
        self.assertEqual(1, len(results['schools']))
        self.assertEqual('Sunset - Eastern Elementary', results['schools']['242']['name'])

    def test_get_user_close_context(self):
        params = {'stateCode': 'NC', 'districtId': '228', 'schoolId': '242'}  # existing school
        results = get_user_close_context(params, tenant=get_unittest_tenant_name())
        self.assertEqual('Sunset School District', results['districts'][0]['name'])
        self.assertEqual(1, len(results['schools']))
        self.assertEqual('Sunset - Eastern Elementary', results['schools'][0]['name'])

    def test_school_rollup_bound(self):
        params = {'stateCode': 'NC', 'districtId': '228', 'schoolId': '242'}  # existing school
        results = get_user_close_context(params, tenant=get_unittest_tenant_name(), school_rollup_bound=0)
        self.assertEqual('Sunset School District', results['districts'][0]['name'])
        self.assertEqual(0, len(results['schools']))

    def test_get_names(self):
        # not existing school
        results = get_names(get_unittest_tenant_name(), 'NC', '228', '-1')
        self.assertIsNone(results)
        # existing school
        results = get_names(get_unittest_tenant_name(), 'NC', '228', '242')
        self.assertIsNotNone(results)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
