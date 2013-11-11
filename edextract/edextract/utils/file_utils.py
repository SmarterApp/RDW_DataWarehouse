'''
Created on Nov 9, 2013

@author: dip
'''
import os


def prepare_path(path):
    '''
    Create the directory if it doesn't exist

    :param string path: Path of the file to create directory for
    '''
    if os.path.exists(os.path.dirname(path)) is not True:
        os.makedirs(os.path.dirname(path), 0o700)
