'''
Created on Mar 27, 2013

@author: aoren
'''
from zope.interface.declarations import implementer
from zope import interface


class IEngine(interface.Interface):
    def get_engine(self):
        pass


@implementer(IEngine)
class Engine:
    def __init__(self, engine):
        self.__engine = engine

    def get_engine(self):
        return self.__engine
