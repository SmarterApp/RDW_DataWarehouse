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
