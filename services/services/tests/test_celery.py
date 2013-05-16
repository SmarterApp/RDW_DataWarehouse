'''
Created on May 15, 2013

@author: dip
'''
import unittest
from services.celery import setup_celery, celery


class TestCelery(unittest.TestCase):

    def test_setup_celery(self):
        celery_config = {'celery.BROKER_URL': 'amqp://guest:guest@localhost:1234//',
                         'celery.CELERY_ALWAYS_EAGER': 'True'}
        setup_celery(celery_config, 'celery')
        self.assertEqual(celery.conf['BROKER_URL'], celery_config['celery.BROKER_URL'])
        self.assertEqual(celery.conf['CELERY_ALWAYS_EAGER'], True)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
