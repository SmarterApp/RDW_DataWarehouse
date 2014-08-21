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
    def __init__(self, file_name, mode='r+'):
        self.file_name = file_name
        self.new_file = False
        self.mode = mode

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
            self.new_file = True
            open(self.file_name, 'a').close()
        self.fd = open(self.file_name, self.mode)
        fcntl.flock(self.fd, fcntl.LOCK_EX)

    def unlock(self):
        fcntl.flock(self.fd, fcntl.LOCK_UN)
        self.fd.close()

    @property
    def file_descriptor(self):
        return self.fd
