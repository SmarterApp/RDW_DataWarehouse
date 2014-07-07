'''
Created on May 14, 2013

@author: dip
'''
import unittest
import services
from services.tasks.pdf import generate, OK, \
    prepare_path, get, is_valid, delete, prepare, bulk_pdf_cover_sheet, \
    _build_url, pdf_merge, archive, hpz_upload_cleanup, group_separator, \
    _partial_pdfunite, _read_dir, _get_next_partial_outputfile_name, \
    _pdfunite_subprocess, _count_pdf_pages
from services.celery import setup_global_settings
import platform
import os
import tempfile
import shutil
from services.exceptions import PdfGenerationError, PDFUniteError
from edcore.exceptions import NotForWindowsException, RemoteCopyError
from unittest.mock import patch, Mock
from celery.exceptions import MaxRetriesExceededError
from services.constants import ServicesConstants
from subprocess import Popen


class TestCreatePdf(unittest.TestCase):

    def setUp(self):
        self.__temp_dir = tempfile.mkdtemp()
        settings = {'pdf.minimum_file_size': '1'}
        setup_global_settings(settings)
        services.tasks.pdf.mswindows = False

    def tearDown(self):
        shutil.rmtree(self.__temp_dir, ignore_errors=True)

    def test_generate_pdf_success_cmd(self):
        services.tasks.pdf.pdf_procs = ['echo', 'dummy']
        file_name = os.path.join(self.__temp_dir, 'b', 'd.pdf')
        prepare_path(file_name)
        with open(file_name, 'w') as file:
            file.write('%PDF-1.4')
        task = generate('cookie', 'url', file_name)
        self.assertEqual(task, OK)

    def test_generate_pdf_timeout_with_output_file_generated(self):
        here = os.path.abspath(__file__)
        services.tasks.pdf.pdf_procs = get_cmd()
        task = generate('cookie', 'url', here, options=[], timeout=1)
        self.assertEqual(task, OK)

    def test_generate_pdf_timeout_without_output_file_generated(self):
        cur_dir = os.path.dirname(__file__)
        output_file = os.path.abspath(os.path.join(cur_dir, 'doesnotexist.out'))
        services.tasks.pdf.pdf_procs = get_cmd()
        self.assertRaises(PdfGenerationError, generate, 'cookie', 'url', output_file, options=[], timeout=1, grayscale=True)

    def test_generate_with_retries(self):
        settings = {'pdf.minimum_file_size': '1000000'}
        setup_global_settings(settings)
        services.tasks.pdf.pdf_procs = ['echo', 'dummy']
        file_name = os.path.join(self.__temp_dir, 'b', 'd.pdf')
        self.assertRaises(PdfGenerationError, generate, 'cookie', 'url', file_name, timeout=1)

    def test_generate_pdf_fail_cmd(self):
        services.tasks.pdf.pdf_procs = ['dummycmd']
        self.assertRaises(PdfGenerationError, generate, 'cookie', 'url', 'outputfile')

    def test_generate_win32(self):
        services.tasks.pdf.mswindows = True
        self.assertRaises(NotForWindowsException, generate, 'cookie', 'url', 'outputfile')

    def test_get_pdf_valid_file(self):
        services.tasks.pdf.pdf_procs = ['echo', 'dummy']
        here = os.path.abspath(__file__)
        task = get('cookie', 'url', here)
        self.assertIsNotNone(task)

    def test_create_directory(self):
        file_name = os.path.join(self.__temp_dir, 'a', 'b', 'c', 'd.pdf')
        # make sure directory does not exist first.
        shutil.rmtree(os.path.dirname(file_name), ignore_errors=True)
        prepare_path(file_name)
        self.assertTrue(os.access(os.path.dirname(file_name), os.R_OK))

    def test_no_exception_when_dir_exist(self):
        file_name = os.path.join(self.__temp_dir, 'a', 'b', 'c', 'd.pdf')
        prepare_path(file_name)
        prepare_path(file_name)
        self.assertTrue(os.path.exists(os.path.dirname(file_name)))

    def test_validate_file_non_existing_file(self):
        path = os.path.join(self.__temp_dir, 'notexist.pdf')
        valid = is_valid(path)
        self.assertFalse(valid)

    def test_validate_file_existing_file(self):
        here = os.path.abspath(__file__)
        valid = is_valid(here)
        self.assertTrue(valid)

    def test_validate_file_size_too_small(self):
        settings = {'pdf.minimum_file_size': '1000000'}
        setup_global_settings(settings)
        here = os.path.abspath(__file__)
        valid = is_valid(here)
        self.assertFalse(valid)

    def test_is_valid_cover(self):
        tmpdir = tempfile.TemporaryDirectory()
        filename = os.path.join(tmpdir.name, ServicesConstants.COVER_SHEET_NAME_PREFIX + 'test.pdf')
        with open(filename, 'b+w') as file:
            file.seek(ServicesConstants.MINIMUM_COVER_FILE_SIZE + 1)
            file.write(bytes('\0', 'UTF-8'))
        isvalid = is_valid(filename)
        tmpdir.cleanup()
        self.assertTrue(isvalid)

    def test_delete_file(self):
        file_name = os.path.join(self.__temp_dir, 'i_exist')
        prepare_path(file_name)
        with open(file_name, 'w') as file:
            file.write('%PDF-1.4')
        delete(file_name)
        self.assertFalse(os.path.exists(file_name))

    def test_prepare_file_already_created(self):
        outfile = tempfile.NamedTemporaryFile()
        return_value = prepare('cookie', 'url', outfile.name, options='pdf_defaults', timeout=0, cookie_name='edware', grayscale=False, always_generate=False)
        self.assertTrue(os.path.exists(outfile.name))
        self.assertFalse(return_value)
        outfile.close()

    @patch('services.tasks.pdf.generate')
    def test_prepare_file_already_created_forced(self, generate_mock):
        generate_mock.return_value = True
        outfile = tempfile.NamedTemporaryFile()
        return_value = prepare('cookie', 'url', outfile.name, options='pdf_defaults', timeout=0, cookie_name='edware', grayscale=False, always_generate=True)
        self.assertFalse(os.path.exists(outfile.name))
        self.assertTrue(return_value)

    @patch('services.tasks.pdf.generate')
    def test_prepare_file_exception(self, generate_mock):
        generate_mock.side_effect = MaxRetriesExceededError()
        self.assertRaises(PdfGenerationError, prepare, 'cookie', 'url', 'outfile.name', options='pdf_defaults', timeout=0, cookie_name='edware', grayscale=False, always_generate=True)

    @patch('services.tasks.pdf._build_url')
    @patch('services.tasks.pdf.generate')
    def test_bulk_pdf_cover_sheet(self, mock_generate, mock_build_url):
        mock_generate.return_value = None
        mock_build_url.return_value = None
        value = bulk_pdf_cover_sheet('cookie', 'out_name', 'merged_pdf_filename', 'base_url', 'base_params')
        self.assertIsNone(value)

    @patch('services.tasks.pdf._count_pdf_pages')
    def test_build_url(self, mock_count_pdf_pages):
        mock_count_pdf_pages.return_value = 43
        url = _build_url('http://www.foo.com/', {}, '/tmp/test.pdf')
        self.assertEqual(url, 'http://www.foo.com/?pageCount=43')

    def test_pdf_merge_merged_file_exist(self):
        outfile = tempfile.NamedTemporaryFile()
        self.assertRaises(PdfGenerationError, pdf_merge, ['pdf_files'], outfile.name, 'pdf_base_dir')
        outfile.close()

    @patch('services.tasks.pdf.prepare_path')
    def test_pdf_merge_pdf_file_doesnot_exist(self, mock_prepare_path):
        self.assertRaises(PdfGenerationError, pdf_merge, ['/foo/pdf_files_doesnot_exist'], '/foo/merged.pdf', 'pdf_base_dir')

    @patch('services.tasks.pdf.os.path.exists')
    @patch('services.tasks.pdf._pdfunite_subprocess')
    @patch('services.tasks.pdf._partial_pdfunite')
    @patch('services.tasks.pdf.prepare_path')
    @patch('services.tasks.pdf.os.path.isfile')
    def test_pdf_merge_more_than_max_pdf(self, mock_isfile, mock_prepare_path, mock_partial_pdfunite, mock_pdfunite_subprocess, mock_exists):
        mock_isfile.return_value = True
        mock_exists.side_effect = [False, True]
        pdffiles = ['/foo/1', '/foo/2', '/foo/3', '/foo/4', '/foo/5', '/foo/6', '/foo/7']
        pdf_merge(pdffiles, '/foo/outfile', '/foo', max_pdfunite_files=2)
        self.assertTrue(mock_partial_pdfunite.called)
        self.assertEqual(1, mock_partial_pdfunite.call_count)
        partial_pdfunite_inputs = mock_partial_pdfunite.call_args[0][0]
        self.assertTrue(partial_pdfunite_inputs == pdffiles)

    @patch('services.tasks.pdf.shutil.copyfile')
    @patch('services.tasks.pdf.prepare_path')
    @patch('services.tasks.pdf.os.path.isfile')
    def test_pdf_merge_single_pdf(self, mock_isfile, mock_prepare_path, mock_copyfile):
        mock_isfile.return_value = True
        pdffiles = ['/foo/1']
        pdf_merge(pdffiles, '/foo/outfile', '/foo', max_pdfunite_files=2)
        self.assertTrue(mock_copyfile.called)
        self.assertEqual(1, mock_copyfile.call_count)

    @patch('services.tasks.pdf._pdfunite_subprocess')
    @patch('services.tasks.pdf.prepare_path')
    @patch('services.tasks.pdf.os.path.isfile')
    def test_pdf_merge(self, mock_isfile, mock_prepare_path, mock_pdfunite_subprocess):
        mock_isfile.return_value = True
        pdffiles = ['/foo/1', '/foo/2', '/foo/3', '/foo/4', '/foo/5', '/foo/6', '/foo/7']
        pdf_merge(pdffiles, '/foo/outfile', '/foo', max_pdfunite_files=10)
        self.assertTrue(mock_pdfunite_subprocess.called)
        self.assertEqual(1, mock_pdfunite_subprocess.call_count)
        partial_pdfunite_inputs = mock_pdfunite_subprocess.call_args[0][0]
        self.assertTrue(partial_pdfunite_inputs == pdffiles)

    @patch('services.tasks.pdf.pdf_merge.retry')
    @patch('services.tasks.pdf._pdfunite_subprocess')
    @patch('services.tasks.pdf.prepare_path')
    @patch('services.tasks.pdf.os.path.isfile')
    def test_pdf_merge_handle_PDFUniteError(self, mock_isfile, mock_prepare_path, mock_pdfunite_subprocess, mock_retry):
        mock_isfile.return_value = True
        mock_pdfunite_subprocess.side_effect = PDFUniteError()
        mock_retry.side_effect = Exception()
        pdffiles = ['/foo/1', '/foo/2', '/foo/3', '/foo/4', '/foo/5', '/foo/6', '/foo/7']
        self.assertRaises(Exception, pdf_merge, pdffiles, '/foo/outfile', '/foo', max_pdfunite_files=10)
        self.assertTrue(mock_retry.called)
        self.assertEqual(1, mock_retry.call_count)

    @patch('services.tasks.pdf.pdf_merge.retry')
    @patch('services.tasks.pdf._pdfunite_subprocess')
    @patch('services.tasks.pdf.prepare_path')
    @patch('services.tasks.pdf.os.path.isfile')
    def test_pdf_merge_handle_Exception(self, mock_isfile, mock_prepare_path, mock_pdfunite_subprocess, mock_retry):
        mock_isfile.return_value = True
        mock_pdfunite_subprocess.side_effect = Exception()
        pdffiles = ['/foo/1', '/foo/2', '/foo/3', '/foo/4', '/foo/5', '/foo/6', '/foo/7']
        self.assertRaises(Exception, pdf_merge, pdffiles, '/foo/outfile', '/foo', max_pdfunite_files=10)
        self.assertFalse(mock_retry.called)
        self.assertEqual(0, mock_retry.call_count)

    @patch('services.tasks.pdf.prepare_path')
    @patch('services.tasks.pdf.archive_files')
    def test_archive(self, mock_archive_files, mock_prepare_path):
        archive(None, None)
        self.assertTrue(mock_archive_files.called)
        self.assertTrue(mock_prepare_path.called)

    @patch('services.tasks.pdf.prepare_path')
    @patch('services.tasks.pdf.archive_files')
    def test_archive_Exception(self, mock_archive_files, mock_prepare_path):
        mock_prepare_path.side_effect = Exception()
        self.assertRaises(PdfGenerationError, archive, '/foo1', '/foo2')

    @patch('services.tasks.pdf.http_file_upload')
    @patch('services.tasks.pdf.shutil.rmtree')
    def test_hpz_upload_cleanup(self, mock_rmtree, mock_http_file_upload):
        hpz_upload_cleanup('/foo1', '123', '/foo2')
        self.assertTrue(mock_rmtree.called)
        self.assertTrue(mock_http_file_upload.called)

    @patch('services.tasks.pdf.hpz_upload_cleanup.retry')
    @patch('services.tasks.pdf.http_file_upload')
    @patch('services.tasks.pdf.shutil.rmtree')
    def test_hpz_upload_cleanup_RemoteCopyError(self, mock_rmtree, mock_http_file_upload, mock_retry):
        mock_http_file_upload.side_effect = RemoteCopyError('error')
        mock_retry.side_effect = Exception()
        self.assertRaises(Exception, hpz_upload_cleanup, '/foo1', '123', '/foo2')

    @patch('services.tasks.pdf.http_file_upload')
    @patch('services.tasks.pdf.shutil.rmtree')
    def test_hpz_upload_cleanup_Exception(self, mock_rmtree, mock_http_file_upload):
        mock_http_file_upload.side_effect = Exception()
        self.assertRaises(RemoteCopyError, hpz_upload_cleanup, '/foo1', '123', '/foo2')

    def test_group_separator(self):
        value = group_separator()
        self.assertIsNone(value)

    def test_partial_pdfunite_file_limit_0(self):
        pdffiles = ['/foo/1', '/foo/2', '/foo/3', '/foo/4', '/foo/5', '/foo/6', '/foo/7']
        file_limit = 0
        self.assertRaises(PDFUniteError, _partial_pdfunite, pdffiles, '/opt/pdf', file_limit)

    @patch('services.tasks.pdf.shutil.copy')
    @patch('services.tasks.pdf._get_next_partial_outputfile_name')
    def test_partial_pdfunite_file_limit_1(self, mock_get_next_partial_outputfile_name, mock_copy):
        pdffiles = ['/foo/1', '/foo/2', '/foo/3', '/foo/4', '/foo/5', '/foo/6', '/foo/7']
        mock_get_next_partial_outputfile_name.side_effect = ['/foo/.partial/000', '/foo/.partial/001', '/foo/.partial/002', '/foo/.partial/003', '/foo/.partial/004', '/foo/.partial/005', '/foo/.partial/006', '/foo/.partial/007']
        files = _partial_pdfunite(pdffiles, '/opt/pdf', 1)
        self.assertEqual(files, ['/foo/.partial/000', '/foo/.partial/001', '/foo/.partial/002', '/foo/.partial/003', '/foo/.partial/004', '/foo/.partial/005', '/foo/.partial/006'])

    @patch('services.tasks.pdf._pdfunite_subprocess')
    @patch('services.tasks.pdf._get_next_partial_outputfile_name')
    @patch('services.tasks.pdf._read_dir')
    @patch('services.tasks.pdf.prepare_path')
    def test_partial_pdfunite_file_limit_2(self, mock_prepare_path, mock_read_dir, mock_get_next_partial_outputfile_name, mock_pdfunite_subprocess):
        mock_read_dir.return_value = []
        mock_get_next_partial_outputfile_name.side_effect = ['/foo/.partial/000', '/foo/.partial/001', '/foo/.partial/002', '/foo/.partial/003', '/foo/.partial/004', '/foo/.partial/005', '/foo/.partial/006', '/foo/.partial/007']
        pdffiles = ['/foo/1', '/foo/2', '/foo/3', '/foo/4', '/foo/5', '/foo/6', '/foo/7']
        files = _partial_pdfunite(pdffiles, '/opt/pdf', 2)
        self.assertEqual(files, ['/foo/.partial/000', '/foo/.partial/001', '/foo/.partial/002', '/foo/7'])

    @patch('services.tasks.pdf._pdfunite_subprocess')
    @patch('services.tasks.pdf._get_next_partial_outputfile_name')
    @patch('services.tasks.pdf._read_dir')
    @patch('services.tasks.pdf.prepare_path')
    def test_partial_pdfunite_file_limit_2_cont(self, mock_prepare_path, mock_read_dir, mock_get_next_partial_outputfile_name, mock_pdfunite_subprocess):
        mock_read_dir.return_value = ['/foo/.partial/000', '/foo/.partial/001']
        mock_get_next_partial_outputfile_name.side_effect = ['/foo/.partial/002', '/foo/.partial/003', '/foo/.partial/004', '/foo/.partial/005', '/foo/.partial/006', '/foo/.partial/007']
        pdffiles = ['/foo/1', '/foo/2', '/foo/3', '/foo/4', '/foo/5', '/foo/6', '/foo/7']
        files = _partial_pdfunite(pdffiles, '/opt/pdf', 2)
        self.assertEqual(files, ['/foo/.partial/000', '/foo/.partial/001', '/foo/.partial/002', '/foo/7'])

    @patch('services.tasks.pdf._pdfunite_subprocess')
    @patch('services.tasks.pdf._get_next_partial_outputfile_name')
    @patch('services.tasks.pdf._read_dir')
    @patch('services.tasks.pdf.prepare_path')
    def test_partial_pdfunite_file_limit_4(self, mock_prepare_path, mock_read_dir, mock_get_next_partial_outputfile_name, mock_pdfunite_subprocess):
        mock_read_dir.return_value = []
        mock_get_next_partial_outputfile_name.side_effect = ['/foo/.partial/000', '/foo/.partial/001', '/foo/.partial/002', '/foo/.partial/003', '/foo/.partial/004', '/foo/.partial/005', '/foo/.partial/006', '/foo/.partial/007']
        pdffiles = ['/foo/1', '/foo/2', '/foo/3', '/foo/4', '/foo/5', '/foo/6', '/foo/7']
        files = _partial_pdfunite(pdffiles, '/opt/pdf', 4)
        self.assertEqual(files, ['/foo/.partial/000', '/foo/.partial/001'])

    @patch('services.tasks.pdf._pdfunite_subprocess')
    @patch('services.tasks.pdf._get_next_partial_outputfile_name')
    @patch('services.tasks.pdf._read_dir')
    @patch('services.tasks.pdf.prepare_path')
    def test_partial_pdfunite_file_limit_10(self, mock_prepare_path, mock_read_dir, mock_get_next_partial_outputfile_name, mock_pdfunite_subprocess):
        mock_read_dir.return_value = []
        mock_get_next_partial_outputfile_name.side_effect = ['/foo/.partial/000', '/foo/.partial/001', '/foo/.partial/002', '/foo/.partial/003', '/foo/.partial/004', '/foo/.partial/005', '/foo/.partial/006', '/foo/.partial/007']
        pdffiles = ['/foo/1', '/foo/2', '/foo/3', '/foo/4', '/foo/5', '/foo/6', '/foo/7']
        files = _partial_pdfunite(pdffiles, '/opt/pdf', 10)
        self.assertEqual(files, ['/foo/.partial/000'])

    @patch('services.tasks.pdf.delete')
    @patch('services.tasks.pdf._pdfunite_subprocess')
    @patch('services.tasks.pdf._get_next_partial_outputfile_name')
    @patch('services.tasks.pdf._read_dir')
    @patch('services.tasks.pdf.prepare_path')
    def test_partial_pdfunite_Exception(self, mock_prepare_path, mock_read_dir, mock_get_next_partial_outputfile_name, mock_pdfunite_subprocess, mock_delete):
        mock_read_dir.return_value = []
        mock_get_next_partial_outputfile_name.side_effect = ['/foo/.partial/000', '/foo/.partial/001', '/foo/.partial/002', '/foo/.partial/003', '/foo/.partial/004', '/foo/.partial/005', '/foo/.partial/006', '/foo/.partial/007']
        mock_pdfunite_subprocess.side_effect = PdfGenerationError()
        pdffiles = ['/foo/1', '/foo/2', '/foo/3', '/foo/4', '/foo/5', '/foo/6', '/foo/7']
        self.assertRaises(PdfGenerationError, _partial_pdfunite, pdffiles, '/opt/pdf', 10)

    def test_read_dir(self):
        d = tempfile.TemporaryDirectory()
        file1 = os.path.join(d.name, '003')
        file2 = os.path.join(d.name, '013')
        file3 = os.path.join(d.name, '103')
        file4 = os.path.join(d.name, '011')
        open(file1, 'a').close()
        open(file2, 'a').close()
        open(file3, 'a').close()
        open(file4, 'a').close()
        files = _read_dir(d.name)
        d.cleanup()
        self.assertEqual(files, [file1, file4, file2, file3])

    def test_read_dir_empty(self):
        d = tempfile.TemporaryDirectory()
        files = _read_dir(d.name)
        d.cleanup()
        self.assertEqual(files, [])

    @patch('services.tasks.pdf._read_dir')
    def test_get_next_partial_outputfile_name(self, mock_read_dir):
        mock_read_dir.return_value = []
        next_file = _get_next_partial_outputfile_name('/foo')
        self.assertEqual(next_file, '/foo/001')
        mock_read_dir.return_value = ['/foo/000', '/foo/001']
        next_file = _get_next_partial_outputfile_name('/foo')
        self.assertEqual(next_file, '/foo/002')

    @patch('services.tasks.pdf.Popen')
    def test_pdfunite_subprocess(self, mock_Popen):
        mock_Popen.return_value.returncode = 0
        value = _pdfunite_subprocess(['/foo/1'], '/foo/2', 1)
        self.assertIsNone(value)

    @patch('services.tasks.pdf.Popen')
    def test_pdfunite_subprocess_error_returncode(self, mock_Popen):
        mock_Popen.return_value.returncode = 255
        mock_Popen.return_value.communicate.return_value = ('', 'hello')
        self.assertRaises(PDFUniteError, _pdfunite_subprocess, ['/foo/1'], '/foo/2', 1)

    @patch('services.tasks.pdf.Popen')
    def test_pdfunite_subprocess_exception(self, mock_Popen):
        mock_Popen.return_value.wait.side_effect = Exception()
        self.assertRaises(PDFUniteError, _pdfunite_subprocess, ['/foo/1'], '/foo/2', 1)

    def test_count_pdf_pages(self):
        outfile = tempfile.NamedTemporaryFile(delete=False)
        outfile.write('hello\n'.encode('utf-8'))
        outfile.write('/Type /Pages /Kids\n'.encode('utf-8'))
        outfile.write('/Count 1242\n'.encode('utf-8'))
        outfile.write('hello\n'.encode('utf-8'))
        outfile.close()
        page = _count_pdf_pages(outfile.name)
        os.remove(outfile.name)
        self.assertEqual(1242, page)

        def test_count_pdf_pages2(self):
            outfile = tempfile.NamedTemporaryFile(delete=False)
            outfile.write('6083 0 obj\n'.encode('utf-8'))
            outfile.write('<< /Type /Pages /Kids [ 6084 0 R 6085 0 R 6086 0 R 6087 0 R 6088 0 R 6089 0 R 6090 0 R 6091 0 R 6092 0 R 6093 0 R 6094 0 R 6095 0 R 6096 0 R 6097 0 R 6098 0 R 6099 0 R 6100 0 R 6101 0 R 6102 0 R 6103 0 R 6104 0 R 6105 0 R 6106 0 R 6107 0 R 6108 0 R 6109 0 R 6110 0 R 6111 0 R 6112 0 R 6113 0 R 6114 0 R 6115 0 R 6116 0 R 6117 0 R 6118 0 R 6119 0 R 6120 0 R 6121 0 R 6122 0 R 6123 0 R 6124 0 R 6125 0 R 6126 0 R 6127 0 R 6128 0 R 6129 0 R 6130 0 R 6131 0 R 6132 0 R 6133 0 R 6134 0 R 6135 0 R 6136 0 R 6137 0 R 6138 0 R 6139 0 R 6140 0 R 6141 0 R 6142 0 R 6143 0 R 6144 0 R 6145 0 R 6146 0 R 6147 0 R 6148 0 R 6149 0 R 6150 0 R 6151 0 R 6152 0 R 6153 0 R 6154 0 R 6155 0 R 6156 0 R 6157 0 R 6158 0 R 6159 0 R 6160 0 R 6161 0 R 6162 0 R 6163 0 R 6164 0 R 6165 0 R ] /Count 82 >>\n'.encode('utf-8'))
            outfile.write('endobj\n'.encode('utf-8'))
            outfile.close()
            page = _count_pdf_pages(outfile.name)
            os.remove(outfile.name)
            self.assertEqual(82, page)

        def test_count_pdf_pages3(self):
            outfile = tempfile.NamedTemporaryFile(delete=False)
            outfile.write('1 0 obj\n'.encode('utf-8'))
            outfile.write('<< /Type /Pages\n'.encode('utf-8'))
            outfile.write('/Count 24\n'.encode('utf-8'))
            outfile.write('/Kids [7 0 R 35 0 R 44 0 R 46 0 R 48 0 R 50 0 R 52 0 R 54 0 R 56 0 R 58 0 R 60 0 R 62 0 R 64 0 R 66 0 R 68 0 R 70 0 R 72 0 R 74 0 R 76 0 R 78 0 R 80 0 R 86 0 R 91 0 R 93 0 R ] >>\n'.encode('utf-8'))
            outfile.write('endobj\n'.encode('utf-8'))
            outfile.close()
            page = _count_pdf_pages(outfile.name)
            os.remove(outfile.name)
            self.assertEqual(24, page)

    def test_count_pdf_pages_wrong_format1(self):
        outfile = tempfile.NamedTemporaryFile(delete=False)
        outfile.write('hello\n'.encode('utf-8'))
        outfile.write('/Type /Page /Kids\n'.encode('utf-8'))
        outfile.write('/Count 1242\n'.encode('utf-8'))
        outfile.write('hello\n'.encode('utf-8'))
        outfile.close()
        page = _count_pdf_pages(outfile.name)
        os.remove(outfile.name)
        self.assertEqual(-1, page)

    def test_count_pdf_pages_wrong_format2(self):
        outfile = tempfile.NamedTemporaryFile(delete=False)
        outfile.write('hello\n'.encode('utf-8'))
        outfile.write('<< /Type /Pages /Kid\n'.encode('utf-8'))
        outfile.write('<< /Type /Page /Kids\n'.encode('utf-8'))
        outfile.write('/Count 1242\n'.encode('utf-8'))
        outfile.write('hello\n'.encode('utf-8'))
        outfile.close()
        page = _count_pdf_pages(outfile.name)
        os.remove(outfile.name)
        self.assertEqual(-1, page)


def get_cmd():
    '''
    Based on os type, return the command to execute test script
    '''
    cur_dir = os.path.dirname(__file__)
    test_file = os.path.abspath(os.path.join(cur_dir, '..', 'resources', 'sleep.sh'))
    cmd = ['sh', test_file]
    if platform.system() == 'Windows':
        test_file = os.path.abspath(os.path.join(cur_dir, '..', 'resources', 'sleep.cmd'))
        cmd = [test_file]
    return cmd


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
