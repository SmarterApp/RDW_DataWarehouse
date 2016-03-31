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
import shutil
import tempfile
from edcore.watch.file_hasher import MD5Hasher, FileHasherException
from edcore.tests.watch.common_test_utils import get_file_hash, write_something_to_a_blank_file


class TestHasher(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.tmp_dir_1 = tempfile.mkdtemp(prefix='tmp_1')

    def tearDown(self):
        shutil.rmtree(self.tmp_dir_1, ignore_errors=True)

    def test_get_file_hash(self):
        test_md5_hasher_hex = MD5Hasher(block_size=64, hex_digest=True)
        test_md5_hasher_binary = MD5Hasher(hex_digest=False)
        test_file_path = write_something_to_a_blank_file(dir_path=self.tmp_dir_1)
        hex_digest, digest = get_file_hash(test_file_path)
        self.assertEqual(test_md5_hasher_hex.get_file_hash(test_file_path), hex_digest)
        self.assertEqual(test_md5_hasher_binary.get_file_hash(test_file_path), digest)

    def test_get_file_hash_for_invalid_file(self):
        test_md5_hasher_hex = MD5Hasher()
        self.assertRaises(FileHasherException, test_md5_hasher_hex.get_file_hash, '/tmp/xyz.gpg')
