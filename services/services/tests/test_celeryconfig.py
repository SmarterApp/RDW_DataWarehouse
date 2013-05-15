'''
Created on May 10, 2013

@author: dawu
'''
import unittest
from services import celeryconfig
import services


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

    def test_load_config_empty_celery_config(self):
        settings = {'dummy': 'data'}
        config = celeryconfig.load_config(settings=settings, prefix="celery")
        self.assertEqual(len(config), 0)

    def test_load_config_test_timeout(self):
        settings = {'pdf.generate.timeout': 50}
        celeryconfig.load_config(settings=settings, prefix="celery")
        self.assertEqual(services.celeryconfig.TIMEOUT, 50)

    def test_load_config_test_default_timeout(self):
        settings = {}
        celeryconfig.load_config(settings=settings, prefix="celery")
        self.assertEqual(services.celeryconfig.TIMEOUT, 20)

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
