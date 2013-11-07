'''
Created on Nov 1, 2013

@author: tosako
'''
import os
from zipfile import ZipFile


def archive_files(zip_filename, directory):
    '''
    zip up all files under given directory.
    archive name is flat directory and no recursive.
    no compression apply because all gpg files shoud be compressed already.
    '''
    with ZipFile(zip_filename, "w") as zipfile:
        files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        for file in files:
            zipfile.write(file, arcname=os.path.basename(file))
