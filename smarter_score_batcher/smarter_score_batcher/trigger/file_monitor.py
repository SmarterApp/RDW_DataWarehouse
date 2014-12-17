import os
import shutil
import logging
import logging.config
import json
from edcore.watch.util import FileUtil
from edcore.utils.utils import tar_files, read_ini
from edcore.utils.utils import run_cron_job, create_daemon
from edcore.utils.data_archiver import encrypt_file
from edcore.watch.file_hasher import MD5Hasher
from smarter_score_batcher.constant import Extensions, Constants
import time
import uuid
from argparse import ArgumentParser
from smarter_score_batcher.error.exceptions import FileMonitorFileNotFoundException, \
    FileMonitorException
from smarter_score_batcher.error.error_codes import ErrorSource, ErrorCode
from smarter_score_batcher.database.db_utils import get_metadata, get_assessments, \
    delete_assessments, get_error_message, get_all_assessment_guids
from smarter_score_batcher.database.tsb_connector import TSBDBConnection
from edcore.database import initialize_db
from smarter_score_batcher.error.exceptions import TSBSecurityException
from smarter_score_batcher.utils.file_utils import csv_file_writer, \
    json_file_writer


logger = logging.getLogger("smarter_score_batcher")


def move_to_staging(settings):
    ''' move assessment files from working directory to staging.

    This function is invoked by scheduler which will periodically check
    working directory for new assessments data. Working directory
    should have below structure:

    `working_dir/tenant/asmt_id/asmt_id.{json,csv}`

    Current design assumes only exactly one JSON file and one CSV file
    for each assessment, although it should be able to handle multiple
    files just fine.

    Upon each call, this function lists all tenants under working
    directory and process assessment data for each tenant one at a
    time. Firstly, it tries to get the lock of CSV file in current
    process which contains data. If CSV file lock couldn't be
    acquired, e.g. another process is writing data, it continues to
    next assessment data.

    Secondly, if current process gets the lock successfuly, this
    function creates a hidden temporary directory under each
    assessment folder and moves JSON file and CSV file over. It then
    archives the files into a tar file with gz2 compression, and
    encrypts it with gpg. A checksum file also be created for the gpg
    file.

    Thirdly, this function moves the gpg file and checksum file to
    staging directory, and tries to cleans up assessment directory by
    deleting it. The clean up might fail if another process starts
    writing data but this is fine.


    :param dict settings: settings defined in INI configuration file.
    '''
    logger.debug("start synchronizing files from working directory to staging directory")
    working_dir = settings['smarter_score_batcher.base_dir.working']
    staging_dir = settings['smarter_score_batcher.base_dir.staging']
    for tenant, assessment in get_all_assessment_guids():
        logger.debug("start processing assessment %s", assessment)
        try:
            with FileEncryption(working_dir, tenant, assessment) as fl:
                # TODO: should we make a backup before manipulating files?
                # encrypt tar file
                data_path = fl.save_to_tempdir()
                tar_file = fl.archive_to_tar(data_path)
                gpg_file_path = fl.encrypt(tar_file, settings)
                fl.move_files(gpg_file_path, staging_dir)
            logger.debug("complete processing assessment %s data", assessment)
        except BlockingIOError:
            # someone already lock.
            time.sleep(1)
        except FileNotFoundError:
            # if file not found, file might be already in process or
            msg = "assessment %s data not found for tenant %s" % (assessment, tenant)
            logger.debug(msg)
            raise FileMonitorFileNotFoundException(msg, err_source=ErrorSource.MOVE_TO_STAGE)
        except TSBSecurityException as e:
            logger.error("Path traversal vulnerability found: %s", e)
        except Exception as e:
            # pass to process next assessment data
            msg = "Error occurs during process assessment %s for tenant %s: %s" % (assessment, tenant, str(e))
            logger.error(msg)
            raise FileMonitorException(msg, err_source=ErrorSource.MOVE_TO_STAGE)


def run_cron_sync_file(settings):
    ''' Configure and run cron job to copy csv files to UDL landing zone for.

    :param dict settings:  configuration for the application
    '''
    run_cron_job(settings, 'trigger.assessment.', move_to_staging)


def _get_gpg_settings_by_tenant(tenant, settings):
    ''' fetches gpg encryption settings. '''
    recipient_key = 'smarter_score_batcher.gpg.public_key.' + tenant.lower()
    recipients = settings.get(recipient_key, None)
    homedir = settings.get('smarter_score_batcher.gpg.homedir', None)
    # TODO: don't really like below code, but this is necessary
    # because udl gpg is configured in '~/.gnupg' locally, otherwise
    # encrypt_file() function will give an error later.
    if homedir:
        homedir = os.path.expanduser(homedir)
    kw_settings = {
        "homedir": homedir,
        "keyserver": settings.get('smarter_score_batcher.gpg.keyserver', None),
        "gpgbinary": settings.get('smarter_score_batcher.gpg.path', 'gpg'),
        "passphrase": settings.get('smarter_score_batcher.gpg.passphrase', None),
        "sign": settings.get('smarter_score_batcher.gpg.sign', None)
    }
    return recipients, kw_settings


def prepare_assessment_dir(base_dir, state_code, asmt_id, mode=0o700):
    # prevent path traversal
    base_dir = os.path.abspath(base_dir)
    request_directory = os.path.join(base_dir, state_code.lower(), asmt_id)
    abs_request_directory = os.path.abspath(request_directory)
    if os.path.commonprefix([base_dir, request_directory, abs_request_directory]) == base_dir:
        os.makedirs(abs_request_directory, mode=mode, exist_ok=True)
    else:
        raise TSBSecurityException(msg='Issue creating path requested dir[' + abs_request_directory + ']', err_code=ErrorCode.PATH_TRAVERSAL_DETECTED, err_source=ErrorSource.PREPARE_ASSESSMENT_DIR)
    return abs_request_directory


class FileEncryption:

    def __init__(self, asmt_dir, tenant, assessment_id):
        ''' Constructor of FileEncryption class.

        :param tenant str: tenant name
        :param asmt_dir str: full os.path to assessment directory
        '''
        self.tenant = tenant
        self.asmt_dir = asmt_dir
        self.assessment_id = assessment_id
        self.tsb_asmt_rec_ids = []
        self.tsb_error_rec_ids = []
        self.__success = False
        self.hasher = MD5Hasher()

    def move_files(self, src_file, staging_dir):
        '''Moves encrypted file to `staging_dir`.

        This function first creates
        a checksum for given file `src_file`, and then move both to staging
        directory.

        :param src_file str: os.path to encrypted GPG file
        :param staging_dir str: staging directory

        '''
        # retain directory structure per tenant in staging
        dst_dir = os.path.join(staging_dir, self.tenant.lower())
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir, exist_ok=True)
        # create checksum
        checksum = self._create_checksum(src_file)
        dst_file = os.path.join(dst_dir, os.path.basename(src_file))
        # add .partial extension to avoid rsync copying incomplete file
        tmp_file = dst_file + Extensions.PARTIAL
        os.rename(src_file, tmp_file)
        # remove partial extension
        os.rename(tmp_file, dst_file)
        # move checksum file over
        shutil.move(checksum, dst_dir)
        self.__success = True
        return dst_file

    def encrypt(self, tar_file, settings):
        ''' Encrypts `tar_file`.

        :param tar_file str: full os.path of archive file
        :param settings dict: application settings
        '''
        # move JSON and CSV file to temporary directory
        gpg_file = os.path.join(self.temp_dir, tar_file + Extensions.GPG)
        # get settings for encryption function
        recipients, kwargs = _get_gpg_settings_by_tenant(self.tenant, settings)
        with open(tar_file, 'rb') as file:
            encrypt_file(file, recipients, gpg_file, **kwargs)
        return gpg_file

    def __enter__(self):
        ''' acquires lock and creates a .tmp directory under current assessment'''
        self.temp_dir = prepare_assessment_dir(self.asmt_dir, self.tenant, self.assessment_id)
        return self

    def __exit__(self, type, value, tb):
        self.__cleanup()

    def __cleanup(self):
        ''' releases lock and remove .tmp directory. '''
        shutil.rmtree(self.temp_dir)
        delete_assessments(self.assessment_id, self.tsb_asmt_rec_ids, self.tsb_error_rec_ids)

    def save_to_tempdir(self):
        ''' moves JSON file and CSV file to temporary directory.

        This function moves JSON file before CSV because CSV file
        holds the lock.

        '''

        def _save_metadata(assessment_id, output_dir):
            metadata = get_metadata(asmtGuid=assessment_id)
            if not metadata:
                return
            filepath = os.path.join(output_dir, assessment_id + Extensions.JSON)
            content = json.loads(metadata[0][Constants.CONTENT])
            with open(filepath, mode='w') as f:
                json_file_writer(f, content)

        def _save_assessments(assessment_id, output_dir):
            asmt_guids, data, headers = get_assessments(asmtGuid=assessment_id)
            filepath = os.path.join(output_dir, assessment_id + Extensions.CSV)
            with open(filepath, mode='w') as f:
                csv_file_writer(f, data, header=headers)
            return asmt_guids

        def _save_errors(assessment_id, output_dir):
            error_guids, error_message = get_error_message(asmtGuid=assessment_id)
            if not error_guids:
                return
            filepath = os.path.join(output_dir, assessment_id + Extensions.ERR)
            with open(filepath, mode='w') as f:
                json_file_writer(f, error_message)
            return error_guids

        # create a directory with name `assessment id`
        tmp_dir = os.path.join(self.temp_dir, self.assessment_id)
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir, exist_ok=True)
        _save_metadata(self.assessment_id, tmp_dir)
        self.tsb_asmt_rec_ids = _save_assessments(self.assessment_id, tmp_dir)
        self.tsb_error_rec_ids = _save_errors(self.assessment_id, tmp_dir)
        return tmp_dir

    def archive_to_tar(self, data_path):
        ''' compress JSON and CSV file into tar which have the same assessment id.

        :param data_path str: full os.path of assessment directory.
        '''
        timestamp = time.strftime('%Y%m%d%H%M%S', time.gmtime())
        output = os.path.join(self.temp_dir, data_path + '.' + timestamp + '.' + str(uuid.uuid4()) + Extensions.TAR + Extensions.GZ)
        tar_files(data_path, output)
        return output

    def _create_checksum(self, source_file):
        ''' creates a md5 checksum file for `source_file`. '''
        checksum_value = self.hasher.get_file_hash(source_file)
        return FileUtil.create_checksum_file(source_file, checksum_value)


def main():
    '''
    Main Entry for ad-hoc testing to trigger batcher
    '''
    parser = ArgumentParser(description='File Batcher entry point')
    parser.add_argument('-p', dest='pid_file', default='/opt/edware/run/file-monitor-smarter_score_batcher.pid',
                        help="pid file for TSB file monitor daemon")
    parser.add_argument('-d', dest='daemon', action='store_true', default=False,
                        help="daemon mode for TSB file monitor")
    parser.add_argument('-i', dest='ini_file', default='/opt/edware/conf/smarter_score_batcher.ini', help="ini file")
    args = parser.parse_args()

    if args.daemon:
        create_daemon(args.pid_file)
    file = args.ini_file
    logging.config.fileConfig(file)
    settings = read_ini(file)
    initialize_db(TSBDBConnection, settings)
    if args.daemon:
        run_cron_sync_file(settings)
        while True:
            time.sleep(1)
    else:
        move_to_staging(settings)


if __name__ == '__main__':
    main()
