'''
Created on Jun 18, 2013

@author: dawu
'''
import configparser
from zope import component
from services.tasks.pdf import generate
from urllib.parse import urljoin
from edauth.security.session_backend import ISessionBackend, SessionBackend
from edauth.security.batch_user_session import create_pdf_user_session


class PDFGenerator():
    '''
    Batch pdf pre-generation trigger.
    '''

    def __init__(self, configFile, tenant):
        '''
        Constructor with config file path as parameter.

        :param string configFile: path to configuration file
        '''
        self.__init_setting(configFile)
        self.__init_cookie(tenant)

    def __init_setting(self, configFile):
        '''
        Loads __settings from configuration file.
        '''
        settings = self.__load_setting(configFile)
        self.__settings = settings
        self.__base_url = settings['pdf.base.url']
        self.__queue_name = settings['pdf.batch.job.queue']

    def __load_setting(self, configFile):
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

    def __init_cookie(self, tenant):
        '''
        Creates cookie for generating pdf.
        '''
        # initiate session backend
        component.provideUtility(SessionBackend(self.__settings), ISessionBackend)
        # get current session cookie and request for pdf
        roles = ['SUPER_USER']
        (self.__cookie_name, self.__cookie_value) = create_pdf_user_session(self.__settings, roles, tenant)

    def send_pdf_request(self, student_guid, file_name, report='indivStudentReport.html'):
        '''
        Sends a student UUID and file path information to message queue.

        :param string student_guid: student guid
        :param string report: report name
        :param string file_name: the absolute path of output pdf file
        '''
        # build url for generating pdf
        pdf_url = urljoin(self.__base_url, report) + "?studentGuid=%s" % student_guid
        # send asynchronous request
        generate.apply_async((self.__cookie_value, pdf_url, file_name), queue=self.__queue_name)
