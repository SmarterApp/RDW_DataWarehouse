import os
import tempfile
import shutil
from os import path
from edcore.utils.utils import archive_files
from edcore.utils.utils import run_cron_job
from edcore.utils.data_archiver import encrypted_archive_files, GPGPublicKeyException
from smarter_score_batcher.utils.file_lock import FileLock


class Extensions:

    TAR = ".tar"
    CSV = ".csv"
    GPG = ".gpg"
    JSON = ".json"


def copy_files(settings):
    # TODO: update to real base dir
    root_dir = settings['smarter_score_batcher.base_dir']
    # lock csv files
    dir_names = list_assessment_files(root_dir)
    for dir_name in dir_names:
        with FileEncryption(root_dir, dir_name) as fl:
            # compress CSV and JSON file
            fl.compress()
            # encrypt tar file
            fl.encrypt(settings)
            fl.create_file_hash()
            fl.move_to_staging()


def list_assessment_files(base_dir):
    '''Return list of csv file names under base_dir that appear in pair of
    JSON and CSV format.
    '''
    return set([dir_name for dir_name in os.listdir(base_dir)])


def run_cron_sync_file(settings):
    '''
    Configure and run cron job to copy csv files to UDL landing zone for.

     :param dict settings:  configuration for the application
    '''
    run_cron_job(settings, 'trigger.assessment.', copy_files)


class FileEncryption(FileLock):

    def __init__(self, root_dir, dir_name):
        self.dir_name = dir_name
        self.path_to_dir = path.join(root_dir, dir_name)
        # TODO: lock csv file
        self.lock_file = path.join(self.path_to_dir, dir_name + ".csv")
        super().__init__(self.lock_file)

    def __enter__(self):
        lock = super().__enter__()
        self.temp_dir = tempfile.mkdtemp()
        return lock

    def __exit__(self, type, value, tb):
        shutil.rmtree(self.temp_dir)
        super().__exit__(type, value, tb)

    def compress(self):
        ''' compress JSON and CSV file into tar which have the same assessment id.'''
        archive_file_name = path.join(self.temp_dir, self.dir_name + Extensions.TAR)
        archive_files(self.path_to_dir, archive_file_name)
        return archive_file_name

    def move_to_staging(self):
        raise NotImplementedError()

    def encrypt(self, settings):
        # TODO: where to get recipients
        recipients = settings.get('extract.gpg.public_key.cat', None)
        keyserver = settings.get('extract.gpg.keyserver', None)
        gpg_binary_file = settings.get('extract.gpg.path', None)
        homedir = settings.get('extract.gpg.homedir', None)
        outputfile = path.join(self.temp_dir, self.dir_name + Extensions.TAR + Extensions.GPG)
        encrypted_archive_files(self.path_to_dir, recipients, outputfile, homedir, keyserver, gpg_binary_file)
        return outputfile

    def create_file_hash(self):
        raise NotImplementedError()
