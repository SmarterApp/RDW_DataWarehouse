'''
Created on Mar 11, 2013

@author: dwu
'''
import unittest
from smarter.reports.compare_pop_report import set_default_min_cell_size
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    UnittestEdcoreDBConnection, get_unittest_tenant_name
from smarter.reports.helpers.constants import Constants
from beaker.util import parse_cache_config_options
from beaker.cache import CacheManager
from pyramid.testing import DummyRequest
from pyramid import testing
from edauth.security.session import Session
from smarter.security.roles.default import DefaultRole  # @UnusedImport
from smarter.reports.helpers.compare_pop_stat_report import ComparingPopStatReport


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
        with UnittestEdcoreDBConnection() as connection:
            # Insert into user_mapping table
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.insert(), user_id='272', guid='272')
        dummy_session = Session()
        dummy_session.set_session_id('123')
        dummy_session.set_roles(['TEACHER'])
        dummy_session.set_uid('272')
        dummy_session.set_tenant(get_unittest_tenant_name())
        self.__config.testing_securitypolicy(dummy_session)
        set_default_min_cell_size(0)

    def tearDown(self):
        # reset the registry
        testing.tearDown()

        # delete user_mapping entries
        with UnittestEdcoreDBConnection() as connection:
            user_mapping = connection.get_table('user_mapping')
            connection.execute(user_mapping.delete())

    def test_comparing_populations_with_not_stated_count_district_view(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        testParam[Constants.DISTRICTGUID] = '229'
        results = ComparingPopStatReport(**testParam).get_report()
        self.assertEqual(results['total'], 47)
        self.assertEqual(results['dmgPrg504'], 3)
        self.assertEqual(results['dmgPrgIep'], 3)
        self.assertEqual(results['dmgPrgLep'], 1)
        self.assertEqual(results['ethnicity'], 1)
        self.assertEqual(results['gender'], 1)

    def test_comparing_populations_with_not_stated_count_state_view(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        results = ComparingPopStatReport(**testParam).get_report()
        self.assertEqual(results['total'], 907)
        self.assertEqual(results['dmgPrg504'], 7)
        self.assertEqual(results['dmgPrgIep'], 9)
        self.assertEqual(results['dmgPrgLep'], 9)
        self.assertEqual(results['ethnicity'], 11)
        self.assertEqual(results['gender'], 1)

    def test_comparing_populations_with_not_stated_count_school_view(self):
        testParam = {}
        testParam[Constants.STATECODE] = 'NY'
        testParam[Constants.DISTRICTGUID] = '228'
        testParam[Constants.SCHOOLGUID] = '242'
        results = ComparingPopStatReport(**testParam).get_report()
        self.assertEqual(results['total'], 70)
        self.assertEqual(results['dmgPrg504'], 4)
        self.assertEqual(results['dmgPrgIep'], 6)
        self.assertEqual(results['dmgPrgLep'], 8)
        self.assertEqual(results['ethnicity'], 6)
        self.assertEqual(results['gender'], 0)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testReport']
    unittest.main()
