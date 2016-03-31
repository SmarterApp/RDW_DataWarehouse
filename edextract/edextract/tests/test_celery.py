# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

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
