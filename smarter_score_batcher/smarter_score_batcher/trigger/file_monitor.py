import os
import shutil
import logging
from os import path
from edcore.watch.util import FileUtil
from edcore.utils.utils import tar_files
from edcore.utils.utils import run_cron_job
from edcore.utils.data_archiver import encrypt_file
from edcore.watch.file_hasher import MD5Hasher
from smarter_score_batcher.constant import Extensions
from smarter_score_batcher.utils.file_lock import FileLock


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
    for tenant, assessment in list_asmt_with_tenant(working_dir):
        logger.debug("start processing assessment %s", assessment)
        try:
            with FileEncryption(tenant, assessment) as fl:
                # TODO: should we make a backup before manipulating files?
                # encrypt tar file
                data_path = fl.move_to_tempdir()
                tar_file = fl.archive_to_tar(data_path)
                gpg_file_path = fl.encrypt(tar_file, settings)
                fl.move_files(gpg_file_path, staging_dir)
            # do housekeeping afterwards
            _clean_up(assessment)
        except FileNotFoundError:
            # if file not found, file might be already in process or
            logger.debug("assessment %s data not found for tenant",
                         assessment, tenant)
        except Exception as e:
            # pass to process next assessment data
            logger.error("Error occurs during process assessment %s for tenant %s: %s",
                         assessment, tenant, e)
        logger.debug("complete processing assessment %s data", assessment)


def _clean_up(dir_path):
    ''' clean up directory `dir_path`. '''
    try:
        os.rmdir(dir_path)
    except OSError as e:
        logger.warning("OSError occurs while attempting to remove %s: %s", dir_path, e)


def list_asmt_with_tenant(workspace):
    ''' Return list of (tenant, assessment directory path) tuple under workspace. '''
    def _valid_name(name):
        return name and not name.startswith(".")

    def _list_dirs(base_dir):
        return [(d, path.join(base_dir, d)) for d in os.listdir(base_dir) if path.isdir(path.join(base_dir, d)) and _valid_name(d)]

    files = []
    for tenant, tenant_full_path in _list_dirs(workspace):
        for _, asmt in _list_dirs(tenant_full_path):
            files.append((tenant, asmt))
    return files


def run_cron_sync_file(settings):
    ''' Configure and run cron job to copy csv files to UDL landing zone for.

    :param dict settings:  configuration for the application
    '''
    run_cron_job(settings, 'trigger.assessment.', move_to_staging)


def _get_gpg_settings_by_tenant(tenant, settings):
    ''' fetches gpg encryption settings. '''
    recipient_key = 'smarter_score_batcher.gpg.public_key.' + tenant
    recipients = settings.get(recipient_key, None)
    homedir = settings.get('smarter_score_batcher.gpg.homedir', None)
    # TODO: don't really like below code, but this is necessary
    # because udl gpg is configured in '~/.gnupg' locally, otherwise
    # encrypt_file() function will give an error later.
    if homedir:
        homedir = path.expanduser(homedir)
    kw_settings = {
        "homedir": homedir,
        "keyserver": settings.get('smarter_score_batcher.gpg.keyserver', None),
        "gpgbinary": settings.get('smarter_score_batcher.gpg.path', 'gpg'),
        "passphrase": settings.get('smarter_score_batcher.gpg.passphrase', None),
        "sign": settings.get('smarter_score_batcher.gpg.sign', None)
    }
    return recipients, kw_settings


class FileEncryption(FileLock):

    def __init__(self, tenant, asmt_dir):
        ''' Constructor of FileEncryption class.

        :param tenant str: tenant name
        :param asmt_dir str: full path to assessment directory
        '''
        self.tenant = tenant
        self.asmt_dir = asmt_dir
        self.assessment_id = path.split(asmt_dir)[1]
        self.lock_file = path.join(self.asmt_dir, self.assessment_id + Extensions.CSV)
        if not path.isfile(self.lock_file):
            raise FileNotFoundError()
        self.hasher = MD5Hasher()
        super().__init__(self.lock_file)

    def move_files(self, src_file, staging_dir):
        '''Moves encrypted file to `staging_dir`.

        This function first creates
        a checksum for given file `src_file`, and then move both to staging
        directory.

        :param src_file str: path to encrypted GPG file
        :param staging_dir str: staging directory

        '''
        # retain directory structure per tenant in staging
        dst_dir = path.join(staging_dir, self.tenant)
        if not path.exists(dst_dir):
            os.makedirs(dst_dir, exist_ok=True)
        # create checksum
        checksum = self._create_checksum(src_file)
        dst_file = path.join(dst_dir, path.basename(src_file))
        # add .partial extension to avoid rsync copying incomplete file
        tmp_file = dst_file + Extensions.PARTIAL
        os.rename(src_file, tmp_file)
        # remove partial extension
        os.rename(tmp_file, dst_file)
        # move checksum file over
        shutil.move(checksum, dst_dir)

    def encrypt(self, tar_file, settings):
        ''' Encrypts `tar_file`.

        :param tar_file str: full path of archive file
        :param settings dict: application settings
        '''
        # move JSON and CSV file to temporary directory
        gpg_file = path.join(self.temp_dir, tar_file + Extensions.GPG)
        # get settings for encryption function
        recipients, kwargs = _get_gpg_settings_by_tenant(self.tenant, settings)
        with open(tar_file, 'rb') as file:
            encrypt_file(file, recipients, gpg_file, **kwargs)
        return gpg_file

    def __enter__(self):
        ''' acquires lock and creates a .tmp directory under current assessment'''
        super().__enter__()
        self.temp_dir = path.join(self.asmt_dir, ".tmp")
        if not path.exists(self.temp_dir):
            os.makedirs(self.temp_dir, exist_ok=True)
        return self

    def __exit__(self, type, value, tb):
        ''' releases lock and remove .tmp directory. '''
        shutil.rmtree(self.temp_dir)
        super().__exit__(type, value, tb)

    def move_to_tempdir(self):
        ''' moves JSON file and CSV file to temporary directory.

        This function moves JSON file before CSV because CSV file
        holds the lock.

        '''

        def _list_file_with_ext(base_dir, ext):
            return [path.join(base_dir, f) for f in os.listdir(base_dir) if f.endswith(ext)]

        # create a directory with name `assessment id` under .tmp
        tmp_dir = path.join(self.temp_dir, self.assessment_id)
        if not path.exists(tmp_dir):
            os.makedirs(tmp_dir, exist_ok=True)
        # copy JSON and CSV files over
        # move JSON file before moving CSV
        for ext in [Extensions.JSON, Extensions.CSV]:
            for file in _list_file_with_ext(self.asmt_dir, ext):
                shutil.move(file, tmp_dir)
        return tmp_dir

    def archive_to_tar(self, data_path):
        ''' compress JSON and CSV file into tar which have the same assessment id.

        :param data_path str: full path of assessment directory.
        '''
        output = path.join(self.temp_dir, data_path + Extensions.TAR + Extensions.GZ)
        tar_files(data_path, output)
        return output

    def _create_checksum(self, source_file):
        ''' creates a md5 checksum file for `source_file`. '''
        checksum_value = self.hasher.get_file_hash(source_file)
        return FileUtil.create_checksum_file(source_file, checksum_value)
