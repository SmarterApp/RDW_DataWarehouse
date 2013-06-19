'''
Created on Jun 19, 2013

@author: dip
'''
from zope import component
from edauth.security.session_backend import ISessionBackend, SessionBackend
import configparser


def setup_sessions(settings):
    # initiate session backend for session creation
    component.provideUtility(SessionBackend(settings), ISessionBackend)


def load_setting(self, configFile):
    '''
    Returns __settings from app:main section in config file.
    '''
    config = configparser.ConfigParser()
    config.read(configFile)
    section = 'app:main'
    settings = {}
    for option in config.options(section):
        settings[option] = config.get(section, option)
    return settings
