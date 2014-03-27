'''
Created on Mar 11, 2013

@author: dwu
'''
import unittest
from smarter.reports.compare_pop_report import set_default_min_cell_size
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite, get_unittest_tenant_name
from smarter.reports.helpers.constants import Constants
from beaker.util import parse_cache_config_options
from beaker.cache import CacheManager
from pyramid.testing import DummyRequest
from pyramid import testing
from smarter.security.roles.default import DefaultRole  # @UnusedImport
from smarter.reports.helpers.compare_pop_stat_report import ComparingPopStatReport
from edauth.tests.test_helper.create_session import create_test_session
from pyramid.security import Allow
import edauth
from edauth.security.user import RoleRelation


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
        defined_roles = [(Allow, 'STATE_EDUCATION_ADMINISTRATOR_1', ('view', 'logout'))]
        edauth.set_roles(defined_roles)
        # Set up context security
        dummy_session = create_test_session(['STATE_EDUCATION_ADMINISTRATOR_1'])
        dummy_session.set_user_context([RoleRelation("STATE_EDUCATION_ADMINISTRATOR_1", get_unittest_tenant_name(), "NC", "228", "242")])
        self.__config.testing_securitypolicy(dummy_session)
        set_default_min_cell_size(0)

    def tearDown(self):
        # reset the registry
        testing.tearDown()

    def test_comparing_populations_with_not_stated_count_district_view(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.DISTRICTGUID] = '229'
        results = ComparingPopStatReport(**testParam).get_report()
        self.assertEqual(results['total'], 56)
        self.assertEqual(results['dmgPrg504'], 5)
        self.assertEqual(results['dmgPrgIep'], 5)
        self.assertEqual(results['dmgPrgLep'], 1)
        self.assertEqual(results['ethnicity'], 1)
        self.assertEqual(results['gender'], 2)

    def test_comparing_populations_with_not_stated_count_state_view(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        results = ComparingPopStatReport(**testParam).get_report()
        self.assertEqual(results['total'], 711)
        self.assertEqual(results['dmgPrg504'], 11)
        self.assertEqual(results['dmgPrgIep'], 13)
        self.assertEqual(results['dmgPrgLep'], 11)
        self.assertEqual(results['ethnicity'], 17)
        self.assertEqual(results['gender'], 2)

    def test_comparing_populations_with_not_stated_count_school_view(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NC'
        testParam[Constants.DISTRICTGUID] = '228'
        testParam[Constants.SCHOOLGUID] = '242'
        results = ComparingPopStatReport(**testParam).get_report()
        self.assertEqual(results['total'], 98)
        self.assertEqual(results['dmgPrg504'], 6)
        self.assertEqual(results['dmgPrgIep'], 8)
        self.assertEqual(results['dmgPrgLep'], 10)
        self.assertEqual(results['ethnicity'], 10)
        self.assertEqual(results['gender'], 0)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testReport']
    unittest.main()
