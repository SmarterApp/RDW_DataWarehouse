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
Created on Nov 18, 2015

@author: sshrestha
'''
import unittest
from pyramid.testing import DummyRequest
from pyramid.registry import Registry
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from pyramid import testing
from smarter.services.statecode_generator import statecode_generator_service, EDWARE_PUBLIC_SECRET
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite_no_data_load
from smarter.reports.helpers.constants import Constants
from edauth.tests.test_helper.create_session import create_test_session


SECRET = 'test_secret_1234'


class TestTrigger(Unittest_with_stats_sqlite_no_data_load):

    def setUp(self):
        reg = Registry()
        reg.settings = {EDWARE_PUBLIC_SECRET: SECRET}
        cache_opts = {
            'cache.type': 'memory',
            'cache.regions': 'public.data,public.filtered_data,public.shortlived,public.very_shortlived'
        }
        CacheManager(**parse_cache_config_options(cache_opts))

        self.__request = DummyRequest()
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)
        dummy_session = create_test_session(['SUPER_USER'], uid='272', tenant='cat')
        self.__config.testing_securitypolicy(dummy_session)

    def tearDown(self):
        testing.tearDown()

    def test_statecode_generator_service(self):
        stateCode = 'AA'
        self.__request.matchdict[Constants.STATE_CODE] = stateCode
        results = statecode_generator_service(self.__request)
        self.assertEqual(stateCode, results.json_body[Constants.STATE_CODE])
        self.assertTrue(len(results.json_body[Constants.SID]) > 20)

if __name__ == "__main__":
    unittest.main()
