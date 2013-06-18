'''
Created on Jun 18, 2013

@author: dawu
'''
import configparser
import urllib
from urllib.parse import urljoin
from zope import component
from edauth.security.session_backend import ISessionBackend, SessionBackend
from edauth.security import pdf_session
from smarter.reports.helpers.ISR_pdf_name_formatter import generate_isr_report_path_by_student_guid
from smarter.reports.helpers.constants import Constants


class PDFGenerator():
    '''
    classdocs
    '''

    def __init__(self, configFile):
        '''
        Constructor
        '''
        settings = self.load_setting(configFile)
        self.settings = settings
        self.url = settings['pdf.base.url']
        # get isr file path name
        self.pdf_base_dir = settings.get('pdf.report_base_dir', "/tmp")
        self.initialize_cookie()
    
    # TODO: move this function to PDFGenerator
    def load_setting(self, configFile):
        '''
        Loads setting from ini file
        '''
        config = configparser.ConfigParser()
        config.read(configFile)
        section = 'app:main'
        settings = {}
        for option in config.options(section):
            settings[option] = config.get(section, option)
        return settings

    def initialize_cookie(self):
        settings = self.settings
        # initiate session backend
        component.provideUtility(SessionBackend(settings), ISessionBackend)
        # get current session cookie and request for pdf
        (self.cookie_name, self.cookie_value) = self.get_session_cookie(settings)
        
    def send_pdf_request(self, params, report, is_grayscale=False):
        '''
        Sends individual student UUID to generate PDFs.
        '''
        student_guid = params.get('studentGuid')
        if student_guid is None:
            raise ValueError('Required parameter is missing')
        # Encode the query parameters and append it to url
        encoded_params = urllib.parse.urlencode(params)
        pdf_url = urljoin(self.url, report) + "?%s" % encoded_params
        # generate file name
        file_name = generate_isr_report_path_by_student_guid(pdf_report_base_dir=self.pdf_base_dir, student_guid=student_guid, asmt_type=Constants.SUMMATIVE, grayScale=is_grayscale)
        generate.delay(cookie_value, pdf_url, file_name, cookie_name=cookie_name, timeout=services.celeryconfig.TIMEOUT, grayScale=is_grayscale)  # @UndefinedVariable

    def get_session_cookie(self, settings):
        roles = ['SUPER_USER']
        return pdf_session.create_pdf_user_session(settings, roles)
    
    def query_student_info(self): 
        '''
        Queries students information from database
        '''
        pass
    
    def build_params(self, student):
        '''
        '''
        pass

    def start(self):
        students = self.query_student_info()
        for student in students:
            params = self.build_params(student)
            self.send_pdf_request(params)
