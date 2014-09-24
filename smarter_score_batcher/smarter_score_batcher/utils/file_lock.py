'''
Created on Aug 18, 2014

@author: dip
'''
import os
import fcntl
from smarter_score_batcher.error.exceptions import FileLockFileDoesNotExist


class FileLock():
    '''
    File Lock class for locking a particular file
    '''
    def __init__(self, file_name, mode='r+', no_block_lock=False, do_not_create_lock_file=False):
        self.__file_name = file_name
        self.__new_file = False
        self.__mode = mode
        self.__no_block_lock = no_block_lock
        self.__do_not_create_lock_file = do_not_create_lock_file
        self.lock()

    def __enter__(self):
        '''
        "with" will lock the file
        '''
        return self

    def __exit__(self, type, value, tb):
        self.unlock()

    def lock(self):
        if not os.path.exists(self.file_name):
            if self.__do_not_create_lock_file:
                raise FileLockFileDoesNotExist('lockfile: ' + self.file_name + ' does not exist')
            # if file doesn't exist, create it
            self.__new_file = True
            parent = os.path.dirname(self.file_name)
            if not os.path.exists(parent):
                os.makedirs(parent, exist_ok=True)
            open(self.__file_name, 'a').close()
        self.__fd = open(self.__file_name, self.__mode)
        lock_operation = fcntl.LOCK_EX
        if self.__no_block_lock:
            lock_operation |= fcntl.LOCK_NB
        fcntl.flock(self.__fd.fileno(), lock_operation)

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
