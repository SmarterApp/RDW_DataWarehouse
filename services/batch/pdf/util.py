'''
Created on Jun 18, 2013

@author: dawu
'''
import os
from urllib.parse import urljoin
from batch.pdf.constants import Constants


def build_url(base_url, report, student_guid):
    # Encode the query parameters and append it to url
    return urljoin(base_url, report) + "?studentGuid=%s" % student_guid


def build_file_path(pdf_report_base_dir='/', state_code=None, asmt_period_year=None, district_guid=None, school_guid=None, asmt_grade=None, student_guid=None, asmt_type=Constants.SUMMATIVE, grayScale=False):
    '''
    generate isr absolute file path name
    '''
    dirname = os.path.join(pdf_report_base_dir, state_code, asmt_period_year, district_guid, school_guid, asmt_grade, 'isr', asmt_type, student_guid)
    return dirname + (".g.pdf" if grayScale else ".pdf")
