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
Created on Mar 23, 2015

'''
import unittest
from smarter_score_batcher.tests.database.unittest_with_tsb_sqlite import Unittest_with_tsb_sqlite
from smarter_score_batcher.services.heartbeat import heartbeat, check_celery
from pyramid.testing import DummyRequest
from pyramid.httpexceptions import HTTPServerError


class TestHeartbeat(Unittest_with_tsb_sqlite):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testValidCelery(self):
        '''
        During unit test, the celery doesn't run. So it should fail
        '''
        self.assertRaises(Exception, check_celery, DummyRequest())

    def testValidHeartbeat(self):
        '''
        During unit test, the celery doesn't run. So it should fail
        '''
        results = heartbeat(DummyRequest())
        self.assertIsInstance(results, HTTPServerError)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
