import unittest
from pyramid.testing import DummyRequest
from pyramid import testing
from hpz.frs.registration_service import put_file_registration_service
from pyramid.registry import Registry
import json
from unittest.mock import patch

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

    @patch('hpz.frs.registration_service.persist_registration_request')
    def test_registration(self, persist_patch):

        persist_patch.return_value = None

        self.__request.method = 'PUT'
        self.__request.json_body = {'uid': '1234'}

        response = put_file_registration_service(None, self.__request)

        self.assertEqual(response.status_code, 200)

        response_json = json.loads(str(response.body, encoding='UTF-8'))
        self.assertTrue('url' in response_json)
        self.assertTrue(persist_patch.called)
