'''
Celery Tasks for pdf generation

Created on May 10, 2013

@author: dawu
'''
import os
import sys
import logging
import subprocess
from services.celery import celery
from services.exceptions import PdfGenerationError
from edcore.exceptions import NotForWindowsException, RemoteCopyError
from edcore.utils.utils import archive_files
import copy
from services.celery import TIMEOUT
import services
from celery.exceptions import MaxRetriesExceededError
import uuid
from subprocess import Popen
import tempfile
from hpz_client.frs.http_file_upload import http_file_upload

mswindows = (sys.platform == "win32")
pdf_procs = ['wkhtmltopdf']
pdfunite_procs = ['pdfunite']
pdf_defaults = ['--enable-javascript', '--page-size', 'Letter', '--print-media-type', '-l', '--javascript-delay', '6000', '--footer-center', 'Page [page] of [toPage]', '--footer-font-size', '9']

OK = 0
FAIL = 1

log = logging.getLogger('smarter')


@celery.task(name='tasks.pdf.generate', max_retries=services.celery.MAX_RETRIES, default_retry_delay=services.celery.RETRY_DELAY)
def generate(cookie, url, outputfile, options=pdf_defaults, timeout=TIMEOUT, cookie_name='edware', grayscale=False):
    '''
    Generates pdf from given url. Returns exist status code from shell command.
    We set up timeout in order to terminate pdf generating process, for wkhtmltopdf 0.10.0 doesn't exit
    properly upon successfully completion (see wkhtmltopdf ISSUE 141). TIMEOUT can be removed if that bug is fixed in future.

    This task can be retried.  It throws MaxRetriesExceededError exception when retries have been exhausted.
    By default, it will retry once, immediately without any time delay.

    :param string cookie: the cookie to pass into http request
    :param string url:  the url to request for
    :param string outputfile:  the path of the file to write pdf to
    :param options:  options passed into wkhtmltopdf
    :param timeout:  subprocess call timeout value
    :param cookie_name:  the name of the cookie being passed into http request
    :param grayscale: whether to generate pdf in grayscale

    NB! celery.task misbehaves so this doc will not go to apidocs. Please modify manually in rst
    '''
    # MS Windows is not supported
    if mswindows:
        raise NotForWindowsException('PDF generator cannot be served for Windows users')
    force_regenerate = False
    try:
        prepare_path(outputfile)
        wkhtmltopdf_option = copy.deepcopy(options)
        if grayscale:
            wkhtmltopdf_option += ['-g']
        wkhtmltopdf_option += ['--cookie', cookie_name, cookie, url, outputfile]
        subprocess.call(pdf_procs + wkhtmltopdf_option, timeout=timeout)
    except subprocess.TimeoutExpired:
        # Note that Timeout exception is valid due to wkhtmltopdf issue 141
        log.error('wkhmltopdf subprocess call timed out')
    except:
        log.error('Generate PDF error: %s', sys.exc_info())
        # Some exception happened, force to regenerate
        force_regenerate = True
    finally:
        # Validate pdf file was generated and greater than a certain size
        if not is_valid(outputfile) or force_regenerate:
            # If the retries throws an exception, return fail
            log.error("Pdf file validation failed.  Removing file %s. Will attempt to regenerate pdf", outputfile)
            delete(outputfile)

            kwargs = {'options': options, 'timeout': timeout, 'cookie_name': cookie_name, 'grayscale': grayscale}
            return generate.retry(args=[cookie, url, outputfile], kwargs=kwargs, exc=PdfGenerationError())
        else:
            return OK


@celery.task(name='tasks.pdf.get')
def get(cookie, url, outputfile, options=pdf_defaults, timeout=TIMEOUT, cookie_name='edware', grayscale=False, always_generate=False):
    '''
    Reads pdf file if it exists, else it'll request to generate pdf.  Returns byte stream from generated pdf file
    This is meant to be a synchronous call.  It waits for generate task to return.

    :param cookie: the cookie to pass into http request
    :param url:  the url to request for
    :param outputfile:  the path of the file to write pdf to
    :param options:  options passed into wkhtmltopdf
    :param timeout:  subprocess call timeout value
    :param cookie_name:  the name of the cookie being passed into http request
    :param grayscale: whether to generate pdf in grayscale
    :param always_generate: whether to always generate pdf instead of checking file system first

    NB! celery.task misbehaves so this doc will not go to apidocs. Please modify manually in rst
    '''
    prepare(cookie, url, outputfile, options=options, timeout=timeout, cookie_name=cookie_name, grayscale=grayscale, always_generate=always_generate)

    with open(outputfile, 'rb') as file:
        stream = file.read()

    return stream


@celery.task(name='tasks.pdf.prepare', ignore_result=True)
def prepare(cookie, url, outputfile, options=pdf_defaults, timeout=TIMEOUT, cookie_name='edware', grayscale=False, always_generate=False):
    '''
    Reads pdf file if it exists, else it'll request to generate pdf.  Returns byte stream from generated pdf file
    This is meant to be a synchronous call.  It waits for generate task to return.

    :param cookie: the cookie to pass into http request
    :param url:  the url to request for
    :param outputfile:  the path of the file to write pdf to
    :param options:  options passed into wkhtmltopdf
    :param timeout:  subprocess call timeout value
    :param cookie_name:  the name of the cookie being passed into http request
    :param grayscale: whether to generate pdf in grayscale
    :param always_generate: whether to always generate pdf instead of checking file system first

    NB! celery.task misbehaves so this doc will not go to apidocs. Please modify manually in rst
    '''
    if always_generate or not os.path.exists(outputfile):
        # always delete it first in case of regeneration error
        delete(outputfile)
        try:
            generate(cookie, url, outputfile, options=pdf_defaults, timeout=timeout, cookie_name=cookie_name, grayscale=grayscale)
        except MaxRetriesExceededError:
            log.error("Max retries exceeded in PDF Generation")
            raise PdfGenerationError()


def prepare_path(path):
    '''
    Create the directory if it doesn't exist

    :param string path: Path of the file to create directory for
    '''
    if os.path.exists(os.path.dirname(path)) is not True:
        os.makedirs(os.path.dirname(path), 0o700)


def is_valid(path):
    '''
    Validate file specified in path that the file exists and is larger than a configurable expected size

    :param string path: Path of the pdf file to validate
    :return:  True if file is valid, else False
    :rtype: Boolean
    '''
    return os.path.exists(path) and (os.path.getsize(path) > services.celery.MINIMUM_FILE_SIZE)


def delete(path):
    '''
    Delete file specified in path

    :param string path: Path of the file to delete from file system
    '''
    if os.path.exists(path):
        os.remove(path)


@celery.task(name='task.pdf.prepare_path')
def prepare_path(paths):
    '''
    Given a list of paths of directories, creates it if it doesn't exist
    '''

    try:
        for path in paths:
            if os.path.exists(path) is not True:
                os.makedirs(path, 0o700)
    except FileNotFoundError as e:
        # unrecoverable error, do not try to retry celery task.  it's just wasting time.
        log.error(e)
        raise PdfGenerationError(str(e))



@celery.task(name='tasks.pdf.merge')
def pdf_merge(pdf_files, out_name, pdf_base_dir, registration_id, timeout=TIMEOUT):
    if os.path.isfile(out_name):
        log.error(out_name + " is already exist")
        raise PdfGenerationError()
    if not os.path.isdir(os.path.dirname(out_name)):
        os.makedirs(os.path.dirname(out_name))
    for pdf_file in pdf_files:
        if not os.path.isfile(pdf_file):
            raise PdfGenerationError('file does not exist: ' + pdf_file)
    try:
        # UNIX can handle upto 1024 file descriptors in default.  To be safe we process 1000 files at once.
        if len(pdf_files) > 1000:
            with tempfile.TemporaryDirectory(dir=os.path.join(pdf_base_dir, '.tmp')) as temp_dir:
                files = _parallel_pdf_unite(pdf_files, temp_dir, timeout=timeout)
                subprocess.call(pdfunite_procs + files + [out_name], timeout=timeout)
        else:
            subprocess.call(pdfunite_procs + pdf_files + [out_name], timeout=timeout)
    except subprocess.TimeoutExpired:
        log.error('pdfunite subprocess call timed out')


@celery.task(name="tasks.pdf.archive")
def archive(archive_file_name, directory):
    '''
    given a directory, archive everything in this directory to a file name specified
    '''

    try:
        archive_files(directory, archive_file_name)
    except Exception as e:
        # unrecoverable exception
        raise PdfGenerationError('Unable to archive file(s): ' + directory + ', ' + archive_file_name)


@celery.task(name="tasks.pdf.remote_copy", max_retries=5)
def remote_copy(src_file_name, registration_id):
    '''
    Remotely copies a source file to a remote machine
    '''

    try:
        http_file_upload(src_file_name, registration_id)
    except RemoteCopyError as e:
        log.error("Exception happened in remote copy. " + str(e))
        try:
            # this looks funny to you, but this is just a work around solution for celery bug
            # since exc option is not really working for retry.
            raise PdfGenerationError(str(e))
        except PdfGenerationError as exc:
            # this could be caused by network hiccup
            raise remote_copy.retry(args=[src_file_name, registration_id], exc=exc)

    except Exception as e:
        raise PdfGenerationError(str(e))


def _parallel_pdf_unite(pdf_files, pdf_tmp_dir, file_limit=1000, timeout=TIMEOUT):
    procs = []
    files = []
    offset = -1
    while offset is not int(len(pdf_files) / file_limit):
        offset += 1
        end = (offset + 1) * file_limit if offset is not int(len(pdf_files) / file_limit) else len(pdf_files)
        partial_file_list = pdf_files[offset * file_limit:end]
        if len(partial_file_list) is 1:
            files.append(partial_file_list[0])
        else:
            partial_outputfile = os.path.join(pdf_tmp_dir, str(uuid.uuid4()))
            partial_file_list.append(partial_outputfile)
            files.append(partial_outputfile)
            proc = Popen(pdfunite_procs + partial_file_list)
            procs.append(proc)
    for proc in procs:
        proc.wait(timeout=timeout) 
    return files
