'''
Created on Dec 2, 2013

@author: tosako
'''

import os
import io
import zipfile
import gnupg
import tempfile
from edextract.exceptions import GPGPublicKeyException, GPGException

## TODO: Refactor this module to just contain archive_unencrypted_files once Smarter is fully integrated with HPZ.


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
        data = archive_files(dirname).getvalue()
        # a bug in celery config that convert None into 'None' instead of None
        if keyserver is None or keyserver == 'None':
            gpg = gnupg.GPG(gnupghome=os.path.abspath(homedir), gpgbinary=gpgbinary, verbose=True)
            gpg.encrypt(data, recipients, output=outputfile, always_trust=True)
        else:
            with tempfile.TemporaryDirectory() as gpghomedir:
                gpg = gnupg.GPG(gnupghome=gpghomedir, gpgbinary=gpgbinary)
                import_recipient_keys(gpg, recipients, keyserver)
                gpg.encrypt(data, recipients, output=outputfile, always_trust=True)
    except GPGPublicKeyException:
        # recoverable error because of public key server
        raise
    except Exception as e:
        # unrecoverable error
        raise GPGException(str(e))
    # if output file does not exist, it's because directory is not writable or recipients were not available
    if not os.path.exists(outputfile):
        raise GPGException("failed to generate: " + outputfile)


def archive_files(dirname):
    '''
    create archive file under given directory and return zip data
    '''
    bufferedIO = io.BytesIO()
    with zipfile.ZipFile(bufferedIO, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        files = [os.path.join(dirname, f) for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f))]
        for file in files:
            zf.write(file, arcname=os.path.basename(file))
    return bufferedIO


## TODO: Replace encrypted_archive_files with this method once Smarter is fully integrated with HPZ.
def archive_unencrypted_files(dir_to_archive, archive_file_name):
    '''
    Create unencrypted archive file from files in directory.
    '''

    with zipfile.ZipFile(archive_file_name, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        files = [os.path.join(dir_to_archive, f) for f in os.listdir(dir_to_archive) if os.path.isfile(os.path.join(dir_to_archive, f))]
        for file in files:
            zf.write(file, arcname=os.path.basename(file))
