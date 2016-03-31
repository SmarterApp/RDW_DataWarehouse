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
import unittest
from celery import Celery
from edworker.celery import setup_celery, get_config_file, configure_celeryd
import os
import tempfile


class TestCelery(unittest.TestCase):

    def tearDown(self):
        os.environ.unsetenv("CELERY_PROD_CONFIG")

    def test_setup_celery(self):
        celery = Celery("unittext")
        celery_config = {'celery.BROKER_URL': 'amqp://guest:guest@localhost:1234//',
                         'celery.CELERY_ALWAYS_EAGER': 'True'}
        setup_celery(celery, celery_config, 'celery')
        self.assertEqual(celery.conf['BROKER_URL'], celery_config['celery.BROKER_URL'])
        self.assertEqual(celery.conf['CELERY_ALWAYS_EAGER'], True)

    def test_setup_celery_with_dif_prefix(self):
        celery = Celery("unittext")
        celery_config = {'ut.BROKER_URL': 'amqp://guest:guest@localhost:1234//',
                         'ut.CELERY_ALWAYS_EAGER': 'True'}
        setup_celery(celery, celery_config, 'ut')
        self.assertEqual(celery.conf['BROKER_URL'], celery_config['ut.BROKER_URL'])
        self.assertEqual(celery.conf['CELERY_ALWAYS_EAGER'], True)

    def test_get_config_file(self):
        self.assertIsNone(get_config_file())

    def test_get_config_file_with_prod_config(self):
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file.write(bytes('Some data', 'UTF-8'))
            temp_file.flush()
            os.environ["CELERY_PROD_CONFIG"] = temp_file.name
            config = get_config_file()
            self.assertEqual(config, temp_file.name)

    def test_configure_celeryd_non_prod_mode(self):
        celery, conf = configure_celeryd('myName')
        self.assertIsNotNone(celery)
        self.assertIsInstance(celery, Celery)

    def test_configure_celeryd_prod_mode(self):
        with tempfile.NamedTemporaryFile() as temp_file:
            temp_file.write(bytes('[app:main]\n', 'UTF-8'))
            temp_file.write(bytes('edworker.celery.CELERY_ALWAYS_EAGER = True', 'UTF-8'))
            temp_file.flush()
            os.environ["CELERY_PROD_CONFIG"] = temp_file.name
            celery, conf = configure_celeryd('unittest', 'edworker.celery')
            self.assertIsNotNone(celery)
            self.assertIsInstance(celery, Celery)
            self.assertEqual(celery.conf['CELERY_ALWAYS_EAGER'], True)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
