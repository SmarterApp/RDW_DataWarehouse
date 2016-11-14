'''
Created on Jan 3, 2013

@author: swimberly
'''


class NameInfo(object):
    '''
    NameInfo object
    '''

    def __init__(self, name, frequency, cum_freq, rank):
        '''
        Constructor
        '''
        self.cum_freq = cum_freq
        self.frequency = frequency
        self.rank = rank
        self.name = name

    def __str__(self):
        '''
        String method
        '''
        return ("NameInfo:[rank: %s, name: %s, frequency: %s, cum_freq: %s]"
                % (self.rank, self.name, self.frequency, self.cum_freq))
