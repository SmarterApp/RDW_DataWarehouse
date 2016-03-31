# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

'''
Created on Jun 18, 2013

@author: dawu
'''
from urllib.parse import urljoin
from services.tasks.pdf import generate
from batch.base import BatchBase
import urllib.parse
import services


class PDFGenerator(BatchBase):
    '''
    Batch pdf pre-generation trigger.
    '''

    def __init__(self, settings, tenant=None):
        '''
        Constructor with config file path as parameter.

        :param string configFile: path to configuration file
        '''
        super().__init__(settings, tenant)
        self.__base_url = settings.get('pdf.base.url')
        self.__queue_name = settings.get('pdf.batch.job.queue')

    def send_pdf_request(self, student_id, state_code, asmt_period_year, asmt_type, date_taken, file_name, report='indivStudentReport.html'):
        '''
        Sends a student UUID and file path information to message queue.

        :param string student_id: student guid
        :param string report: report name
        :param string file_name: the absolute path of output pdf file
        '''
        # build url for generating pdf
        pdf_url = self.build_url(student_id, state_code, asmt_period_year, asmt_type, date_taken, report)
        # send asynchronous request
        kwargs = {'cookie_name': self.cookie_name, 'timeout': services.celery.TIMEOUT, 'grayscale': True}
        return generate.apply_async((self.cookie_value, pdf_url, file_name), kwargs=kwargs, queue=self.__queue_name)  # @UndefinedVariable

    def build_url(self, student_id, state_code, asmt_period_year, asmt_type, date_taken, report):
        '''
        Build and return the full url for ISR report

        :param string student_id:  student id of the student
        :param string report:  the name of the report
        '''
        # Encode the query parameters and append it to url
        encoded_params = urllib.parse.urlencode({'studentId': student_id, 'pdf': 'true', 'stateCode': state_code, 'dateTaken': date_taken, 'asmtType': asmt_type, 'asmtYear': asmt_period_year})
        return urljoin(self.__base_url, report) + "?%s" % encoded_params
