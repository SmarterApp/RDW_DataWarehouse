__author__ = 'tshewchuk'
"""
Unit tests for the file upload service of HPZ.
"""

import unittest
from unittest.mock import patch
from pyramid.testing import DummyRequest
from pyramid import testing
from hpz.frs.upload_service import file_upload_service
from pyramid.registry import Registry


class RegistrationTest(unittest.TestCase):

    def setUp(self):
        self.__request = DummyRequest()
        self.__request.matchdict['registration_id'] = 'a1-b2-c3-d4-e5'
        self.__request.headers['Filename'] = 'xyz_user_extract.zip'
        reg = Registry()
        reg.settings = {'hpz.frs.upload_base_path': '/bogus/directory'}
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)

    def tearDown(self):
        self.__request = None

    @patch('hpz.frs.registration_service.FileRegistry.file_upload_request')
    @patch('hpz.frs.registration_service.FileRegistry.is_file_registered')
    def test_file_upload_service(self, is_file_registered, file_upload_patch):

        file_upload_patch.return_value = None
        is_file_registered.return_value = True

        self.__request.method = 'POST'
        self.__request.json_body = {}

        response = file_upload_service(None, self.__request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(file_upload_patch.called)
        self.assertTrue(is_file_registered.called)

    @patch('hpz.frs.registration_service.FileRegistry.file_upload_request')
    @patch('hpz.frs.registration_service.FileRegistry.is_file_registered')
    def test_file_upload_service_not_registered(self, is_file_registered, file_upload_patch):

        file_upload_patch.return_value = None
        is_file_registered.return_value = False

        self.__request.method = 'POST'
        self.__request.json_body = {}

        response = file_upload_service(None, self.__request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(not file_upload_patch.called)
        self.assertTrue(is_file_registered.called)
