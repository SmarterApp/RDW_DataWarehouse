'''
Created on Aug 5, 2013

@author: dawu
'''
import unittest
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    get_unittest_tenant_name
from edapi.tests.dummy import DummyRequest
from pyramid import testing
from smarter.reports.helpers.aggregate_dim import get_aggregate_dim
from beaker.util import parse_cache_config_options
from beaker.cache import CacheManager
from edauth.tests.test_helper.create_session import create_test_session
from smarter.reports.helpers.constants import AssessmentType
from smarter.reports.helpers.constants import Constants


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
        dummy_session = create_test_session(['TEACHER'], uid='272')
        self.__config.testing_securitypolicy(dummy_session)

    def tearDown(self):
        # reset the registry
        testing.tearDown()

    def test_get_aggregate_dim(self):
        tenant = get_unittest_tenant_name()
        agg_results = get_aggregate_dim({'subject1': 'Math', 'subject2': 'ELA'}, 'NC', districtGuid=None, schoolGuid=None, asmtYear=2016, asmtType=AssessmentType.INTERIM_COMPREHENSIVE, tenant=tenant)
        records = agg_results[Constants.RECORDS]
        self.assertEqual(4, len(records))
        record = records[3]
        results = record[Constants.RESULTS]
        self.assertFalse(results['subject1'][Constants.HASINTERIM])
        self.assertTrue(results['subject2'][Constants.HASINTERIM])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
