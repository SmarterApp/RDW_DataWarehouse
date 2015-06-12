import unittest
from smarter_score_batcher.tasks.health_check import health_check
from smarter_score_batcher.celery import conf
from smarter_score_batcher.tests.database.unittest_with_tsb_sqlite import Unittest_with_tsb_sqlite


class Test(Unittest_with_tsb_sqlite):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testHealthCheck(self):
        self.assertTrue(health_check()[0:9] == 'heartbeat')
