'''
Created on Jun 22, 2013

@author: tosako
'''
import unittest
from smarter.tests.utils.unittest_with_smarter_sqlite import Unittest_with_smarter_sqlite
from beaker.cache import cache_region, cache_managers, CacheManager
from beaker.util import parse_cache_config_options
from smarter.trigger.pre_cache_generator import prepare_pre_cache,\
    trigger_precache


@cache_region('test')
def dummy_method(state_code):
    return True

class Test(Unittest_with_smarter_sqlite):

    def testPrepare_pre_cache(self):
        results = prepare_pre_cache('testtenant', 'NY', '20080101')
        self.assertEqual(2, len(results))

    def testTrigger_precache(self):
        cache_managers.clear()
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data, test'
        }
        CacheManager(**parse_cache_config_options(cache_opts))

        results = prepare_pre_cache('testtenant', 'NY', '20080101')
        triggered = trigger_precache('testtenant', 'NY', results)
        self.assertTrue(triggered)

    def testTrigger_precacheFail(self):
        cache_managers.clear()
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data, notest'
        }
        CacheManager(**parse_cache_config_options(cache_opts))
        results = prepare_pre_cache('testtenant', 'NY', '20080101')
        triggered = trigger_precache('testtenant', 'NY', results)
        self.assertFalse(triggered)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
