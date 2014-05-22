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
        reg.settings = {'hpz.frs.upload_base_path': '/dev/null', 'hpz.frs.file_size_limit': '1024'}
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)

    def tearDown(self):
        self.__request = None

    @patch('hpz.frs.upload_service.FileRegistry.update_registration')
    @patch('shutil.copyfileobj')
    @patch('builtins.open')
    def test_file_upload_service(self, open_patch, copyfileobj_patch, update_registration_patch):
        update_registration_patch.return_value = True
        copyfileobj_patch.return_value = DummyFile()
        open_patch.return_value.__exit__.return_value = None

        self.__request.method = 'POST'
        self.__request.POST['file'] = DummyFile()

        response = file_upload_service(None, self.__request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(update_registration_patch.called)

    @patch('hpz.frs.upload_service.FileRegistry.update_registration')
    def test_file_upload_service_not_registered(self, update_registration_patch):
        test_logger = logging.getLogger(upload_service.__name__)
        with mock.patch.object(test_logger, 'error') as mock_error:

            update_registration_patch.return_value = False

            self.__request.method = 'POST'
            self.__request.POST['file'] = DummyFile()

            response = file_upload_service(None, self.__request)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(update_registration_patch.called)
            self.assertTrue(mock_error.called)

    @patch('hpz.frs.upload_service.FileRegistry.update_registration')
    @patch('shutil.copyfileobj')
    @patch('builtins.open')
    @patch('hpz.frs.upload_service.logger.error')
    def test_file_creation_error(self, logger_patch, open_patch, copyfileobj_patch, update_registration_patch):
        update_registration_patch.return_value = True
        copyfileobj_patch.return_value = DummyFile()
        logger_patch.return_value = None
        open_patch.side_effect = IOError('Message')

        self.__request.method = 'POST'
        self.__request.POST['file'] = DummyFile()

        response = file_upload_service(None, self.__request)

        logger_patch.assert_called_once_with('Cannot complete file copying due to: Message')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(update_registration_patch.called)

    @patch('hpz.frs.upload_service.FileRegistry.update_registration')
    @patch('shutil.copyfileobj')
    @patch('builtins.open')
    @patch('hpz.frs.upload_service.logger.warning')
    @patch('os.path.getsize')
    def test_file_creation_error(self, getsize_patch, logger_patch, open_patch, copyfileobj_patch, update_registration_patch):
        update_registration_patch.return_value = True
        copyfileobj_patch.return_value = DummyFile()
        logger_patch.return_value = None
        getsize_patch.return_value = 1025
        open_patch.return_value.__exit__.return_value = None

        self.__request.method = 'POST'
        self.__request.POST['file'] = DummyFile()

        response = file_upload_service(None, self.__request)

        logger_patch.assert_called_once_with('File [%s] exceeds recommended size limit', '/dev/null/a1-b2-c3-d4-e5.zip')

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
        __invalid_request.headers['InvalidFileext'] = 'zip'

        self.__request.method = 'POST'
        self.__request.POST['file'] = DummyFile()

        response = file_upload_service(None, __invalid_request)

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

        response = file_upload_service(None, self.__request)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(not update_registration_patch.called)
        self.assertTrue(not copyfileobj_patch.called)
        self.assertTrue(not open_patch.called)
