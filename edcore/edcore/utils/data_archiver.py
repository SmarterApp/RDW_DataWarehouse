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

'''
Created on Dec 2, 2013

@author: tosako
'''

import os
import io
import gnupg
import tempfile
from edcore.utils.utils import archive_files
from edcore.exceptions import GPGPublicKeyException, GPGException


def import_recipient_keys(gpg, recipients, keyserver):
    keys = gpg.search_keys(recipients, keyserver)
    if not keys:
        raise GPGPublicKeyException()
    key_ids = [key['keyid'] for key in keys]
    gpg.recv_keys(keyserver, *key_ids)


def encrypted_archive_files(dirname, recipients, outputfile, homedir=None, keyserver=None, gpgbinary='gpg'):
    '''
    create encrypted archive file.
    '''
    archive_memory_file = io.BytesIO()
    archive_files(dirname, archive_memory_file)
    encrypt_file(archive_memory_file, recipients, outputfile, homedir, keyserver, gpgbinary)


def encrypt_file(file, recipients, outputfile, homedir=None, keyserver=None, gpgbinary='gpg', passphrase=None, sign=None):
    try:
        # a bug in celery config that convert None into 'None' instead of None
        if keyserver is None or keyserver == 'None':
            gpg = gnupg.GPG(gnupghome=os.path.abspath(homedir), gpgbinary=gpgbinary, verbose=True)
            if passphrase is None:
                gpg.encrypt_file(file, recipients, output=outputfile, always_trust=True)
            else:
                gpg.encrypt_file(file, recipients, output=outputfile, sign=sign, passphrase=passphrase)
        else:
            with tempfile.TemporaryDirectory() as gpghomedir:
                gpg = gnupg.GPG(gnupghome=gpghomedir, gpgbinary=gpgbinary)
                import_recipient_keys(gpg, recipients, keyserver)
                gpg.encrypt_file(file, recipients, output=outputfile, always_trust=True)
    except GPGPublicKeyException:
        # recoverable error because of public key server
        raise
    except Exception as e:
        # unrecoverable error
        raise GPGException(str(e))
    # if output file does not exist, it's because directory is not writable or recipients were not available
    if not os.path.exists(outputfile):
        raise GPGException("failed to generate: " + outputfile)
