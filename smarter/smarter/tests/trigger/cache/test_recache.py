# (c) 2014 The Regents of the University of California. All rights reserved,
# subject to the license below.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0. Unless required by
# applicable law or agreed to in writing, software distributed under the License
# is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the specific language
# governing permissions and limitations under the License.

'''
Created on Jun 20, 2013

@author: dip
'''
import unittest
from beaker.cache import CacheManager, cache_managers
from beaker.util import parse_cache_config_options
from smarter.trigger.cache.recache import CacheTrigger,\
    flush_report_in_cache_region
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite,\
    get_unittest_tenant_name
from edapi.cache import cache_region, region_invalidate
from edcore.security.tenant import set_tenant_map


@cache_region('unittest')
def dummy_method(state_code):
    return True


class TestRecache(Unittest_with_edcore_sqlite):

    def setUp(self):
        cache_managers.clear()
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data, public.filtered_data, unittest, public.shortlived, public.very_shortlived'
        }
        self.cache_mgr = CacheManager(**parse_cache_config_options(cache_opts))
        set_tenant_map({'tomcat': 'NC', get_unittest_tenant_name(): 'NC'})

    def tearDown(self):
        cache_managers.clear()

    def test_recache_state_view_report(self):
        cache_trigger = CacheTrigger(get_unittest_tenant_name(), 'NC', {})
        cache_trigger.recache_cpop_report()
#        self.validate_cache_has_expected_number_of_item(2)

    def test_recache_district_view_report(self):
        cache_trigger = CacheTrigger(get_unittest_tenant_name(), 'NC', {})
        cache_trigger.recache_cpop_report('228')
#        self.validate_cache_has_expected_number_of_item(2)

    def test_flush_state_view_report(self):
        cache_trigger = CacheTrigger(get_unittest_tenant_name(), 'NC', {})
        cache_trigger.recache_cpop_report()

    def test_flush_district_view_report(self):
        cache_trigger = CacheTrigger(get_unittest_tenant_name(), 'NC', {})
        cache_trigger.recache_cpop_report('228')

    def test_flush_report_in_cache_region_with_empty_cache(self):
        region_invalidate(dummy_method, 'unittest', ('NC'))
        self.assertTrue(len(cache_managers.keys()), 0)

    def test_flush_unconfigured_region(self):
        self.assertRaises(KeyError, region_invalidate, dummy_method, 'unconfigured_region', 'NC')

    def validate_cache_has_expected_number_of_item(self, expected):
        self.assertTrue(len(cache_managers.keys()), 1)
        for cache_region in cache_managers.values():
            self.assertEqual(len(cache_region.namespace.dictionary.keys()), expected)

    def validate_cache_is_empty(self):
        self.assertTrue(len(cache_managers.keys()), 1)
        for cache_region in cache_managers.values():
            self.assertEqual(len(cache_region.namespace.dictionary.keys()), 0)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
