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
    def __init__(self, file_name, mode='r+', lock_operation=fcntl.LOCK_EX):
        self.__file_name = file_name
        self.__new_file = False
        self.__mode = mode
        self.__lock_operation = lock_operation

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
            self.__new_file = True
            open(self.__file_name, 'a').close()
        self.__fd = open(self.__file_name, self.__mode)
        fcntl.flock(self.__fd.fileno(), self.__lock_operation)

    def unlock(self):
        fcntl.flock(self.__fd.fileno(), fcntl.LOCK_UN)
        self.__fd.close()

    @property
    def file_object(self):
        return self.__fd

    @property
    def new_file(self):
        return self.__new_file

    @property
    def file_name(self):
        return self.__file_name
