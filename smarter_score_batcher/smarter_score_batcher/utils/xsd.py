'''
Created on Aug 7, 2014

@author: tosako
'''

xsd = None


class XSD():

    def __init__(self, filepath):
        with open(filepath) as f:
            self.__xsd = f.read()

    def get_xsd(self):
        return self.__xsd
