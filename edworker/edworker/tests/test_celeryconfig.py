'''
Created on May 10, 2013

@author: dawu
'''
import unittest
from edworker.celeryconfig import convert_to_celery_options
from edworker import celeryconfig


class TestCeleryConfig(unittest.TestCase):

    def test_get_config(self):
        settings = {'celery.broker_url': "amqp://guest:guest@localhost:5672//",
                    'celery.celery_always_eager': 'True',
                    'celery.CElerY_IMPORTS': '("myapp.tasks",)'}
        config = celeryconfig.get_config(settings=settings, prefix="celery")
        self.assertEqual(config['BROKER_URL'], settings['celery.broker_url'])
        self.assertEqual(config['CELERY_ALWAYS_EAGER'], True)
        # test capitalization
        self.assertTupleEqual(config['CELERY_IMPORTS'], ("myapp.tasks",))

    def test_get_config_empty_celery_config(self):
        settings = {'dummy': 'data'}
        config = celeryconfig.get_config(settings=settings, prefix="celery")
        self.assertEqual(len(config), 0)

    def test_convert_to_celery_options_of_tuple(self):
        config = {'CELERY_IMPORTS': '("tasks", "moretasks")'}
        celery_config = convert_to_celery_options(config)
        self.assertTupleEqual(celery_config['CELERY_IMPORTS'], ("tasks", "moretasks"))

    def test_convert_to_celery_options_of_int(self):
        config = {'CELERY_MAX_CACHED_RESULTS': '24'}
        celery_config = convert_to_celery_options(config)
        self.assertEqual(celery_config['CELERY_MAX_CACHED_RESULTS'], 24)

    def test_convert_to_celery_options_of_float(self):
        config = {'CELERY_TASK_RESULT_EXPIRES': '1.234'}
        celery_config = convert_to_celery_options(config)
        self.assertEqual(celery_config['CELERY_TASK_RESULT_EXPIRES'], 1.234)

    def test_convert_to_celery_options_of_string(self):
        config = {'CELERY_TIMEZONE': 'eastern'}
        celery_config = convert_to_celery_options(config)
        self.assertEqual(celery_config['CELERY_TIMEZONE'], 'eastern')

    def test_convert_to_celery_options_of_bool(self):
        config = {'CELERY_TRACK_STARTED': 'False'}
        celery_config = convert_to_celery_options(config)
        self.assertEqual(celery_config['CELERY_TRACK_STARTED'], False)

    def test_convert_to_celery_options_of_dict(self):
        config = {'CELERY_QUEUES': '{"key":"value"}'}
        celery_config = convert_to_celery_options(config)
        self.assertEqual(celery_config['CELERY_QUEUES']['key'], "value")

    def test_convert_to_celery_options_of_list(self):
        config = {'CASSANDRA_SERVERS': '[1,2]'}
        celery_config = convert_to_celery_options(config)
        self.assertListEqual(celery_config['CASSANDRA_SERVERS'], [1, 2])

    def test_convert_to_celery_options_of_any(self):
        config = {'CELERY_ACCEPT_CONTENT': '["application.json"]'}
        celery_config = convert_to_celery_options(config)
        self.assertEqual(celery_config['CELERY_ACCEPT_CONTENT'], ["application.json"])

    def test_convert_to_celery_options_of_BROKER_USE_SSL(self):
        config = {'BROKER_USE_SSL': '{"key":"value"}'}
        celery_config = convert_to_celery_options(config)
        self.assertEqual(celery_config['BROKER_USE_SSL']['key'], 'value')

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
