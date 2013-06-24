'''
Created on Jun 20, 2013

@author: dip
'''
import unittest
from beaker.cache import CacheManager, cache_region, cache_managers
from beaker.util import parse_cache_config_options
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite,\
    get_unittest_tenant_name
from edapi.exceptions import NotFoundException
from smarter.reports.helpers.constants import Constants
from smarter.trigger.cache.recache import CacheTrigger,\
    flush_report_in_cache_region


@cache_region('test')
def dummy_method(state_code):
    return True


class TestRecache(Unittest_with_smarter_sqlite):

    def setUp(self):
        cache_managers.clear()
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data, test'
        }
        self.cache_mgr = CacheManager(**parse_cache_config_options(cache_opts))

    def tearDown(self):
        cache_managers.clear()

    def test_recache_state_view_report(self):
        cache_trigger = CacheTrigger(get_unittest_tenant_name())
        results = cache_trigger.recache_state_view_report('NY')

        self.assertTrue(Constants.RECORDS in results, "returning JSON must have records")
        self.assertTrue(Constants.COLORS in results, "returning JSON must have colors")
        self.assertTrue(Constants.SUBJECTS in results, "returning JSON must have subjects")
        self.assertTrue('context' in results, "returning JSON must have context")
        self.assertTrue(Constants.SUMMARY in results, "returning JSON must have summary")

        # check district-level results
        records = results[Constants.RECORDS]
        self.assertEqual(2, len(records), "2 districts in the list")

    def test_recache_state_view_report_invalid_tenant(self):
        cache_trigger = CacheTrigger('i_dont_exists')
        self.assertRaises(AttributeError, cache_trigger.recache_state_view_report, 'NY')

    def test_recache_state_view_report_invalid_state_code(self):
        cache_trigger = CacheTrigger(get_unittest_tenant_name())
        self.assertRaises(NotFoundException, cache_trigger.recache_state_view_report, 'DU')

    def test_recache_district_view_report(self):
        cache_trigger = CacheTrigger(get_unittest_tenant_name())
        results = cache_trigger.recache_district_view_report('NY', '228')

        # check top-level attributes
        self.assertTrue(Constants.RECORDS in results, "returning JSON must have records")
        self.assertTrue(Constants.COLORS in results, "returning JSON must have colors")
        self.assertTrue(Constants.SUBJECTS in results, "returning JSON must have subjects")
        self.assertTrue('context' in results, "returning JSON must have context")
        self.assertTrue(Constants.SUMMARY in results, "returning JSON must have summary")

        # check school-level results
        records = results[Constants.RECORDS]
        self.assertEqual(3, len(records), "3 schools in the list")

    def test_recache_district_view_report_invalid_tenant(self):
        cache_trigger = CacheTrigger('i_dont_exists')
        self.assertRaises(Exception, cache_trigger.recache_district_view_report, 'NY', '228')

    def test_recache_district_view_report_invalid_district_guid(self):
        cache_trigger = CacheTrigger(get_unittest_tenant_name())
        self.assertRaises(NotFoundException, cache_trigger.recache_district_view_report, 'NY', 'i_dont_exist')

    def test_flush_state_view_report(self):
        cache_trigger = CacheTrigger(get_unittest_tenant_name())
        cache_trigger.recache_state_view_report('NY')
        self.validate_cache_has_one_item()

        cache_trigger.flush_state_view_report('NY')
        self.validate_cache_is_empty()

    def test_flush_district_view_report(self):
        cache_trigger = CacheTrigger(get_unittest_tenant_name())
        cache_trigger.recache_district_view_report('NY', '228')
        self.validate_cache_has_one_item()
        cache_trigger.flush_district_view_report('NY', '228')
        self.validate_cache_is_empty()

    def test_flush_report_in_cache_region_with_empty_cache(self):
        flush_report_in_cache_region(dummy_method, 'NY')
        self.assertTrue(len(cache_managers.keys()), 0)

    def test_flush_report_in_cache_region(self):
        dummy_method('NY')
        self.validate_cache_has_one_item()
        flush_report_in_cache_region(dummy_method, 'NY', region='test')
        self.validate_cache_is_empty()

    def validate_cache_has_one_item(self):
        self.assertTrue(len(cache_managers.keys()), 1)
        for cache_region in cache_managers.values():
            self.assertEqual(len(cache_region.namespace.dictionary.keys()), 1)

    def validate_cache_is_empty(self):
        self.assertTrue(len(cache_managers.keys()), 1)
        for cache_region in cache_managers.values():
            self.assertEqual(len(cache_region.namespace.dictionary.keys()), 0)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
