'''
Created on May 3, 2013

@author: dip
'''
import configparser
import os 

class CeleryConfig:
    def __init__(self):
        # load configuration file
        self.config = configparser.RawConfigParser()
        resources_dir = os.path.dirname(os.path.dirname(__file__))
        self.config.read(os.path.join(resources_dir , 'celeryconfig.ini'))
        self.read("Celery Config")
        
    def read(self, section):
        self.dict = {}
        options = self.config.options(section)
        for option in options:
            try:
                self.dict[option.upper()] = self.config.get(section, option)
            except:
                print("exception on %s!" % option)
                self.dict[option] = None
        
    def __getattr__(self, name):
        if name in self.dict:
            return self.dict[name]
        else:
            raise AttributeError()
    