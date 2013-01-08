'''
Created on Jan 8, 2013

@author: V5102883
'''

import configparser


class EdwareConfig(object):
    '''
    classdocs
    '''
    _config = configparser.SafeConfigParser()
    _config.read("edwareconfigs.ini")

    def __init__(self):
        '''
        Constructor
        '''
    @classmethod
    def getConfigValue(self, section, key):
        return self._config.get(section, key)

if __name__ == "__main__":
    print(EdwareConfig.getConfigValue("edware:db", "host"))
