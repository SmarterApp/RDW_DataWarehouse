'''
Created on Jun 18, 2013

@author: dawu
'''
import configparser
from zope import component
from edauth.security.session_backend import ISessionBackend, SessionBackend
from edauth.security.batch_user_session import create_pdf_user_session
from batch.pdf import util
import services
import sys
from services.tasks.pdf import generate
from batch.pdf.constants import Constants


class PDFGenerator():
    '''
    Batch pdf pre-generation trigger.
    '''

    def __init__(self, configFile):
        '''
        Constructor with config file path as parameter.
        '''
        self.__init_setting(configFile)
        self.__init_cookie()

    def __init_setting(self, configFile):
        '''
        Loads settings from configuration file.
        '''
        settings = self.__load_setting(configFile)
        self.settings = settings
        self.base_url = settings['pdf.base.url']
        # get isr file path name
        self.pdf_base_dir = settings.get('pdf.report_base_dir', "/tmp")

    def __load_setting(self, configFile):
        '''
        Returns settings from app:main section in config file.
        '''
        config = configparser.ConfigParser()
        config.read(configFile)
        section = 'app:main'
        settings = {}
        for option in config.options(section):
            settings[option] = config.get(section, option)
        return settings

    def __init_cookie(self):
        '''
        Creates cookie for generating pdf.
        '''
        # initiate session backend
        component.provideUtility(SessionBackend(self.settings), ISessionBackend)
        # get current session cookie and request for pdf
        roles = ['SUPER_USER']
        (self.cookie_name, self.cookie_value) = create_pdf_user_session(self.settings, roles)

    def __send_pdf_request(self, student_guid, report, file_name):
        '''
        Sends a student UUID and file path information to message queue.
        '''
        # build url for generating pdf
        pdf_url = util.build_url(self.base_url, report, student_guid)
        # send request
        generate.delay(self.cookie_value, pdf_url, file_name, cookie_name=self.cookie_name, timeout=services.celeryconfig.TIMEOUT)

    def __query_student_info(self):
        '''
        Queries students information from UDL process
        '''
        # TODO: dummy data, will include trigger mechanism from UDL process
        return [{Constants.STUDENT_GUID: '3efe8485-9c16-4381-ab78-692353104cce',
                 Constants.STATE_CODE: 'NY', Constants.ASMT_PERIOD_YEAR: '2012',
                 Constants.SCHOOL_GUID: '228', Constants.DISTRICT_GUID: '228',
                 Constants.ASMT_GRADE: '7'}]

    def __build_params(self, student):
        '''
        Returns student_guid and file_name to generate pdf. File name is created based on student's information.
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
        '''
        Starts batch pdf generation process.
        '''
        students = self.__query_student_info()
        for student in students:
            (student_guid, file_name) = self.__build_params(student)
            # send request to generate report
            self.__send_pdf_request(student_guid, Constants.INDIV_STUDENT_REPORT, file_name)


# main function
if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print('Usage: python %s <path-to-config-file>' % __file__)
        exit()
    configFile = sys.argv[1]
    PDFGenerator(configFile).start()
