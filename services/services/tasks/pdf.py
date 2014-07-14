'''
Celery Tasks for pdf generation

Created on May 10, 2013

@author: dawu
'''
import os
import sys
import logging
import subprocess
import urllib.parse
from services.celery import celery, PDFUNITE_TIMEOUT
from services.exceptions import PdfGenerationError, PDFUniteError
from edcore.exceptions import NotForWindowsException, RemoteCopyError
from edcore.utils.utils import archive_files
import copy
from services.celery import TIMEOUT
import services
from celery.exceptions import MaxRetriesExceededError
from subprocess import Popen
import shutil
from hpz_client.frs.http_file_upload import http_file_upload
from services.constants import ServicesConstants
import uuid

mswindows = (sys.platform == "win32")
pdf_procs = ['wkhtmltopdf']
pdfunite_procs = ['pdfunite']
pdf_defaults = ['--enable-javascript', '--page-size', 'Letter', '--print-media-type', '-l', '--javascript-delay', '6000', '--footer-center', 'Page [page] of [toPage]', '--footer-font-size', '9']
cover_sheet_pdf_defaults = ['--enable-javascript', '--page-size', 'Letter', '--print-media-type', '-l', '--javascript-delay', '1000']

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

            try:
                # this looks funny to you, but this is just a work around solution for celery bug
                # since exc option is not really working for retry.
                # the specific exception raised is irrelevant, it just needs to be unique
                raise PdfGenerationError()
            except PdfGenerationError as exc:
                # this could be caused by network hiccup
                log.info('[generate] retry generate   : ' + outputfile)
                kwargs = {'options': options, 'timeout': timeout, 'cookie_name': cookie_name, 'grayscale': grayscale}
                raise generate.retry(args=(cookie, url, outputfile), kwargs=kwargs, exc=exc)

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


@celery.task(name='tasks.pdf.prepare')
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
    # for UT purpose
    return_value = False
    if always_generate or not os.path.exists(outputfile):
        # always delete it first in case of regeneration error
        delete(outputfile)
        try:
            generate(cookie, url, outputfile, options=pdf_defaults, timeout=timeout, cookie_name=cookie_name, grayscale=grayscale)
            return_value = True
        except MaxRetriesExceededError:
            log.error("Max retries exceeded in PDF Generation")
            raise PdfGenerationError()
    return return_value


def prepare_path(path):
    '''
    Create the directory if it doesn't exist

    :param string path: Path of the file to create directory for
    '''
    if os.path.exists(os.path.dirname(path)) is not True:
        os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)


def is_valid(path):
    '''
    Validate file specified in path that the file exists and is larger than a configurable expected size

    :param string path: Path of the pdf file to validate
    :return:  True if file is valid, else False
    :rtype: Boolean
    '''
    if ServicesConstants.COVER_SHEET_NAME_PREFIX in path:
        return os.path.exists(path) and (os.path.getsize(path) > ServicesConstants.MINIMUM_COVER_FILE_SIZE)
    return os.path.exists(path) and (os.path.getsize(path) > services.celery.MINIMUM_FILE_SIZE)


def delete(path):
    '''
    Delete file specified in path

    :param string path: Path of the file to delete from file system
    '''
    if os.path.exists(path):
        os.remove(path)


@celery.task(name='tasks.pdf.coversheet')
def bulk_pdf_cover_sheet(cookie, out_name, merged_pdf_filename, base_url, base_params, cookie_name='edware', grayscale=False,
                         timeout=TIMEOUT):
    url = _build_url(base_url, base_params, merged_pdf_filename)

    # Generate the cover sheet
    generate(cookie, url, out_name, cookie_name=cookie_name, grayscale=grayscale, options=cover_sheet_pdf_defaults,
             timeout=timeout)


def _build_url(base_url, base_params, merged_pdf_filename):
    # Get the page count from the merged PDF
    base_params[ServicesConstants.PAGECOUNT] = _count_pdf_pages(merged_pdf_filename)

    # Build the URL for the page to generate
    encoded_params = urllib.parse.urlencode(base_params)
    url = base_url + "?%s" % encoded_params
    return url


@celery.task(name='tasks.pdf.merge', max_retries=ServicesConstants.PDF_MERGE_MAX_RETRY, default_retry_delay=ServicesConstants.PDF_MERGE_RETRY_DELAY)
def pdf_merge(pdf_files, out_name, pdf_base_dir, max_pdfunite_files=ServicesConstants.MAX_PDFUNITE_FILE):
    # Prepare output file
    if os.path.exists(out_name):
        log.error(out_name + " is already exist")
        raise PdfGenerationError()
    prepare_path(out_name)

    # Verify that all PDFs to merge exist
    for pdf_file in pdf_files:
        if not os.path.isfile(pdf_file):
            raise PdfGenerationError('file does not exist: ' + pdf_file)
    try:
        # UNIX can handle upto 1024 file descriptors in default.  To be safe we process 50 files at once.
        if len(pdf_files) > max_pdfunite_files:
            partial_dir = os.path.join(os.sep, '.tmp', 'partial')
            if partial_dir not in pdf_base_dir:
                gid = uuid.uuid4()
                pdf_base_dir = os.path.join(pdf_base_dir, '.tmp', 'partial', str(gid))
                if os.path.exists(pdf_base_dir) is not True:
                    os.makedirs(pdf_base_dir, mode=0o700, exist_ok=True)
            files = _partial_pdfunite(pdf_files, pdf_base_dir, timeout=PDFUNITE_TIMEOUT, file_limit=max_pdfunite_files)
            _pdfunite_subprocess(files, out_name, PDFUNITE_TIMEOUT)
            shutil.rmtree(pdf_base_dir, ignore_errors=True)
        elif len(pdf_files) is 1:
            # pdfunite is not callable if there is only one pdf to merge
            shutil.copyfile(pdf_files[0], out_name)
        else:
            _pdfunite_subprocess(pdf_files, out_name, PDFUNITE_TIMEOUT)
    except PDFUniteError as exc:
        try:
            # this looks funny to you, but this is just a work around solution for celery bug
            # since exc option is not really working for retry.
            # the specific exception raised is irrelevant, it just needs to be unique
            raise
        except PDFUniteError as exc:
            # this could be caused by network hiccup
            log.info('[pdf_merge] retry generate   : ' + out_name)
            log.error('[pdf_merge] retry generate   : ' + str(exc))
            raise pdf_merge.retry(args=(pdf_files, out_name, pdf_base_dir, max_pdfunite_files), exc=exc)
    except Exception as e:
        log.error(str(e))
        raise


@celery.task(name="tasks.pdf.archive")
def archive(archive_file_name, directory):
    '''
    given a directory, archive everything in this directory to a file name specified
    '''
    try:
        prepare_path(archive_file_name)
        archive_files(directory, archive_file_name)
    except Exception:
        # unrecoverable exception
        raise PdfGenerationError('Unable to archive file(s): ' + directory + ', ' + archive_file_name)


@celery.task(name="tasks.pdf.hpz_upload_cleanup", max_retries=5)
def hpz_upload_cleanup(src_file_name, registration_id, pdf_base_dir):
    '''
    Remotely copies a source file to a remote machine
    '''
    try:
        # Upload to HPZ
        http_file_upload(src_file_name, registration_id)

        # Clean up the PDF merge working directory
        shutil.rmtree(os.path.join(pdf_base_dir, 'bulk', registration_id), ignore_errors=True)
    except RemoteCopyError as e:
        log.error("Exception happened in remote copy. " + str(e))
        try:
            # this looks funny to you, but this is just a work around solution for celery bug
            # since exc option is not really working for retry.
            # the specific exception raised is irrelevant, it just needs to be unique
            raise ValueError(str(e))
        except ValueError as exc:
            # this could be caused by network hiccup
            raise hpz_upload_cleanup.retry(args=[src_file_name, registration_id, pdf_base_dir], exc=exc)

    except Exception as e:
        raise RemoteCopyError(str(e))


@celery.task(name="tasks.pdf.separator")
def group_separator():
    '''
    A dummy task to separate out a chain of two consecutive groups
    '''
    pass


def _partial_pdfunite(pdf_files, pdf_tmp_dir, file_limit=ServicesConstants.MAX_PDFUNITE_FILE, timeout=TIMEOUT):
    files = []
    if file_limit < 1:
        raise PDFUniteError('file_limit must be grater than 1')
    elif file_limit is 1:
        for pdf_file in pdf_files:
            partial_outputfile = _get_next_partial_outputfile_name(pdf_tmp_dir)
            shutil.copy(pdf_file, partial_outputfile)
            files.append(partial_outputfile)
    else:
        files = _read_dir(pdf_tmp_dir)
        offset = len(files)
        partial_outputfile = _get_next_partial_outputfile_name(pdf_tmp_dir)
        while offset < int(len(pdf_files) / file_limit) or (offset == int(len(pdf_files) / file_limit) and int(len(pdf_files) % file_limit) > 0):
            if offset == int(os.path.basename(partial_outputfile)):
                if offset == int(len(pdf_files) / file_limit):
                    partial_file_list = pdf_files[-1 * int(len(pdf_files) % file_limit):]
                else:
                    end = (offset + 1) * file_limit if offset is not int(len(pdf_files) / file_limit) else len(pdf_files)
                    partial_file_list = pdf_files[offset * file_limit:end]
                if len(partial_file_list) is 1:
                    files.append(partial_file_list[0])
                else:
                    files.append(partial_outputfile)
                    try:
                        _pdfunite_subprocess(partial_file_list, partial_outputfile, timeout)
                    except PdfGenerationError:
                        # delete partial_outputfiles
                        delete(partial_outputfile)
                        raise
                partial_outputfile = _get_next_partial_outputfile_name(pdf_tmp_dir)
            offset += 1
    return files


def _read_dir(pdf_tmp_dir):
    files = [os.path.join(pdf_tmp_dir, f) for f in os.listdir(pdf_tmp_dir) if os.path.isfile(os.path.join(pdf_tmp_dir, f))]
    if files:
        files.sort()
    return files


def _get_next_partial_outputfile_name(pdf_tmp_dir):
    '''
    generate next partial pdf filename for pdfunite
    '''
    next_filename = None
    files = _read_dir(pdf_tmp_dir)
    if files:
        filename = files[-1]
        next_filename = os.path.join(pdf_tmp_dir, ('%03d' % (int(os.path.basename(filename)) + 1)))
    else:
        next_filename = os.path.join(pdf_tmp_dir, "001")
    return next_filename


def _pdfunite_subprocess(input_files, output_file, timeout):
    exception = None
    try:
        proc = Popen(pdfunite_procs + input_files + [output_file])
        proc.wait(timeout=timeout)
        if proc is not None and proc.returncode is not 0:
            stderr = proc.communicate()[1]
            # raise if there ie error
            exception = PDFUniteError('pdfunite: ' + str(stderr))
    except Exception as e:
        exception = PDFUniteError(str(e))
    if exception is not None:
        raise exception


def _count_pdf_pages(pdf_path):
    seen = {'type': False,  # /Type
            'pages': False,  # /Pages
            'kids': False,  # /Kids
            'count': False  # /Count
            }

    def reset():
        seen['type'] = False
        seen['pages'] = False
        seen['count'] = False

    with open(pdf_path, 'rb') as file:
        for line in file:
            skip = True
            if line.startswith(b'<<') or b'obj <<' in line:
                reset()
                line = line[line.find(b'<<'):]
            if seen['type']:
                skip = False
            elif not seen['type'] and b'/Type' in line:
                skip = False

            if not skip:
                parts = line.strip().split(b' ')
                for part in parts:
                    if not seen['type'] and not seen['pages'] and part == b'/Type':
                        seen['type'] = True
                    elif seen['type'] and not seen['pages'] and part == b'/Pages':
                        seen['pages'] = True
                    elif seen['type'] and seen['pages'] and part == b'/Count':
                        seen['count'] = True
                    elif part.isdigit() and seen['type'] and seen['pages'] and seen['count']:
                        return int(part)

    return -1
