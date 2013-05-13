'''
Created on May 10, 2013

@author: dawu
'''
import unittest
from services import celeryconfig


class TestCeleryConfig(unittest.TestCase):

    def test_load_config(self):
        settings = {'celery.broker_url': "amqp://guest:guest@localhost:5672//",
                    'celery.celery_always_eager': 'True',
                    'celery.CElerY_IMPORTS': ("myapp.tasks",)}
        config = celeryconfig.load_config(settings=settings, prefix="celery")
        self.assertEqual(config['BROKER_URL'], settings['celery.broker_url'])
        self.assertEqual(config['CELERY_ALWAYS_EAGER'], settings['celery.celery_always_eager'])
        # test capitalization
        self.assertEqual(config['CELERY_IMPORTS'], settings['celery.CElerY_IMPORTS'])

    def test_setup_celery(self):
        celery_config = {'BROKER_URL': 'amqp://guest:guest@localhost:1234//',
                         'CELERY_ALWAYS_EAGER': 'True'}
        celeryconfig.setup_celery(celery_config)
        self.assertEqual(celeryconfig.celery.conf['BROKER_URL'], celery_config['BROKER_URL'])
        self.assertEqual(celeryconfig.celery.conf['CELERY_ALWAYS_EAGER'], celery_config['CELERY_ALWAYS_EAGER'])

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
