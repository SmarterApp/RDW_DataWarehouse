'''
Created on Mar 11, 2013

@author: dwu
'''
import unittest

from beaker.util import parse_cache_config_options
from beaker.cache import CacheManager
from pyramid.testing import DummyRequest
from pyramid import testing
from pyramid.security import Allow

from smarter.reports.compare_pop_report import set_default_min_cell_size
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite, get_unittest_tenant_name
from smarter.reports.helpers.constants import Constants
from smarter.reports.helpers.compare_pop_stat_report import ComparingPopStatReport
from edauth.tests.test_helper.create_session import create_test_session
import edauth
from smarter_common.security.constants import RolesConstants
from edcore.security.tenant import set_tenant_map
from smarter.security.roles.default import DefaultRole  # @UnusedImport
from smarter.security.roles.pii import PII  # @UnusedImport


class TestComparingPopulationsStat(Unittest_with_edcore_sqlite):

    def setUp(self):
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data,public.filtered_data,public.shortlived'
        }
        CacheManager(**parse_cache_config_options(cache_opts))

        self.__request = DummyRequest()
        # Must set hook_zca to false to work with unittest_with_sqlite
        self.__config = testing.setUp(request=self.__request, hook_zca=False)
        defined_roles = [(Allow, RolesConstants.PII, ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        set_tenant_map({get_unittest_tenant_name(): 'NC'})
        # Set up context security
        dummy_session = create_test_session([RolesConstants.PII])
        self.__config.testing_securitypolicy(dummy_session.get_user())
        set_default_min_cell_size(0)

    def tearDown(self):
        # reset the registry
        testing.tearDown()

    def test_comparing_populations_with_not_stated_count_district_view(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.DISTRICTGUID] = '229'
        testParam[Constants.ASMTYEAR] = 2015
        results = ComparingPopStatReport(**testParam).get_report()
        self.assertEqual(results['total'], 27)
        self.assertEqual(results['dmgPrg504'], 3)
        self.assertEqual(results['dmgPrgIep'], 3)
        self.assertEqual(results['dmgPrgLep'], 1)
        self.assertEqual(results['ethnicity'], 1)
        self.assertEqual(results['sex'], 1)

    def test_comparing_populations_with_not_stated_count_state_view(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.ASMTYEAR] = 2015
        results = ComparingPopStatReport(**testParam).get_report()
        self.assertEqual(results['total'], 503)
        self.assertEqual(results['dmgPrg504'], 5)
        self.assertEqual(results['dmgPrgIep'], 5)
        self.assertEqual(results['dmgPrgLep'], 3)
        self.assertEqual(results['ethnicity'], 7)
        self.assertEqual(results['sex'], 1)

    def test_comparing_populations_with_not_stated_count_school_view(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.DISTRICTGUID] = '228'
        testParam[Constants.SCHOOLGUID] = '242'
        testParam[Constants.ASMTYEAR] = 2015
        results = ComparingPopStatReport(**testParam).get_report()
        self.assertEqual(results['total'], 28)
        self.assertEqual(results['dmgPrg504'], 2)
        self.assertEqual(results['dmgPrgIep'], 2)
        self.assertEqual(results['dmgPrgLep'], 2)
        self.assertEqual(results['ethnicity'], 4)
        self.assertEqual(results['sex'], 0)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testReport']
    unittest.main()
