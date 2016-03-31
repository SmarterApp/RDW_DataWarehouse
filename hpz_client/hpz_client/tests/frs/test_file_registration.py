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

__author__ = 'tshewchuk'
"""
This module tests registering extract files with the HPZ.
"""

import unittest
from unittest.mock import patch

from pyramid import testing
from pyramid.registry import Registry
from pyramid.testing import DummyRequest

from hpz_client.frs.file_registration import register_file
from hpz_client.frs.config import Config, initialize


class MockResponse():
    def __init__(self, json):
        self.__json = json

    def json(self):
        return self.__json


class TestFileRegistration(unittest.TestCase):

    def setUp(self):
        self.__request = DummyRequest()
        self.reg = Registry()
        self.__config = testing.setUp(registry=self.reg, request=self.__request, hook_zca=False)
        settings = {Config.HPZ_FILE_REGISTRATION_URL: 'http://somehost:82/registration'}
        initialize(settings)

    @patch('hpz_client.frs.file_registration.put')
    def test_register_file(self, put_patch):
        put_patch.return_value = MockResponse({'registration_id': 'a1-b2-c3-d4-e1e10', 'url': 'http://somehost:82/download/a1-b2-c3-d4-e1e10', 'web_url': 'http://something.com/web/as'})
        registration_id, download_url, web_download_url = register_file('dummy_user@phony.com', 'dummy_user@phony.com')
        self.assertEqual('a1-b2-c3-d4-e1e10', registration_id)
        self.assertEqual('http://somehost:82/download/a1-b2-c3-d4-e1e10', download_url)
        self.assertEqual('http://something.com/web/as', web_download_url)
        #disable because key order of serialized dictionaly is unpredictable
        #put_patch.assert_called_once_with('http://somehost:82/registration', '{"email": "dummy_user@phony.com", "uid": "dummy_user@phony.com"}', verify=True)
