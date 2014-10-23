'''
Created on Oct 21, 2014

@author: tosako
'''
import unittest
from pyramid.testing import DummyRequest
from pyramid import testing
from pyramid.security import Allow
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite, get_unittest_tenant_name
from edauth.tests.test_helper.create_session import create_test_session
import edauth
from smarter_common.security.constants import RolesConstants
from edcore.security.tenant import set_tenant_map
from smarter.security.roles.default import DefaultRole  # @UnusedImport
from smarter.security.roles.pii import PII  # @UnusedImport
from smarter.reports.helpers.constants import Constants
from smarter.reports.list_of_students_report_iab import get_list_of_students_iab, \
    get_list_of_students_report_iab
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options


class Test(Unittest_with_edcore_sqlite):

    def setUp(self):
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data,public.filtered_data,public.shortlived'
        }

        CacheManager(**parse_cache_config_options(cache_opts))
        # Set up user context
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with unittest_with_sqlite
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        defined_roles = [(Allow, RolesConstants.PII, ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        set_tenant_map({get_unittest_tenant_name(): 'NC'})
        # Set up context security
        dummy_session = create_test_session([RolesConstants.PII])
        self.__config.testing_securitypolicy(dummy_session.get_user())

    def test_get_list_of_students_for_iab(self):
        params = {}
        params[Constants.STATECODE] = 'NC'
        params[Constants.DISTRICTGUID] = '229'
        params[Constants.SCHOOLGUID] = '936'
        params[Constants.ASMTGRADE] = '3'
        params[Constants.ASMTSUBJECT] = ['Math']
        params[Constants.ASMTYEAR] = 2015
        results = get_list_of_students_iab(params)
        self.assertEqual(6, len(results))

    def test_get_list_of_students_report_iab(self):
        params = {}
        params[Constants.STATECODE] = 'NC'
        params[Constants.DISTRICTGUID] = '229'
        params[Constants.SCHOOLGUID] = '936'
        params[Constants.ASMTGRADE] = '3'
        params[Constants.ASMTSUBJECT] = ['Math']
        params[Constants.ASMTYEAR] = 2015
        los_results = get_list_of_students_report_iab(params)
        IAB = los_results['assessments']['20150106']['Interim Assessment Blocks']
        data = IAB['34b99412-fd5b-48f0-8ce8-f8ca3788634a']
        subject1 = data['subject1']
        claims = subject1['claims']
        self.assertEqual(2, len(IAB))
        self.assertEqual(1, len(claims))
        self.assertEqual('Mathematics Performance Task', claims[0]['name'])


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
