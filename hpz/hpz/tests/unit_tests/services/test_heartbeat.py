'''
Created on Oct 9, 2014

@author: tosako
'''
import unittest
import tempfile
import os
from hpz.services.heartbeat import check_file_write, check_database, heartbeat
from edcore.tests.utils.unittest_with_edcore_sqlite import Unittest_with_edcore_sqlite_no_data_load
from hpz.database import hpz_connector
from pyramid.testing import DummyRequest
from pyramid.registry import Registry
from pyramid import testing
from pyramid.httpexceptions import HTTPOk, HTTPServerError


class Test(Unittest_with_edcore_sqlite_no_data_load):

    def test_check_file_write_fail(self):
        tested = False
        with tempfile.TemporaryDirectory() as tmp:
            test_dir = os.path.join(tmp, 'foo')
            ok = check_file_write(test_dir)
            tested = True
            self.assertFalse(ok)
        self.assertTrue(tested)

    def test_check_file_write_ok(self):
        tested = False
        with tempfile.TemporaryDirectory() as tmp:
            ok = check_file_write(tmp)
            tested = True
            self.assertTrue(ok)
        self.assertTrue(tested)

    def test_check_database(self):
        hpz_connector.HPZ_NAMESPACE = 'edware.db.tomcat'
        ok = check_database()
        self.assertTrue(ok)

    def test_check_database_fail(self):
        hpz_connector.HPZ_NAMESPACE = 'edware.db.foo'
        ok = check_database()
        self.assertFalse(ok)

    def test_heartbeat(self):
        tested = False
        hpz_connector.HPZ_NAMESPACE = 'edware.db.tomcat'
        with tempfile.TemporaryDirectory() as tmp:
            request = DummyRequest()
            reg = Registry()
            reg.settings = {'hpz.frs.upload_base_path': tmp}
            testing.setUp(registry=reg, request=request, hook_zca=False)
            res = heartbeat(request)
            tested = True
        self.assertTrue(tested)
        self.assertEqual(type(res), HTTPOk)

    def test_heartbeat_fail(self):
        tested = False
        hpz_connector.HPZ_NAMESPACE = 'edware.db.tomcat.foo'
        with tempfile.TemporaryDirectory() as tmp:
            request = DummyRequest()
            reg = Registry()
            reg.settings = {'hpz.frs.upload_base_path': tmp}
            testing.setUp(registry=reg, request=request, hook_zca=False)
            res = heartbeat(request)
            tested = True
        self.assertTrue(tested)
        self.assertEqual(type(res), HTTPServerError)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
