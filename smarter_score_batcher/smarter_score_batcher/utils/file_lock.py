'''
Created on Aug 18, 2014

@author: dip
'''
import os
import fcntl


class FileLock():
    '''
    File Lock class for locking a particular file
    '''
    def __init__(self, file_name):
        self.file_name = file_name
        self.created_file = False

    def __enter__(self):
        '''
        "with" will lock the file
        '''
        self.lock()
        return self

    def __exit__(self, type, value, tb):
        self.unlock()

    def lock(self):
        if not os.path.exists(self.file_name):
            # if file doesn't exist, create it
            self.created_file = True
            open(self.file_name, 'a').close()
        self.fd = open(self.file_name, 'r+')
        fcntl.flock(self.fd, fcntl.LOCK_EX)

    def unlock(self):
        fcntl.flock(self.fd, fcntl.LOCK_UN)
        self.fd.close()
