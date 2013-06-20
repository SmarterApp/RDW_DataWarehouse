'''
Created on Jun 18, 2013

@author: dawu
'''
from urllib.parse import urljoin
from services.tasks.pdf import generate
from batch.base import BatchBase


class PDFGenerator(BatchBase):
    '''
    Batch pdf pre-generation trigger.
    '''

    def __init__(self, settings, tenant):
        '''
        Constructor with config file path as parameter.

        :param string configFile: path to configuration file
        '''
        super().__init__(settings, tenant)
        self.__base_url = settings.get('pdf.base.url')
        self.__queue_name = settings.get('pdf.batch.job.queue', 'batch_pdf_gen')

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
        kwargs = {'cookie_name': self.cookie_name}
        generate.apply_async((self.cookie_value, pdf_url, file_name), kwargs=kwargs, queue=self.__queue_name)  # @UndefinedVariable
