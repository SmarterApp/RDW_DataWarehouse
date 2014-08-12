'''
Created on Aug 12, 2014

@author: dip
'''
import os


class DummyObj:

    def __init__(self):
        pass

    def get_value(self):
        return 1


def read_data(filename):
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'resources', filename)), 'r') as f:
        data = f.read()
    return data
