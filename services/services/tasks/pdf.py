'''
Celery Tasks for pdf generation

Created on May 10, 2013

@author: dawu
'''
import os
import sys
import errno
import logging
import urllib.parse
import copy
import shutil
import uuid
import subprocess
from subprocess import Popen

from celery.exceptions import MaxRetriesExceededError

from edcore.exceptions import NotForWindowsException, RemoteCopyError
from edcore.utils.utils import archive_files

import services
from services.celery import celery
from services.exceptions import PdfGenerationError, PDFUniteError
from services.celery import TIMEOUT
from services.constants import ServicesConstants

from hpz_client.frs.http_file_upload import http_file_upload

mswindows = (sys.platform == "win32")
pdf_procs = ['wkhtmltopdf']
pdfunite_procs = ['pdfunite']
pdf_defaults = ['--enable-javascript', '--page-size', 'Letter', '--print-media-type', '-l', '--footer-center', 'Page [page] of [toPage]', '--footer-font-size', '9']
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
        wkhtmltopdf_option.append('--javascript-delay')
        wkhtmltopdf_option.append(str(services.celery.JAVASCRIPT_DELAY))
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


def _make_uniq_temp_dir(pdf_base_dir):
    temp_dir_path = os.path.join(pdf_base_dir, '.tmp', 'partial', uuid.uuid4().hex)

    try:
        os.makedirs(temp_dir_path, mode=0o700, exist_ok=False)
    except OSError as e:
        # we expect that directory can already exist. in that case we just try again
        # and re-raise the error if it's not related
        if e.errno != errno.EEXIST:
            log.error('Received unexpected error when tried to create unique temp dir')
            raise

        return _make_uniq_temp_dir(pdf_base_dir)

    return temp_dir_path


@celery.task(name='tasks.pdf.merge', max_retries=ServicesConstants.PDF_MERGE_MAX_RETRY, default_retry_delay=ServicesConstants.PDF_MERGE_RETRY_DELAY)
def pdf_merge(pdf_files, out_name, pdf_base_dir, max_pdfunite_files=ServicesConstants.MAX_PDFUNITE_FILE):
    if os.path.exists(out_name):
        log.error(out_name + " is already exist")
        raise PdfGenerationError()

    # Prepare output file
    prepare_path(out_name)

    # Verify that all PDFs to merge exist
    for pdf_file in pdf_files:
        if not os.path.isfile(pdf_file):
            raise PdfGenerationError('file does not exist: ' + pdf_file)

    try:
        # UNIX can handle upto 1024 file descriptors in default.  To be safe we process 50 files at once.
        if len(pdf_files) > max_pdfunite_files:
            pdf_temp_dir = _make_uniq_temp_dir(pdf_base_dir)
            path_to_merged = _partial_pdfunite(pdf_files, pdf_temp_dir,
                                               timeout=services.celery.PDFUNITE_TIMEOUT,
                                               file_limit=max_pdfunite_files)

            shutil.copyfile(path_to_merged, out_name)
            shutil.rmtree(pdf_temp_dir, ignore_errors=True)
        elif len(pdf_files) is 1:
            # pdfunite is not callable if there is only one pdf to merge
            shutil.copyfile(pdf_files[0], out_name)
        else:
            _pdfunite_subprocess(pdf_files, out_name, services.celery.PDFUNITE_TIMEOUT)
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


def chunker(pdf_files, chunk_size):
    for offset in range(0, len(pdf_files), chunk_size):
        yield pdf_files[offset:offset + chunk_size]


def merge_files(pdf_files, output_filename, timeout):
    try:
        _pdfunite_subprocess(pdf_files, output_filename, timeout)
    except PdfGenerationError:
        log.error("Pdf generation of [%s] failed. Tried to merge following files: %s",
                  output_filename, pdf_files)
        raise


def _partial_pdfunite(pdf_files, pdf_tmp_dir, file_limit=ServicesConstants.MAX_PDFUNITE_FILE, timeout=TIMEOUT):
    # defyrlt: previous code supported `file_limit == 1`, but it doesn't make
    # any sense, so it was removed
    if file_limit < 2:
        raise PDFUniteError('file_limit must be grater than 1')

    files = []
    for chunk_num, chunk in enumerate(chunker(pdf_files, file_limit)):
        if len(chunk) == 1:
            # we shouldn't pass one file to `pdfunite` -- it's kind of already merged
            files.append(chunk[0])
            continue

        output_filename = os.path.join(pdf_tmp_dir, "{}.pdf".format(chunk_num))
        merge_files(chunk, output_filename, timeout)
        files.append(output_filename)

        # this part (and the whole function) is not recursive because we don't
        # want to run into max recursion depth error
        # here we're merging resulting files so we never pass more files than
        # specified in `file_limit` to the `_pdfunite_subprocess`
        if len(files) >= file_limit:
            range_filename = os.path.join(pdf_tmp_dir, "0-{}.pdf".format(chunk_num))
            merge_files(files, range_filename, timeout)
            files = [range_filename]

    if len(files) == 1:
        return files[0]

    output_filename = os.path.join(pdf_tmp_dir, "result.pdf")
    merge_files(files, output_filename, timeout)
    return output_filename


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
