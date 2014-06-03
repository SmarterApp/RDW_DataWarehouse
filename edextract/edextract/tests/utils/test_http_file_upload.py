import unittest
from unittest.mock import patch, Mock, mock_open
from edextract.utils.http_file_upload import http_file_upload
from edcore.exceptions import RemoteCopyError

__author__ = 'ablum'


class TestHTTPFileUpload(unittest.TestCase):
    def setUp(self):
        pass

    @patch('edextract.utils.http_file_upload.__create_stream')
    @patch('edextract.utils.http_file_upload.api.post')
    def test_http_file_upload(self, post_patch, create_stream_patch):
        stream_mock = Mock()
        stream_mock.content_type = 'test_content_type'
        create_stream_patch.return_value = stream_mock
        response_mock = Mock()
        response_mock.status_code = 200
        post_patch.return_value = response_mock

        url = 'http://www.this_is_a_dummy_url.com'

        with patch('builtins.open', mock_open(), create=True):
            http_file_upload('filename', url)

        post_patch.assert_called_once_with('http://www.this_is_a_dummy_url.com', data=stream_mock, headers={'Content-Type': stream_mock.content_type, 'File-Name': 'filename'})

    @patch('edextract.utils.http_file_upload.__create_stream')
    @patch('edextract.utils.http_file_upload.api.post')
    def test_http_file_upload_error(self, post_patch, create_stream_patch):
        stream_mock = Mock()
        stream_mock.content_type = 'test_content_type'
        create_stream_patch.return_value = stream_mock
        response_mock = Mock()
        response_mock.status_code = 200
        post_patch.side_effect = RemoteCopyError('ooops!')

        url = 'http://www.this_is_a_dummy_url.com'

        with patch('builtins.open', mock_open(), create=True), self.assertRaises(RemoteCopyError) as context:
            http_file_upload('filename', url)

        post_patch.assert_called_once_with('http://www.this_is_a_dummy_url.com', data=stream_mock, headers={'Content-Type': stream_mock.content_type, 'File-Name': 'filename'})
        self.assertEquals(context.exception.msg, 'ooops!')
