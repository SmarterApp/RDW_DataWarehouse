__author__ = 'tshewchuk'
"""
This module tests registering extract files with the HPZ.
"""

import unittest
from unittest.mock import patch

from pyramid import testing
from pyramid.registry import Registry
from pyramid.testing import DummyRequest

from hpz_client.file_registration.file_registration import register_file


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

    @patch('hpz_client.file_registration.file_registration.put')
    def test_register_file(self, put_patch):
        put_patch.return_value = MockResponse({'registration_id': 'a1-b2-c3-d4-e1e10', 'url': 'http://somehost:82/download/a1-b2-c3-d4-e1e10'})
        registration_id, download_url = register_file('dummy_user@phony.com')
        self.assertEqual('a1-b2-c3-d4-e1e10', registration_id)
        self.assertEqual('http://somehost:82/download/a1-b2-c3-d4-e1e10', download_url)
