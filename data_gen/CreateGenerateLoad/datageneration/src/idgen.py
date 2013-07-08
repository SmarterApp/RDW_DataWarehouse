'''
Created on Jan 22, 2013

@author: swimberly
'''


class IdGen(object):
    '''
    Singleton for generating incremental ids
    ids will start at 0 unless set_start() is called.
    '''

    next_id = 20
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(IdGen, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def get_id(self):
        nid = self.next_id
        self.next_id += 1
        return nid

    def set_start(self, start):
        self.next_id = start
