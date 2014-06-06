__author__ = 'tshewchuk'
"""
Unit test for archive_with_encryption module.
"""

import unittest
from unittest.mock import patch

from edextract.tasks.archive_with_encryption import archive_with_encryption
from edextract.settings.config import Config, setup_settings


class TestArchiveWithEncryption(unittest.TestCase):

    def setUp(self):
        settings = {Config.HOMEDIR: '~/.gpg',
                    Config.BINARYFILE: 'gpg',
                    Config.KEYSERVER: 'the_key_keeper'}
        setup_settings(settings)

    @patch('edextract.tasks.archive_with_encryption.encrypted_archive_files')
    @patch('edextract.tasks.archive_with_encryption.insert_extract_stats')
    def test_archive_task(self, insert_stats_patch, archive_patch):
        request_id = '1'
        recipients = 'whatzittuya'
        zip_file = 'output.zip'
        csv_dir = 'csv/file/dir'

        result = archive_with_encryption.apply(args=[request_id, recipients, zip_file, csv_dir])
        result.get()

        archive_patch.assert_called_once_with(csv_dir, recipients, zip_file, keyserver='the_key_keeper', gpgbinary='gpg', homedir='~/.gpg')
        self.assertTrue(insert_stats_patch.called)
        self.assertEqual(2, insert_stats_patch.call_count)
