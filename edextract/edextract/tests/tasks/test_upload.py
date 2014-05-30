import unittest
from unittest.mock import patch, ANY
from edextract.tasks.upload import upload

__author__ = 'ablum'


class TestUpload(unittest.TestCase):
    def setUp(self):
        pass

    @patch('edextract.tasks.upload.insert_extract_stats')
    @patch('edextract.tasks.upload.http_file_upload')
    def test_upload(self, file_upload_patch, insert_stats_patch):
        file_upload_patch.side_effect = None
        insert_stats_patch.return_value = None
        http_info = {'url': 'http://test_url.com'}

        upload('test_request_id', 'test_file_name', http_info)

        file_upload_patch.assert_called_once_with('test_file_name', 'http://test_url.com')
        self.assertTrue(insert_stats_patch.called)
        self.assertEqual(2, insert_stats_patch.call_count)

    @patch('edextract.tasks.upload.insert_extract_stats')
    @patch('edextract.tasks.upload.http_file_upload')
    def test_upload_task(self, file_upload_patch, insert_stats_patch):
        file_upload_patch.side_effect = None
        insert_stats_patch.return_value = None
        http_info = {'url': 'http://test_url.com'}

        result = upload.apply(args=['test_request_id', 'test_file_name', http_info])

        file_upload_patch.assert_called_once_with('test_file_name', 'http://test_url.com')
        self.assertTrue(insert_stats_patch.called)
        self.assertEqual(2, insert_stats_patch.call_count)

    @patch('edextract.tasks.upload.extract.MAX_RETRY')
    @patch('edextract.tasks.upload.insert_extract_stats')
    @patch('edextract.tasks.upload.http_file_upload')
    def test_upload_connection_error(self, file_upload_patch, insert_stats_patch, max_retry_patch):
        max_retry_patch.return_value = 2
        file_upload_patch.side_effect = ConnectionError
        insert_stats_patch.return_value = None
        http_info = {'url': 'http://test_url.com'}

        upload.apply(args=['test_request_id', 'test_file_name', http_info])

        file_upload_patch.assert_called_with('test_file_name', 'http://test_url.com')
        self.assertEqual(2, file_upload_patch.call_count)
        self.assertTrue(insert_stats_patch.called)
        self.assertEqual(4, insert_stats_patch.call_count)
