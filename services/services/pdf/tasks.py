'''
Created on May 10, 2013

@author: dawu
'''
import os
import sys
import logging
import subprocess
import platform
from services.celery import celery
from services.exceptions import PdfGenerationError
import copy
from services.celeryconfig import TIMEOUT
import services

pdf_procs = ['wkhtmltopdf']
pdf_defaults = ['--enable-javascript', '--page-size', 'Letter', '--print-media-type', '-l', '--javascript-delay', '6000', '--footer-center', 'Page [page] of [toPage]', '--footer-font-size', '9']

OK = 0
FAIL = 1

log = logging.getLogger('smarter')


@celery.task(name='tasks.pdf.generate')
def generate(cookie, url, outputfile, options=pdf_defaults, timeout=TIMEOUT, cookie_name='edware', grayScale=False, retries=0):
    '''
    Generates pdf from given url. Returns exist status code from shell command.
    We set up timeout in order to terminate pdf generating process, for wkhtmltopdf 0.10.0 doesn't exit
    properly upon successfully completion (see wkhtmltopdf ISSUE 141). TIMEOUT can be removed if that bug is fixed in future.
    '''
    force_regenerate = False
    try:
        # Only for windows environment, set shell to true
        shell = False
        if platform.system() == 'Windows':
            shell = True
        prepare_file_path(outputfile)
        wkhtmltopdf_option = copy.deepcopy(options)
        if grayScale:
            wkhtmltopdf_option += ['-g']
        wkhtmltopdf_option += ['--cookie', cookie_name, cookie, url, outputfile]
        subprocess.call(pdf_procs + wkhtmltopdf_option, timeout=timeout, shell=shell)
    except subprocess.TimeoutExpired:
        log.error('Pdf subprocess timed out')
    except:
        log.error("Generate PDF error: %s", sys.exc_info())
        # Some exception happened, force a regenerate
        force_regenerate = True

    # Validate pdf file was generated and greater than a certain size
    if not validate_file(outputfile) or force_regenerate:
        if retries < services.celeryconfig.RETRIES:
            log.error("PDF %s failed validation, Going to retry #%s", outputfile, str(retries + 1))
            return generate(cookie, url, outputfile, options=options, timeout=timeout, cookie_name=cookie_name, grayScale=grayScale, retries=retries + 1)
        else:
            log.error("Maximum retries of pdf generation reached. Removing pdf file %s as validation of file failed", outputfile)
            delete_file(outputfile)
            return FAIL
    else:
        return OK


@celery.task(name='tasks.pdf.get')
def get(cookie, url, outputfile, options=pdf_defaults, timeout=TIMEOUT, cookie_name='edware', grayScale=False, always_generate=False):
    '''
    Reads pdf file if it exists, else it'll request to generate pdf.  Returns byte stream from generated pdf file
    '''
    if always_generate or not os.path.exists(outputfile):
        generate_task = generate(cookie, url, outputfile, options=pdf_defaults, timeout=timeout, cookie_name=cookie_name, grayScale=grayScale)
        if generate_task is FAIL:
            raise PdfGenerationError()

    with open(outputfile, 'rb') as file:
        stream = file.read()
    return stream


def prepare_file_path(path):
    '''
    Create the directory if it doesn't exist
    '''
    if os.path.exists(os.path.dirname(path)) is not True:
        os.makedirs(os.path.dirname(path), 0o700)


def validate_file(path):
    '''
    Validate file specified in path that the file exists and is larger than a configurable expected size
    Returns True if file is valid, else False
    '''
    return os.path.exists(path) and (os.path.getsize(path) > services.celeryconfig.MINIMUM_FILE_SIZE)


def delete_file(path):
    '''
    Delete file specified in path
    '''
    if os.path.exists(path):
        os.remove(path)
