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
