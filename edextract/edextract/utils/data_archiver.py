'''
Created on Dec 2, 2013

@author: tosako
'''

import os
import io
import gnupg
import tempfile
from edcore.utils.utils import archive_files
from edextract.exceptions import GPGPublicKeyException, GPGException


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
    try:
        archive_memory_file = io.BytesIO()

        archive_files(dirname, archive_memory_file)

        # a bug in celery config that convert None into 'None' instead of None
        if keyserver is None or keyserver == 'None':
            gpg = gnupg.GPG(gnupghome=os.path.abspath(homedir), gpgbinary=gpgbinary, verbose=True)
            gpg.encrypt(archive_memory_file.getvalue(), recipients, output=outputfile, always_trust=True)
        else:
            with tempfile.TemporaryDirectory() as gpghomedir:
                gpg = gnupg.GPG(gnupghome=gpghomedir, gpgbinary=gpgbinary)
                import_recipient_keys(gpg, recipients, keyserver)
                gpg.encrypt(archive_memory_file.getvalue(), recipients, output=outputfile, always_trust=True)
    except GPGPublicKeyException:
        # recoverable error because of public key server
        raise
    except Exception as e:
        # unrecoverable error
        raise GPGException(str(e))
    # if output file does not exist, it's because directory is not writable or recipients were not available
    if not os.path.exists(outputfile):
        raise GPGException("failed to generate: " + outputfile)
