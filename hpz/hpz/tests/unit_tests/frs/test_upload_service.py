__author__ = 'tshewchuk'
"""
Unit tests for the file upload service of HPZ.
"""

import unittest
from unittest.mock import patch
from pyramid.testing import DummyRequest
from pyramid import testing
import os
from hpz.frs.upload_service import file_upload_service
from pyramid.registry import Registry


class DummyFile:
    def __init__(self):
        self.file = None
        self.read = None


class UploadTest(unittest.TestCase):

    def setUp(self):
        self.__request = DummyRequest()
        self.__request.matchdict['registration_id'] = ''
        self.__request.headers['Filename'] = ''
        reg = Registry()
        reg.settings = {'hpz.frs.upload_base_path': '/dev/null'}
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)

    def tearDown(self):
        self.__request = None

    @patch('hpz.frs.upload_service.FileRegistry.file_upload_request')
    @patch('shutil.copyfileobj')
    @patch('builtins.open')
    def test_file_upload_service(self, open_patch, copyfileobj_patch, file_upload_patch):
        file_upload_patch.return_value = DummyFile()
        copyfileobj_patch.return_value = None
        open_patch.return_value.__exit__.return_value = None

        self.__request.method = 'POST'
        self.__request.POST['file'] = DummyFile()

        response = file_upload_service(None, self.__request)

        self.assertEqual(response.status_code, 200)
