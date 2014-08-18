'''
Created on Aug 7, 2014

@author: tosako
'''

xsd = None


class XSD():
    '''
    XSD file data place holder
    '''
    def __init__(self, filepath):
        '''
        :param filepath: xsd file to read
        '''
        with open(filepath) as f:
            self.__xsd = f.read()

    def get_xsd(self):
        '''
        return xsd data
        :returns: xsd data
        '''
        return self.__xsd
