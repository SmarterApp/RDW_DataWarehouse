'''
Created on May 10, 2013

@author: dawu
'''
import os
import sys
import logging
import subprocess
from services.celeryconfig import celery
from services.celeryconfig import TIMEOUT

pdf_procs = ['wkhtmltopdf']
pdf_defaults = ['--enable-javascript', '--page-size', 'Letter', '--javascript-delay', '5000']


@celery.task
def generate_pdf(cookie, url, outputfile, options=pdf_defaults):
    '''
    Generates pdf from given url. Returns exist status code from shell command.
    We set up timeout in order to terminate pdf generating process, for wkhtmltopdf 0.10.0 doesn't exit
    properly upon successfully completion (see wkhtmltopdf ISSUE 141). TIMEOUT can be removed if that bug is fixed in future.
    '''
    try:
        return subprocess.call(pdf_procs + options + ['--cookie', 'edware', cookie, url, outputfile], timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        (SUCCESS, FAILURE) = (0, 1)
        # check output file, return 0 if file is created successfully
        isSucceed = os.path.exists(outputfile) and os.path.getsize(outputfile)
        return SUCCESS if isSucceed else FAILURE
    except:
        log = logging.getLogger(__name__)
        log.error("Generate PDF error: %s", sys.exc_info())
        return False
