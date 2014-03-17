import unittest
from unittest.mock import MagicMock
from mocket.mocket import Mocket
from edmigrate.tests.utils.unittest_with_repmgr_sqlite import Unittest_with_repmgr_sqlite
from edmigrate.tasks.slave import get_hostname


class Test(Unittest_with_repmgr_sqlite):

    @classmethod
    def setUpClass(cls):
        Unittest_with_repmgr_sqlite.setUpClass()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_hostname(self):
        Mocket.enable()
        hostname = get_hostname()
        self.assertEqual(hostname, 'localhost')
