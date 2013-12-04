'''
Created on Dec 2, 2013

@author: tosako
'''
import os
import io
import zipfile
import gnupg


def encrypted_archive_files(dirname, recipients, outputfile, homedir=None, gpgbinary='gpg'):
    '''
    create encrpyted archive file.
    '''
    data = archive_files(dirname).getvalue()
    gpg = gnupg.GPG(gnupghome=homedir, gpgbinary=gpgbinary)
    gpg.encrypt(data, recipients, output=outputfile)


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
