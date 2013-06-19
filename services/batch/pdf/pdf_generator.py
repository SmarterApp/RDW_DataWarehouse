'''
Created on Jun 18, 2013

@author: dawu
'''
import configparser
from zope import component
from edauth.security.session_backend import ISessionBackend, SessionBackend
from edauth.security import batch_user_session
from batch.pdf import util
import services
import sys
from services.tasks.pdf import generate
from batch.pdf.constants import Constants

# TODO:
report = 'indivStudentReport.html'

class PDFGenerator():
    '''
    classdocs
    '''

    def __init__(self, configFile):
        '''
        Constructor
        '''
        self.init_setting(configFile)
        self.init_cookie()
    
    def init_setting(self, configFile):
        settings = self.load_setting(configFile)
        self.settings = settings
        self.base_url = settings['pdf.base.url']
        # get isr file path name
        self.pdf_base_dir = settings.get('pdf.report_base_dir', "/tmp")

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

    def init_cookie(self):
        settings = self.settings
        # initiate session backend
        component.provideUtility(SessionBackend(settings), ISessionBackend)
        # TODO: get current session cookie and request for pdf
        (self.cookie_name, self.cookie_value) = self.get_cookie(settings)
        
    def send_pdf_request(self, student_guid, report, file_name):
        '''
        Sends individual student UUID to generate PDFs.
        '''
        if student_guid is None or file_name is None:
            raise ValueError('Required parameter is missing')
        # build url for generating pdf
        pdf_url = util.build_url(self.base_url, report, student_guid)
        # send request
        generate.delay(self.cookie_value, pdf_url, file_name, cookie_name=self.cookie_name, timeout=services.celeryconfig.TIMEOUT)

    def get_cookie(self, settings):
        roles = ['SUPER_USER']
        return batch_user_session.create_pdf_user_session(settings, roles)
    
    def query_student_info(self): 
        '''
        Queries students information from database
        '''
        # TODO: dummy data
        return [{Constants.STUDENT_GUID : '3efe8485-9c16-4381-ab78-692353104cce',
                 Constants.STATE_CODE : 'NY', Constants.ASMT_PERIOD_YEAR: '2012',
                 Constants.SCHOOL_GUID: '228', Constants.DISTRICT_GUID: '228',
                 Constants.ASMT_GRADE : '7'}]
        
    def build_params(self, student):
        '''
        '''
        student_guid = student[Constants.STUDENT_GUID]
        state_code = student[Constants.STATE_CODE]
        asmt_period_year = str(student[Constants.ASMT_PERIOD_YEAR])
        district_guid = student[Constants.DISTRICT_GUID]
        school_guid = student[Constants.SCHOOL_GUID]
        asmt_grade = student[Constants.ASMT_GRADE]
        # generate file name
        file_name = util.build_file_path(self.pdf_base_dir, state_code, asmt_period_year, district_guid, school_guid, asmt_grade, student_guid)
        return (student_guid, file_name)

    def start(self):
        students = self.query_student_info()
        for student in students:
            (student_guid, file_name) = self.build_params(student)
            self.send_pdf_request(student_guid, report, file_name)

    
# TODO: grabs new results from database/file that need reports generated


# TODO: includes trigger mechanism from UDL process

# test
if __name__ == '__main__':
    configFile = sys.argv[1]
    PDFGenerator(configFile).start()
