import unittest
from unittest.mock import patch, Mock
from edextract.utils.http_file_upload import http_file_upload

__author__ = 'ablum'


class TestHTTPFileUpload(unittest.TestCase):
    def setUp(self):
        pass

    @patch('edextract.utils.http_file_upload.__create_stream')
    @patch('edextract.utils.http_file_upload.post')
    def test_http_file_upload(self, post_patch, create_stream_patch):
        stream_mock = Mock()
        stream_mock.content_type = 'test_content_type'
        create_stream_patch.return_value = stream_mock
        response_mock = Mock()
        response_mock.status_code = 200
        post_patch.return_value = response_mock

        http_file_upload('filename', 'http://www.this_is_a_dummy_url.com')

        post_patch.assert_called_once_with('http://www.this_is_a_dummy_url.com', data=stream_mock, headers={'Content-Type': stream_mock.content_type, 'File-Name': 'filename'})
