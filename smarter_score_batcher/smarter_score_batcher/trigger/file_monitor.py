import os
import shutil
import logging
from os import path
from edcore.watch.util import FileUtil
from edcore.utils.utils import tar_files
from edcore.utils.utils import run_cron_job
from edcore.utils.data_archiver import encrypt_file
from smarter_score_batcher.utils.file_lock import FileLock


logger = logging.getLogger("smarter_score_batcher")


class Extensions:

    TAR = ".tar"
    CSV = ".csv"
    GPG = ".gpg"
    JSON = ".json"
    PARTIAL = ".partial"


def move_to_staging(settings):
    working_dir = settings['smarter_score_batcher.base_dir.working']
    staging_dir = settings['smarter_score_batcher.base_dir.staging']
    assessments = list_assessments(working_dir)
    for assessment in assessments:
        with FileEncryption(assessment) as fl:
            # encrypt tar file
            gpg_file_path = fl.encrypt(settings)
            fl.move_files(gpg_file_path, staging_dir)
        # do housekeeping afterwards
        _clean_up(assessment)


def _clean_up(dir_path):
    try:
        os.removedirs(dir_path)
    except OSError:
        logger.warning("OSError occurs while attempting to remove %s", dir_path)


def list_assessments(workspace):
    '''Return list of csv file names under workspace that appear in pair of
    JSON and CSV format.
    '''
    def _valid_name(name):
        return name and not path.islink(name) and not name.startswith(".")

    files = set()
    for dir_name in os.listdir(workspace):
        if not _valid_name(dir_name):
            continue
        full_path = path.join(workspace, dir_name)
        files.add(full_path)
    return files


def run_cron_sync_file(settings):
    ''' Configure and run cron job to copy csv files to UDL landing zone for.

    :param dict settings:  configuration for the application
    '''
    run_cron_job(settings, 'trigger.assessment.', move_to_staging)


class FileEncryption(FileLock):

    def __init__(self, dir_name):
        self.assessment_dir = dir_name
        self.assessment_id = path.split(dir_name)[1]
        self.lock_file = path.join(self.assessment_dir, self.assessment_id + Extensions.CSV)
        if not path.isfile(self.lock_file):
            # TODO: need to handle exception properly if lock file doesn't exist for some reason
            raise FileNotFoundError()
        super().__init__(self.lock_file)

    def move_files(self, src_file, dst_dir):
        # TODO: create checksum
        # FileUtil.create_checksum_file()
        dst_file = path.join(dst_dir, path.basename(src_file))
        # add .partial extension to avoid rsync copying incomplete file
        tmp_file = dst_file + Extensions.PARTIAL
        shutil.copy(src_file, tmp_file)
        # remove partial extension
        shutil.move(tmp_file, dst_file)

    def encrypt(self, settings):
        # move JSON and CSV file to temporary directory
        data_path = self._move_to_tempdir()
        tar_file = self._compress(data_path)
        gpg_file = path.join(self.temp_dir, tar_file + Extensions.GPG)
        # gpg settings
        recipients = settings.get('smarter_score_batcher.gpg.public_key.cat', None)
        homedir = settings.get('smarter_score_batcher.gpg.homedir', None)
        keyserver = settings.get('smarter_score_batcher.gpg.keyserver', None)
        gpg_binary_file = settings.get('smarter_score_batcher.gpg.path', None)
        with open(tar_file, 'rb') as file:
            encrypt_file(file, recipients, gpg_file, homedir=homedir, keyserver=keyserver, gpgbinary=gpg_binary_file)
        return gpg_file

    def __enter__(self):
        lock = super().__enter__()
        self.temp_dir = path.join(self.assessment_dir, ".tmp")
        if not path.exists(self.temp_dir):
            os.mkdir(self.temp_dir)
        return lock

    def __exit__(self, type, value, tb):
        shutil.rmtree(self.temp_dir)
        super().__exit__(type, value, tb)

    def _move_to_tempdir(self):

        def _valid_file(file):
            if not path.isfile(file):
                return False
            return file.endswith(Extensions.CSV) or file.endswith(Extensions.JSON)

        # create a directory with name `assessment id` under .tmp
        target_dir = path.join(self.temp_dir, self.assessment_id)
        if not path.exists(target_dir):
            os.mkdir(target_dir)
        # copy JSON and CSV files over
        for file in os.listdir(self.assessment_dir):
            src_file = path.join(self.assessment_dir, file)
            if _valid_file(src_file):
                shutil.move(src_file, target_dir)
        return target_dir

    def _compress(self, data_path):
        ''' compress JSON and CSV file into tar which have the same assessment id.'''
        output = path.join(self.temp_dir, data_path + Extensions.TAR)
        tar_files(data_path, output)
        return output

    def create_file_hash(self):
        raise NotImplementedError()
