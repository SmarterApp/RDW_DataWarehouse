'''
Created on May 15, 2013

@author: dip
'''
import os
import unittest

import services
from services.celery import setup_celery, celery


class TestCelery(unittest.TestCase):

    def tearDown(self):
        os.environ.unsetenv("CELERY_PROD_CONFIG")

    def test_setup_celery(self):
        celery_config = {'celery.BROKER_URL': 'amqp://guest:guest@localhost:1234//',
                         'celery.CELERY_ALWAYS_EAGER': 'True'}
        setup_celery(celery_config, 'celery')
        self.assertEqual(celery.conf['BROKER_URL'], celery_config['celery.BROKER_URL'])
        self.assertEqual(celery.conf['CELERY_ALWAYS_EAGER'], True)

    def test_setup_celery_test_timeout(self):
        settings = {'pdf.generate_timeout': '50'}
        setup_celery(settings=settings, prefix="celery")
        self.assertEqual(services.celery.TIMEOUT, 50)

    def test_setup_celery_test_default_timeout(self):
        settings = {}
        setup_celery(settings=settings, prefix="celery")
        self.assertEqual(services.celery.TIMEOUT, 60)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
