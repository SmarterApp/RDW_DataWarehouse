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
Created on Nov 9, 2013

@author: dip
'''
import os


def prepare_path(path):
    '''
    Create the directory if it doesn't exist

    :param string path: Path of the directory to create directory for
    '''
    if os.path.exists(path) is not True:
        os.makedirs(path, 0o700)


class File():
    def __init__(self, path, size):
        self.__path = path
        self.__size = size

    @property
    def name(self):
        return self.__path

    @property
    def size(self):
        return self.__size
