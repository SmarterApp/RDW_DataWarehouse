import unittest
from pyramid.testing import DummyRequest
from hpz.swi.download_service import download_file
from unittest.mock import patch

__author__ = 'npandey'


class RegistrationTest(unittest.TestCase):

    def setUp(self):
        self.__request = DummyRequest()

    def tearDown(self):
        self.__request = None

    @patch('hpz.frs.registration_service.FileRegistry.get_file_info')
    def test_download_file(self, file_info_patch):
        dummy_file_path = 'tmp/filename.zip'
        dummy_file_name = 'ActualName.zip'
        file_info_patch.return_value = dummy_file_path, dummy_file_name

        self.__request.method = 'GET'
        self.__request.matchdict['reg_id'] = '1234'

        response = download_file(None, self.__request)

        self.assertEqual(response.status_code, 200)

        headers = response.headers

        self.assertEqual(len(headers), 3)
        self.assertEqual(headers['X-Sendfile'], dummy_file_path)
        self.assertEqual(headers['Content-Type'], '')
        self.assertEqual(headers['Content-Disposition'], 'attachment; filename=ActualName.zip')
