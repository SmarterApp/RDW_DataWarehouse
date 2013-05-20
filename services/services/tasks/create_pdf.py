'''
Created on May 10, 2013

@author: dawu
'''
import os
import sys
import logging
import subprocess
from services.celeryconfig import TIMEOUT
import platform
from services.celery import celery
from services.exceptions import PdfGenerationError

pdf_procs = ['wkhtmltopdf']
pdf_defaults = ['--enable-javascript', '--page-size', 'Letter', '--print-media-type', '-l', '--javascript-delay', '6000']

OK = 0
FAIL = 1


@celery.task(name='tasks.generate_pdf')
def generate_pdf(cookie, url, outputfile, options=pdf_defaults, timeout=TIMEOUT, cookie_name='edware'):
    '''
    Generates pdf from given url. Returns exist status code from shell command.
    We set up timeout in order to terminate pdf generating process, for wkhtmltopdf 0.10.0 doesn't exit
    properly upon successfully completion (see wkhtmltopdf ISSUE 141). TIMEOUT can be removed if that bug is fixed in future.
    '''
    try:
        # Only for windows environment, set shell to true
        shell = False
        if platform.system() == 'Windows':
            shell = True

        return subprocess.call(pdf_procs + options + ['--cookie', cookie_name, cookie, url, outputfile], timeout=timeout, shell=shell)
    except subprocess.TimeoutExpired:
        # check output file, return 0 if file is created successfully
        isSucceed = os.path.exists(outputfile) and os.path.getsize(outputfile)
        return OK if isSucceed else FAIL
    except:
        log = logging.getLogger(__name__)
        log.error("Generate PDF error: %s", sys.exc_info())
        return FAIL


@celery.task(name='tasks.get_pdf_file')
def get_pdf_file(cookie, url, outputfile, options=pdf_defaults, timeout=TIMEOUT, cookie_name='edware'):
    '''
    Returns byte stream from the path specified
    '''
    if not os.path.exists(outputfile):
        generate_task = generate_pdf(cookie, url, outputfile, options=pdf_defaults, timeout=timeout, cookie_name=cookie_name)
        if generate_task is FAIL:
            raise PdfGenerationError

    with open(outputfile, 'rb') as file:
        stream = file.read()
    return stream
