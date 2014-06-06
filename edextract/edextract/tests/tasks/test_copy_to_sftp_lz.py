__author__ = 'tshewchuk'
"""
Unit test for copy_to_sftp_lz module.
"""

import unittest
from unittest.mock import patch

from edextract.celery import setup_celery
from edcore.exceptions import RemoteCopyError
from edextract.exceptions import ExtractionError
from edextract.tasks.copy_to_sftp_lz import copy_to_sftp_lz
from edextract.settings.config import Config, setup_settings


class TestCopyToSFTPLZ(unittest.TestCase):

    def setUp(self):
        settings = {Config.HOMEDIR: '~/.gpg',
                    Config.BINARYFILE: 'gpg',
                    Config.KEYSERVER: 'the_key_keeper',
                    Config.PICKUP_ROUTE_BASE_DIR: 'route',
                    'extract.celery.CELERY_ALWAYS_EAGER': 'True',
                    'extract.retries_allowed': '1',
                    'extract.retry_delay': '3'}
        setup_celery(settings)
        setup_settings(settings)

    @patch('edextract.tasks.copy_to_sftp_lz.insert_extract_stats')
    @patch('edextract.utils.file_remote_copy.copy')
    def test_copy_to_sftp_lz_success(self, file_upload_patch, insert_stats_patch):
        file_upload_patch.side_effect = None
        insert_stats_patch.side_effect = None
        insert_stats_patch.return_value = None
        request_id = 'test_request_id'
        src_file_name = 'test_file_name.zip'
        tenant = 'NJ'
        gatekeeper = 'the_gatekeeper'
        sftp_info = ['hostname', 'sftp_username', 'private_key_file']

        result = copy_to_sftp_lz.apply(args=[request_id, src_file_name, tenant, gatekeeper, sftp_info], kwargs={'timeout': 1800})
        result.get()

        file_upload_patch.assert_called_once_with('test_file_name.zip', 'hostname', 'NJ', 'the_gatekeeper', 'sftp_username',
                                                  'private_key_file', timeout=1800)
        self.assertTrue(insert_stats_patch.called)
        self.assertEqual(2, insert_stats_patch.call_count)

    @patch('edextract.tasks.copy_to_sftp_lz.insert_extract_stats')
    @patch('edextract.utils.file_remote_copy.copy')
    def test_copy_to_sftp_lz_connection_error(self, file_upload_patch, insert_stats_patch):
        file_upload_patch.side_effect = RemoteCopyError('ooops!')
        insert_stats_patch.side_effect = None
        insert_stats_patch.return_value = None
        request_id = 'test_request_id'
        src_file_name = 'test_file_name.zip'
        tenant = 'NJ'
        gatekeeper = 'the_gatekeeper'
        sftp_info = ['hostname', 'sftp_username', 'private_key_file']

        results = copy_to_sftp_lz.apply(args=[request_id, src_file_name, tenant, gatekeeper, sftp_info])

        file_upload_patch.assert_called_with('test_file_name.zip', 'hostname', 'NJ', 'the_gatekeeper', 'sftp_username',
                                             'private_key_file', timeout=1800)
        self.assertEqual(2, file_upload_patch.call_count)
        self.assertTrue(insert_stats_patch.called)
        self.assertEqual(4, insert_stats_patch.call_count)

        self.assertRaises(ExtractionError, results.get)
