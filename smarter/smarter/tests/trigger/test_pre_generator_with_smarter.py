'''
Created on Jun 22, 2013

@author: tosako
'''
import unittest
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite,\
    get_unittest_tenant_name
from beaker.cache import cache_managers, CacheManager, cache_regions
from beaker.util import parse_cache_config_options
from smarter.trigger.pre_cache_generator import prepare_pre_cache, \
    trigger_precache
import datetime


class TestPreCacheGenerator(Unittest_with_smarter_sqlite):

    def setUp(self):
        cache_managers.clear()
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data'
        }
        CacheManager(**parse_cache_config_options(cache_opts))
        self.tenant = get_unittest_tenant_name()

    def testPrepare_pre_cache(self):
        results = prepare_pre_cache(self.tenant, 'NY', datetime.datetime.strptime('20080101000000', '%Y%m%d%H%M%S'))
        self.assertEqual(2, len(results))

    def testPrepare_pre_cache_nodata(self):
        results = prepare_pre_cache(self.tenant, 'NY', datetime.datetime.strptime('20200101000000', '%Y%m%d%H%M%S'))
        self.assertEqual(0, len(results))

    def testTrigger_precache(self):
        results = prepare_pre_cache(self.tenant, 'NY', datetime.datetime.strptime('20080101000000', '%Y%m%d%H%M%S'))
        triggered = trigger_precache(self.tenant, 'NY', results)
        self.assertTrue(triggered)

    def testTrigger_precacheFail(self):
        results = [{'district_guid': 'I_dont_exist'}]
        triggered = trigger_precache(self.tenant, 'NY', results)
        self.assertFalse(triggered)

    def testTrigger_precache_with_invalid_state(self):
        results = [{'district_guid': '123'}]
        triggered = trigger_precache(self.tenant, 'DU', results)
        self.assertFalse(triggered)

    def testTrigger_precache_with_empty_results(self):
        results = prepare_pre_cache(self.tenant, 'DU', datetime.datetime.strptime('20080101000000', '%Y%m%d%H%M%S'))
        triggered = trigger_precache(self.tenant, 'DU', results)
        self.assertFalse(triggered)

    def testTrigger_precache_with_unconfigured_region(self):
        # Clears all cache regions
        cache_regions.clear()
        results = prepare_pre_cache(self.tenant, 'NY', datetime.datetime.strptime('20080101000000', '%Y%m%d%H%M%S'))
        triggered = trigger_precache(self.tenant, 'NY', results)
        self.assertFalse(triggered)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
