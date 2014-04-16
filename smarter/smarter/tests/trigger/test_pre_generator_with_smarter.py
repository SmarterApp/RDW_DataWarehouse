'''
Created on Jun 22, 2013

@author: tosako
'''
import unittest
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    get_unittest_tenant_name
from beaker.cache import cache_managers, CacheManager, cache_regions
from beaker.util import parse_cache_config_options
from smarter.trigger.pre_cache_generator import prepare_pre_cache, \
    trigger_precache, read_config_from_json_file
import os


class TestPreCacheGenerator(Unittest_with_edcore_sqlite):

    def setUp(self):
        cache_managers.clear()
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data'
        }
        CacheManager(**parse_cache_config_options(cache_opts))
        self.tenant = get_unittest_tenant_name()

    def testPrepare_pre_cache(self):
        results = prepare_pre_cache(self.tenant, 'NC', '820568d0-ddaa-11e2-a63d-68a86d3c2f82')
        self.assertEqual(5, len(results))

    def testPrepare_pre_cache_nodata(self):
        results = prepare_pre_cache(self.tenant, 'NC', '2cf08036-ddb0-11e2-a15e-68a86d3c2f82')
        self.assertEqual(0, len(results))

    def testTrigger_precache(self):
        results = prepare_pre_cache(self.tenant, 'NC', '820568d0-ddaa-11e2-a63d-68a86d3c2f82')
        triggered = trigger_precache(self.tenant, 'NC', results, {})
        self.assertTrue(triggered)

    def testTrigger_precache_with_bad_district(self):
        results = [{'district_guid': 'I_dont_exist'}]
        triggered = trigger_precache(self.tenant, 'NC', results, {})
        self.assertTrue(triggered)

    def testTrigger_precache_with_invalid_state(self):
        results = [{'district_guid': '123'}]
        triggered = trigger_precache(self.tenant, 'DU', results, {})
        self.assertTrue(triggered)

    def testTrigger_precache_with_empty_results(self):
        results = prepare_pre_cache(self.tenant, 'DU', '820568d0-ddaa-11e2-a63d-68a86d3c2f82')
        triggered = trigger_precache(self.tenant, 'DU', results, {})
        self.assertFalse(triggered)

    def testTrigger_precache_with_unconfigured_region(self):
        # Clears all cache regions
        cache_regions.clear()
        results = prepare_pre_cache(self.tenant, 'NC', '820568d0-ddaa-11e2-a63d-68a86d3c2f82')
        triggered = trigger_precache(self.tenant, 'NC', results, {})
        self.assertFalse(triggered)

    def test_read_config_file_with_invalid_file(self):
        self.assertRaises(Exception, read_config_from_json_file, '../I_dont_exist.json')

    def test_read_config_file_with_valid_file(self):
        cwd = os.path.abspath(os.path.dirname(__file__))
        data = read_config_from_json_file(os.path.join(cwd, 'resource/filter.json'))
        self.assertEqual(len(data.keys()), 3)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
