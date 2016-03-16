__author__ = 'smuhit'

import os

from sqlalchemy.sql import select

from edware_testing_automation.frontend_tests.common_session_share_steps import SessionShareHelper
from edware_testing_automation.hpz.hpz_helper import HpzHelper
from edware_testing_automation.utils.db_connector import DBConnection
from edware_testing_automation.utils.db_utils import create_connection
from edware_testing_automation.utils.preferences import preferences, HPZ
from edware_testing_automation.utils.test_base import DOWNLOADS

HPZ_UPLOAD_DIRECTORY = preferences(HPZ.uploads_directory) + '/'
DOWNLOAD_DIRECTORY = DOWNLOADS + "/"


class HpzSadPathTests(HpzHelper, SessionShareHelper):
    def __init__(self, *args, **kwargs):
        HpzHelper.__init__(self, *args, **kwargs)

    def tearDown(self):
        for file_to_delete in self.files_to_delete:
            if os.path.exists(file_to_delete):
                os.remove(file_to_delete)

    def setUp(self):
        self.test_file_name = 'test_file.tar'
        self.test_file = os.path.join(os.path.dirname(__file__), 'resources', self.test_file_name)
        old_downloaded_file = DOWNLOAD_DIRECTORY + self.test_file_name
        if os.path.exists(old_downloaded_file):
            os.remove(old_downloaded_file)
        if not os.path.exists(HPZ_UPLOAD_DIRECTORY):
            os.makedirs(HPZ_UPLOAD_DIRECTORY)
        if not os.path.exists(DOWNLOAD_DIRECTORY):
            os.makedirs(DOWNLOAD_DIRECTORY)
        self.files_to_delete = []
        self.base_url = self.get_hpz_url()
        self.reg_endpoint = preferences(HPZ.registration_endpoint)
        self.files_endpoint = preferences(HPZ.files_endpoint)
        self.reg_url = self.base_url + self.reg_endpoint
        self.upload_url = self.base_url + self.files_endpoint
        self.db = preferences(HPZ.db_main_url)
        self.db_schema = preferences(HPZ.db_schema_name)
        self.reg_table = preferences(HPZ.db_registration_table)
        create_connection(self.db, self.db_schema, 'hpz')

    def verify_registration_not_in_db(self, reg_id):
        with DBConnection(name='hpz') as connector:
            table = connector.get_table(self.reg_table)
            query = select([table]).where(table.c.registration_id == reg_id)
            result = connector.execute(query).fetchall()
            self.assertFalse(result, 'Registration is stored in db')

    def verify_file_location_not_in_db(self, reg_id):
        with DBConnection(name='hpz') as connector:
            table = connector.get_table(self.reg_table)
            query = select([table.c.file_path]).where(table.c.registration_id == reg_id)
            result = connector.execute(query).fetchall()
            self.assertEqual(result, [(None,)])

    def test_register_with_invalid_payload(self):
        self.set_payload({'blah': 'blah'})
        self.send_request('PUT', base=self.base_url, end_point=self.reg_endpoint)
        self.check_response_code(200)
        self.check_resp_list_fields(expected_fields=[])

    def test_upload_before_registration(self):
        self.set_headers_for_file_upload(self.test_file_name, self.test_file)
        reg_id = 'non-existant-registration'
        upload_endpoint = self.files_endpoint + reg_id
        self.send_request('POST', base=self.base_url, end_point=upload_endpoint)
        self.check_response_code(200)
        self.verify_registration_not_in_db(reg_id)

    def test_upload_with_no_file(self):
        self.set_headers_for_file_registration('dummy_user')
        self.send_request('PUT', base=self.base_url, end_point=self.reg_endpoint)
        self.check_response_code(200)

        self.check_resp_list_fields(expected_fields=["url", "registration_id", "web_url"])
        reg_id = self.get_response_field('registration_id')

        self.set_headers_for_file_upload(self.test_file_name, self.test_file)
        self.set_non_json_payload(None)
        upload_endpoint = self.files_endpoint + reg_id
        self.send_request('POST', base=self.base_url, end_point=upload_endpoint)
        self.check_response_code(200)
        self.verify_file_location_not_in_db(reg_id)

    def test_upload_with_incorrect_header(self):
        self.set_headers_for_file_registration('dummy_user')
        self.send_request('PUT', base=self.base_url, end_point=self.reg_endpoint)
        self.check_response_code(200)

        self.check_resp_list_fields(expected_fields=["url", "registration_id", "web_url"])
        reg_id = self.get_response_field('registration_id')

        self.set_headers_for_file_upload(self.test_file_name, self.test_file)
        self.remove_request_header('File-Name')
        upload_endpoint = self.files_endpoint + reg_id
        self.send_request('POST', base=self.base_url, end_point=upload_endpoint)
        self.check_response_code(200)
        self.verify_file_location_not_in_db(reg_id)

    def test_download_file_not_registered(self):
        self.set_headers_for_file_registration('jmacey')
        self.send_request('PUT', base=self.base_url, end_point=self.reg_endpoint)
        self.check_response_code(200)
        self.check_resp_list_fields(expected_fields=["url", "registration_id", "web_url"])
        url = self.get_response_field('web_url')
        bad_url = list(url)
        bad_url[-1] = 'x'
        bad_url = ''.join(bad_url)

        self.open_requested_page_redirects_login_page("hpz download url", url=bad_url)
        self.enter_login_credentials('jmacey', 'jmacey1234')

        downloaded_file = DOWNLOAD_DIRECTORY + self.test_file_name
        self.assertFalse(os.path.isfile(downloaded_file))

    def test_download_file_not_owner(self):
        self.set_headers_for_file_registration('shall')
        self.send_request('PUT', base=self.base_url, end_point=self.reg_endpoint)
        self.check_response_code(200)
        self.check_resp_list_fields(expected_fields=["url", "registration_id", "web_url"])
        url = self.get_response_field('web_url')

        self.open_requested_page_redirects_login_page("hpz download url", url=url)
        self.enter_login_credentials('jmacey', 'jmacey1234')

        downloaded_file = DOWNLOAD_DIRECTORY + self.test_file_name
        self.assertFalse(os.path.isfile(downloaded_file))

    def test_download_file_still_processing(self):
        self.set_headers_for_file_registration('jmacey')
        self.send_request('PUT', base=self.base_url, end_point=self.reg_endpoint)
        self.check_response_code(200)
        self.check_resp_list_fields(expected_fields=["url", "registration_id", "web_url"])
        url = self.get_response_field('web_url')

        self.open_requested_page_redirects_login_page("hpz download url", url=url)
        self.enter_login_credentials('jmacey', 'jmacey1234')

        downloaded_file = DOWNLOAD_DIRECTORY + self.test_file_name
        self.assertFalse(os.path.isfile(downloaded_file))
