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
Created on Jun 27, 2013

@author: dip
'''
import unittest
from pyramid.testing import DummyRequest
from pyramid.registry import Registry
from pyramid import testing
from smarter.services.trigger import trigger
from edcore.tests.utils.unittest_with_stats_sqlite import Unittest_with_stats_sqlite_no_data_load
from edapi.httpexceptions import EdApiHTTPNotFound
from edauth.tests.test_helper.create_session import create_test_session


class TestTrigger(Unittest_with_stats_sqlite_no_data_load):

    def setUp(self):
        self.__request = DummyRequest()
        # Must set hook_zca to false to work with uniittest_with_sqlite
        reg = Registry()
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)
        dummy_session = create_test_session(['SUPER_USER'], uid='272', tenant='cat')
        self.__config.testing_securitypolicy(dummy_session)

    def tearDown(self):
        testing.tearDown()

    def test_invalid_key(self):
        self.__request.matchdict['trigger_type'] = 'invalid'
        rtn = trigger(self.__request)
        self.assertIsInstance(rtn, EdApiHTTPNotFound)

    def test_cache_trigger(self):
        self.__request.matchdict['trigger_type'] = 'cache'
        rtn = trigger(self.__request)
        self.assertTrue(rtn['result'], 'OK')

    def test_pdf_trigger(self):
        self.__request.matchdict['trigger_type'] = 'pdf'
        rtn = trigger(self.__request)
        self.assertTrue(rtn['result'], 'OK')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
