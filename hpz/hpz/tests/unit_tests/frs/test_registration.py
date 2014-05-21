import logging
import unittest
import mock
from pyramid.testing import DummyRequest
from pyramid import testing
from hpz.frs import registration_service
from hpz.frs.registration_service import put_file_registration_service
from pyramid.registry import Registry
import json
from unittest.mock import patch, Mock, ANY

__author__ = 'npandey'


class RegistrationTest(unittest.TestCase):

    def setUp(self):
        self.__request = DummyRequest()
        reg = Registry()
        reg.settings = {}
        self.__config = testing.setUp(registry=reg, request=self.__request, hook_zca=False)
        self.__config.add_route('download', '/{reg_id}')

    def tearDown(self):
        self.__request = None

    @patch('hpz.frs.registration_service.FileRegistry.register_request')
    def test_registration(self, persist_patch):

        persist_patch.return_value = None

        self.__request.method = 'PUT'
        self.__request.json_body = {'uid': '1234'}

        response = put_file_registration_service(None, self.__request)

        self.assertEqual(response.status_code, 200)

        response_json = json.loads(str(response.body, encoding='UTF-8'))
        self.assertTrue('url' in response_json)
        self.assertTrue(persist_patch.called)

    @patch('hpz.frs.registration_service.FileRegistry.register_request')
    def test_registration_incorrect_payload(self, persist_patch):
        test_logger = logging.getLogger(registration_service.__name__)
        with mock.patch.object(test_logger, 'error') as mock_debug:
            persist_patch.return_value = None

            self.__request.method = 'PUT'
            self.__request.json_body = {}

            response = put_file_registration_service(None, self.__request)

            self.assertEqual(response.status_code, 200)

            response_json = json.loads(str(response.body, encoding='UTF-8'))
            self.assertTrue('url' not in response_json)
            self.assertTrue(not persist_patch.called)
            self.assertTrue(mock_debug.called)
