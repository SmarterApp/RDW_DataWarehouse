'''
Created on Nov 5, 2013

@author: dip
'''
import unittest
from edextract.celery import setup_global_settings, setup_celery, celery
import edextract


class TestCelery(unittest.TestCase):

    def test_setup_celery(self):
        celery_config = {'celery.BROKER_URL': 'amqp://guest:guest@localhost:1234//',
                         'celery.CELERY_ALWAYS_EAGER': 'True'}
        setup_celery(celery_config, 'celery')
        self.assertEqual(celery.conf['BROKER_URL'], celery_config['celery.BROKER_URL'])
        self.assertEqual(celery.conf['CELERY_ALWAYS_EAGER'], True)

    def test_setup_global_settings(self):
        global MAX_RETRIES
        settings = {'extract.retries_allowed': 500}
        setup_global_settings(settings)
        self.assertEqual(edextract.celery.MAX_RETRIES, 500)
        self.assertEqual(edextract.celery.RETRY_DELAY, 60)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
