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
from hpz.frs import upload_service
from hpz.frs.upload_service import file_upload_service_with_default_notification
from pyramid.registry import Registry


class DummyFile:
    def __init__(self):
        self.file = None
        self.read = None


class UploadTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._dir = tempfile.TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        cls._dir.cleanup()

    def setUp(self):
        self.__request = DummyRequest()
        self.__request.matchdict['registration_id'] = 'a1-b2-c3-d4-e5'
        self.__request.headers['File-Name'] = 'dummy.zip'
        reg = Registry()
        reg.settings = {'hpz.frs.upload_base_path': self._dir.name, 'hpz.frs.file_size_limit': '1024'}
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)

    def tearDown(self):
        self.__request = None

    @patch('hpz.frs.upload_service.FileRegistry.update_registration')
    @patch('hpz.frs.upload_service.FileRegistry.is_file_registered')
    @patch('shutil.copyfileobj')
    @patch('os.path.getsize')
    @patch('hpz.frs.upload_service.logger.info')
    def test_file_upload_service_with_default_notification(self, logger_patch, get_size_patch, copyfileobj_patch, is_file_registered_patch,
                                                           update_registration_patch):
        update_registration_patch.return_value = None
        copyfileobj_patch.return_value = DummyFile()
        is_file_registered_patch.return_value = True
        get_size_patch.return_value = 1
        logger_patch.return_value = None

        self.__request.method = 'POST'
        self.__request.POST['file'] = DummyFile()

        response = file_upload_service_with_default_notification(None, self.__request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(update_registration_patch.called)
        self.assertTrue(copyfileobj_patch.called)
        self.assertTrue(is_file_registered_patch.called)

    @patch('hpz.frs.upload_service.FileRegistry.is_file_registered')
    def test_file_upload_service_not_registered(self, is_file_registered_patch):
        is_file_registered_patch.return_value = False

        self.__request.method = 'POST'
        self.__request.POST['file'] = DummyFile()

        response = file_upload_service_with_default_notification(None, self.__request)

        self.assertEqual(response.status_code, 404)

    @patch('hpz.frs.upload_service.FileRegistry.update_registration')
    @patch('hpz.frs.upload_service.FileRegistry.is_file_registered')
    @patch('shutil.copyfileobj')
    @patch('hpz.frs.upload_service.logger.error')
    @patch('os.path.getsize')
    def test_file_creation_error(self, get_size_patch, logger_patch, copyfileobj_patch, is_file_registered_patch,
                                 update_registration_patch):
        update_registration_patch.return_value = True
        copyfileobj_patch.return_value = DummyFile()
        logger_patch.return_value = None
        # open_patch.side_effect = IOError('Message')
        is_file_registered_patch.return_value = True
        get_size_patch.return_value = 1

        self.__request.method = 'POST'
        self.__request.POST['file'] = DummyFile()

        response = file_upload_service_with_default_notification(None, self.__request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(update_registration_patch.called)

    @patch('hpz.frs.upload_service.FileRegistry.update_registration')
    @patch('shutil.copyfileobj')
    @patch('builtins.open')
    def test_invalid_headers(self, open_patch, copyfileobj_patch, update_registration_patch):
        update_registration_patch.return_value = True
        copyfileobj_patch.return_value = DummyFile()
        open_patch.return_value.__exit__.return_value = None

        __invalid_request = DummyRequest()
        __invalid_request.matchdict['registration_id'] = 'a1-b2-c3-d4-e5'
        __invalid_request.headers['InvalidFileName'] = 'Dummy'

        self.__request.method = 'POST'
        self.__request.POST['file'] = DummyFile()

        response = file_upload_service_with_default_notification(None, __invalid_request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(not update_registration_patch.called)
        self.assertTrue(not copyfileobj_patch.called)
        self.assertTrue(not open_patch.called)

    @patch('hpz.frs.upload_service.FileRegistry.update_registration')
    @patch('shutil.copyfileobj')
    @patch('builtins.open')
    def test_invalid_file_body(self, open_patch, copyfileobj_patch, update_registration_patch):
        update_registration_patch.return_value = True
        copyfileobj_patch.return_value = DummyFile()
        open_patch.return_value.__exit__.return_value = None

        self.__request.method = 'POST'
        self.__request.POST['invalid_file'] = DummyFile()

        response = file_upload_service_with_default_notification(None, self.__request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(not update_registration_patch.called)
        self.assertTrue(not copyfileobj_patch.called)
        self.assertTrue(not open_patch.called)
import tempfile
