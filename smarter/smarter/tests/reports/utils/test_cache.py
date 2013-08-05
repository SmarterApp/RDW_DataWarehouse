'''
Created on Jul 15, 2013

@author: dip
'''
import unittest
from smarter.reports.utils.cache import get_cache_key, region_invalidate,\
    cache_region
from beaker.cache import cache_managers, CacheManager
from beaker.util import parse_cache_config_options


def dummy_method(stateCode):
    return True


@cache_region('dummyunittest')
def dummy_cache_method(stateCode):
    return True


class TestCache(unittest.TestCase):

    def setUp(self):
        cache_managers.clear()
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'dummyunittest',
            'cache.expire': 10
        }
        self.cache_mgr = CacheManager(**parse_cache_config_options(cache_opts))

    def tearDown(self):
        cache_managers.clear()

    def test_get_cache_key(self):
        args = 'NY'
        key = get_cache_key(args, 'dummy_method_name')
        self.assertIsNotNone(key)
        self.assertIsInstance(key, str)

    def test_get_cache_key_non_str_args(self):
        key = get_cache_key(['list'], 'dummy')
        self.assertIsNotNone(key)
        self.assertIsInstance(key, str)

    def test_region_invalidate_invalid_region(self):
        self.assertRaises(KeyError, region_invalidate, dummy_method, 'idontexist', 'ny')

    def test_region_invalidate_invalid_func(self):
        self.assertRaises(KeyError, region_invalidate, dummy_method, 'unittest', 'ny')

#    def test_region_invalidate(self):
#        before_invalidate = self.get_cache_key_count()
#        region_invalidate(dummy_cache_method, 'dummyunittest', 'nyc')
#        after_flush = self.get_cache_key_count()
#        self.assertEqual(before_invalidate, after_flush)

    def test_region_invalidate_valid_caching(self):
        dummy_cache_method('ny')
        before_invalidate = self.get_cache_key_count()
        region_invalidate(dummy_cache_method, 'dummyunittest', 'ny')
        after_flush = self.get_cache_key_count()
        self.assertEqual(before_invalidate - 1, after_flush)

    def get_cache_key_count(self):
        count = 0
        for cache_region in cache_managers.values():
            count += len(cache_region.namespace.dictionary.keys())
        return count


if __name__ == "__main__":
    unittest.main()
