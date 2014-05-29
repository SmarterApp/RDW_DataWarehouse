import unittest
from pyramid.testing import DummyRequest
from hpz.swi.download_service import download_file
from unittest.mock import patch
from edauth.security.user import User

__author__ = 'npandey'


class RegistrationTest(unittest.TestCase):

    def setUp(self):
        self.__request = DummyRequest()

    def tearDown(self):
        self.__request = None

    @patch('hpz.swi.download_service.authenticated_userid')
    @patch('hpz.frs.registration_service.FileRegistry.get_registration_info')
    @patch('os.path.isfile')
    def test_download_file(self, is_file_patch, get_reg_info_patch, auth_userid_patch):
        dummy_uid = 'bbunny'
        dummy_user = User()
        dummy_user.set_uid(dummy_uid)
        dummy_file_path = 'tmp/filename.zip'
        auth_userid_patch.return_value = dummy_user
        get_reg_info_patch.return_value = (dummy_uid, dummy_file_path)
        is_file_patch.return_value = True

        self.__request.method = 'GET'
        self.__request.matchdict['reg_id'] = '1234'

        response = download_file(None, self.__request)

        self.assertEqual(response.status_code, 200)

        headers = response.headers

        self.assertEqual(len(headers), 3)
        self.assertEqual(headers['X-Sendfile'], dummy_file_path)
        self.assertEqual(headers['Content-Type'], '')
        self.assertEqual(headers['Content-Disposition'], 'attachment; filename=filename.zip')
