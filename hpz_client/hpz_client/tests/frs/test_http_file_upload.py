# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

import unittest

from pyramid import testing
from unittest.mock import patch, Mock, mock_open
from pyramid.registry import Registry
from pyramid.testing import DummyRequest

from edcore.exceptions import RemoteCopyError
from hpz_client.frs.http_file_upload import http_file_upload
from hpz_client.frs.config import Config, initialize


__author__ = 'ablum'


class TestHTTPFileUpload(unittest.TestCase):
    def setUp(self):
        self.reg = Registry()
        self.__request = DummyRequest()
        self.__config = testing.setUp(registry=self.reg, request=self.__request, hook_zca=False)
        settings = {Config.HPZ_FILE_UPLOAD_BASE_URL: 'http://somehost:82/files'}
        initialize(settings)

    @patch('hpz_client.frs.http_file_upload.__create_stream')
    @patch('hpz_client.frs.http_file_upload.api.post')
    def test_http_file_upload(self, post_patch, create_stream_patch):
        stream_mock = Mock()
        stream_mock.content_type = 'test_content_type'
        create_stream_patch.return_value = stream_mock
        response_mock = Mock()
        response_mock.status_code = 200
        post_patch.return_value = response_mock
        reg_id = 'a1-b2-c3-d4-e5'

        with patch('builtins.open', mock_open(), create=True):
            http_file_upload('filename', reg_id)

        post_patch.assert_called_once_with('http://somehost:82/files/a1-b2-c3-d4-e5', data=stream_mock, headers={'Content-Type': stream_mock.content_type, 'File-Name': 'filename'}, verify=True)

    @patch('hpz_client.frs.http_file_upload.__create_stream')
    @patch('hpz_client.frs.http_file_upload.api.post')
    def test_http_file_upload_error(self, post_patch, create_stream_patch):
        stream_mock = Mock()
        stream_mock.content_type = 'test_content_type'
        create_stream_patch.return_value = stream_mock
        post_patch.side_effect = RemoteCopyError('ooops!')
        response_mock = Mock()
        response_mock.status_code = 200
        reg_id = 'a1-b2-c3-d4-e5'

        with patch('builtins.open', mock_open(), create=True), self.assertRaises(RemoteCopyError) as context:
            http_file_upload('filename', reg_id)

        post_patch.assert_called_once_with('http://somehost:82/files/a1-b2-c3-d4-e5', data=stream_mock, headers={'Content-Type': stream_mock.content_type, 'File-Name': 'filename'}, verify=True)
        self.assertEquals(context.exception.msg, 'ooops!')
