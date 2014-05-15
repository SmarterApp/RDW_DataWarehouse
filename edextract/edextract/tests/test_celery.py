'''
Created on Nov 5, 2013

@author: dip
'''
import unittest
from edextract.celery import setup_celery, celery
from edextract import run_cron_cleanup


class TestCelery(unittest.TestCase):

    def test_setup_celery(self):
        celery_config = {'celery.BROKER_URL': 'amqp://guest:guest@localhost:1234//',
                         'celery.CELERY_ALWAYS_EAGER': 'True'}
        setup_celery(celery_config, 'celery')
        self.assertEqual(celery.conf['BROKER_URL'], celery_config['celery.BROKER_URL'])
        self.assertEqual(celery.conf['CELERY_ALWAYS_EAGER'], True)

    def test_run_cron_cleanup(self):
        # 2036 is currently the maximum year that is acceptable by python apscheduler.
        settings = {'extract.cleanup.schedule.cron.year': '2036',
                    'extract.cleanup.schedule.cron.month': '1-12',
                    'extract.cleanup.schedule.cron.day': '1',
                    'extract.cleanup.schedule.cron.week': '1',
                    'extract.cleanup.schedule.cron.hour': '0',
                    'extract.cleanup.schedule.cron.minute': '5',
                    'extract.cleanup.schedule.cron.second': '53'}
        run_cron_cleanup(settings)

    def test_run_cron_cleanup_bad_config(self):
        # 2036 is currently the maximum year that is acceptable by python apscheduler.
        settings = {'extract.cleanup.schedule.cron.year': '2036',
                    'extract.cleanup.schedule.cron.month': '1-12',
                    'extract.cleanup.schedule.cron.day': '1',
                    'extract.cleanup.schedule.cron.day_of_week': '3',
                    'extract.cleanup.schedule.cron.week': '1',
                    'extract.cleanup.schedule.cron.hour': '0',
                    'extract.cleanup.schedule.cron.minute': '5',
                    'extract.cleanup.schedule.cron.second': '53'}
        self.assertRaises(Exception, run_cron_cleanup, settings)


if __name__ == "__main__":
    unittest.main()
