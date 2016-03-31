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

import tempfile
import hashlib


def get_file_hash(test_file_path):
    with open(test_file_path, 'rb') as f:
        md5 = hashlib.md5()
        for buf in iter(lambda: f.read(md5.block_size), b''):
            md5.update(buf)
        return md5.hexdigest(), md5.digest()


def write_something_to_a_blank_file(dir_path):
    with tempfile.NamedTemporaryFile(delete=False, dir=dir_path, prefix='source', suffix='.gpg') as test_file:
        test_file.write(b"test\n")
        test_file.flush()
        return test_file.name


def create_checksum_file(source_file_path, valid_check_sum=True):
    with open(source_file_path + '.done', 'wb') as checksum_file:
        hex_digest, _ = get_file_hash(source_file_path)
        if not valid_check_sum:
            checksum_file.write(bytes("MD5 =" + 'aaavfi385etegdg83kdgd', 'UTF-8'))
        else:
            checksum_file.write(bytes("MD5 =" + hex_digest, 'UTF-8'))
        checksum_file.flush()
        return checksum_file.name
