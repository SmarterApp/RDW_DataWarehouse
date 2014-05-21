__author__ = 'tshewchuk'
"""
Unit tests for the file upload service of HPZ.
"""

import unittest
from unittest import mock
from unittest.mock import patch
from pyramid.testing import DummyRequest
from pyramid import testing
import logging
from hpz.frs.upload_service import file_upload_service
from pyramid.registry import Registry


class DummyFile:
    def __init__(self):
        self.file = None
        self.read = None


class UploadTest(unittest.TestCase):

    def setUp(self):
        self.__request = DummyRequest()
        self.__request.matchdict['registration_id'] = 'a1-b2-c3-d4-e5'
        self.__request.headers['Fileext'] = 'zip'
        reg = Registry()
        reg.settings = {'hpz.frs.upload_base_path': '/dev/null'}
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)

    def tearDown(self):
        self.__request = None

    @patch('hpz.frs.upload_service.FileRegistry.update_registration')
    @patch('hpz.frs.upload_service.FileRegistry.is_file_registered')
    @patch('shutil.copyfileobj')
    @patch('builtins.open')
    def test_file_upload_service(self, open_patch, copyfileobj_patch, is_file_registered, update_registration_patch):
        update_registration_patch.return_value = DummyFile()
        copyfileobj_patch.return_value = None
        open_patch.return_value.__exit__.return_value = None
        is_file_registered.return_value = True

        self.__request.method = 'POST'
        self.__request.POST['file'] = DummyFile()

        response = file_upload_service(None, self.__request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(is_file_registered.called)
        self.assertTrue(copyfileobj_patch.called)
        self.assertTrue(update_registration_patch.called)

    @patch('hpz.frs.upload_service.FileRegistry.update_registration')
    @patch('hpz.frs.upload_service.FileRegistry.is_file_registered')
    def test_file_upload_service_not_registered(self, is_file_registered, update_registration_patch):
        test_logger = logging.getLogger(file_upload_service.__name__)
        with mock.patch.object(test_logger, 'error') as mock_debug:

            update_registration_patch.return_value = None
            is_file_registered.return_value = False

            self.__request.method = 'POST'
            self.__request.json_body = {}

            response = file_upload_service(None, self.__request)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(is_file_registered.called)
            self.assertFalse(update_registration_patch.called)
