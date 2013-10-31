__author__ = 'sravi'

import unittest
from uuid import uuid4
from post_etl import post_etl


class TestPostEtl(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def setUp(self):
        pass

    @classmethod
    def tearDownClass(self):
        pass

    def tearDown(self):
        pass

    def test_verify_work_zone_cleanedup(self):
        fake_guid_batch = str(uuid4())
        self.assertTrue(post_etl.cleanup_work_zone(fake_guid_batch))
