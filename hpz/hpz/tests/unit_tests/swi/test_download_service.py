import unittest
from pyramid.testing import DummyRequest
from hpz.swi.download_service import download_file, is_file_exist
from unittest.mock import patch
from edauth.security.user import User

__author__ = 'npandey'


class RegistrationTest(unittest.TestCase):

    def setUp(self):
        self.dummy_uid = 'bbunny'
        self.dummy_user = User()
        self.dummy_user.set_uid(self.dummy_uid)
        self.dummy_file_path = 'tmp/filename.zip'
        self.dummy_file_name = 'ActualName.zip'
        self.__request = DummyRequest()

    def tearDown(self):
        self.__request = None

    @patch('hpz.swi.download_service.authenticated_userid')
    @patch('hpz.frs.registration_service.FileRegistry.get_registration_info')
    @patch('os.path.isfile')
    @patch('hpz.swi.download_service.logger.info')
    def test_download_file(self, logger_patch, is_file_patch, get_reg_info_patch, auth_userid_patch):
        auth_userid_patch.return_value = self.dummy_user
        get_reg_info_patch.return_value = {"user_id": self.dummy_uid, "file_path": self.dummy_file_path,
                                           "file_name": self.dummy_file_name}
        is_file_patch.return_value = True
        logger_patch.return_value = None

        self.__request.method = 'GET'
        self.__request.matchdict['reg_id'] = '1234'

        response = download_file(None, self.__request)

        self.assertEqual(response.status_code, 200)

        headers = response.headers

        self.assertEqual(len(headers), 3)
        self.assertEqual(headers['X-Sendfile'], self.dummy_file_path)
        self.assertEqual(headers['Content-Type'], '')
        self.assertEqual(headers['Content-Disposition'], 'attachment; filename=ActualName.zip')
        logger_patch.assert_called_once_with('File %s was successfully downloaded', 'tmp/filename.zip')

    @patch('hpz.swi.download_service.authenticated_userid')
    @patch('hpz.frs.registration_service.FileRegistry.get_registration_info')
    @patch('os.path.isfile')
    @patch('hpz.swi.download_service.logger.error')
    def test_download_file_not_registered(self, logger_patch, is_file_patch, get_reg_info_patch, auth_userid_patch):
        auth_userid_patch.return_value = self.dummy_user
        get_reg_info_patch.return_value = None
        is_file_patch.return_value = True
        logger_patch.return_value = None

        self.__request.method = 'GET'
        self.__request.matchdict['reg_id'] = '12345'

        response = download_file(None, self.__request)

        self.assertEqual(response.status_code, 404)
        logger_patch.assert_called_once_with('No file record is registered with requested id %s', '12345')

    @patch('hpz.swi.download_service.authenticated_userid')
    @patch('hpz.frs.registration_service.FileRegistry.get_registration_info')
    @patch('os.path.isfile')
    @patch('hpz.swi.download_service.logger.error')
    def test_download_file_not_owner(self, logger_patch, is_file_patch, get_reg_info_patch, auth_userid_patch):
        auth_userid_patch.return_value = self.dummy_user
        reg_user_id = 'dduck'
        get_reg_info_patch.return_value = {"user_id": reg_user_id, "file_path": self.dummy_file_path,
                                           "file_name": self.dummy_file_name}
        is_file_patch.return_value = True
        logger_patch.return_value = None

        self.__request.method = 'GET'
        self.__request.matchdict['reg_id'] = '12345'

        response = download_file(None, self.__request)

        self.assertEqual(response.status_code, 404)
        logger_patch.assert_called_once_with('User %s is not owner of the file with registration id %s', 'bbunny', '12345')

    @patch('hpz.swi.download_service.authenticated_userid')
    @patch('hpz.frs.registration_service.FileRegistry.get_registration_info')
    @patch('os.path.isfile')
    @patch('hpz.swi.download_service.logger.error')
    def test_download_file_still_processing(self, logger_patch, is_file_patch, get_reg_info_patch, auth_userid_patch):
        auth_userid_patch.return_value = self.dummy_user
        get_reg_info_patch.return_value = {"user_id": self.dummy_uid, "file_path": None, "file_name": None}
        is_file_patch.return_value = True
        logger_patch.return_value = None

        self.__request.method = 'GET'
        self.__request.matchdict['reg_id'] = '12345'

        response = download_file(None, self.__request)

        self.assertEqual(response.status_code, 404)
        logger_patch.assert_called_once_with('File with registration id %s is not yet available', '12345')

    @patch('hpz.swi.download_service.authenticated_userid')
    @patch('hpz.frs.registration_service.FileRegistry.get_registration_info')
    @patch('os.path.isfile')
    @patch('hpz.swi.download_service.logger.error')
    def test_download_file_not_on_disk(self, logger_patch, is_file_patch, get_reg_info_patch, auth_userid_patch):
        auth_userid_patch.return_value = self.dummy_user
        get_reg_info_patch.return_value = {"user_id": self.dummy_uid, "file_path": self.dummy_file_path,
                                           "file_name": self.dummy_file_name}
        is_file_patch.return_value = False
        logger_patch.return_value = None

        self.__request.method = 'GET'
        self.__request.matchdict['reg_id'] = '12345'

        response = download_file(None, self.__request)

        self.assertEqual(response.status_code, 404)
        logger_patch.assert_called_once_with('File %s is registered, but does not exist on disk', 'tmp/filename.zip')

    @patch('hpz.swi.download_service.authenticated_userid')
    @patch('hpz.frs.registration_service.FileRegistry.get_registration_info')
    def test_file_exists_file_not_exist(self, get_reg_info_patch, auth_userid_patch):
        auth_userid_patch.return_value = self.dummy_user
        get_reg_info_patch.return_value = {"user_id": self.dummy_uid, "file_path": self.dummy_file_path,
                                           "file_name": self.dummy_file_name}
        self.__request.method = 'GET'
        self.__request.matchdict['reg_id'] = '12345'
        response = is_file_exist(None, self.__request)
        self.assertEqual(response.status_code, 404)

    @patch('hpz.swi.download_service.authenticated_userid')
    @patch('hpz.frs.registration_service.FileRegistry.get_registration_info')
    @patch('os.path.isfile')
    @patch('hpz.swi.download_service.logger.info')
    def test_file_exists_for_valid_file(self, logger_patch, is_file_patch, get_reg_info_patch, auth_userid_patch):
        auth_userid_patch.return_value = self.dummy_user
        get_reg_info_patch.return_value = {"user_id": self.dummy_uid, "file_path": self.dummy_file_path,
                                           "file_name": self.dummy_file_name}
        is_file_patch.return_value = True
        logger_patch.return_value = None
        self.__request.method = 'GET'
        self.__request.matchdict['reg_id'] = '1234'
        response = is_file_exist(None, self.__request)
        self.assertEqual(response.status_code, 200)
