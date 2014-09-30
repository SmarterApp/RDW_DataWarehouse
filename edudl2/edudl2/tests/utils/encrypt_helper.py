import os
import uuid
import tempfile
import shutil
from edcore.utils.data_archiver import encrypt_file
from edcore.utils.utils import tar_files
from edcore.watch.util import FileUtil
from edcore.watch.file_hasher import MD5Hasher


def _get_gpg_settings_by_tenant(settings):
    ''' fetches gpg encryption settings. '''
    recipients = 'sbac_data_provider@sbac.com'
    homedir = settings.get('gpg_home', None)
    if homedir:
        homedir = os.path.expanduser(homedir)
    kw_settings = {
        "homedir": homedir,
        "gpgbinary": 'gpg',
        "passphrase": settings.get('passphrase', None),
        "sign": 'ca_user@ca.com'
    }
    return recipients, kw_settings


class EncryptHelper():

    def __init__(self, settings):
        self.settings = settings
        self.temp_dir = tempfile.mkdtemp()
        self.hasher = MD5Hasher()

    def compress_directory(self, dir_path):
        # create tmp directory
        tar_file_name = self._get_tar_file_name()
        tar_files(dir_path, tar_file_name)
        return tar_file_name

    def encrypt(self, tar_file):
        # move JSON and CSV file to temporary directory
        gpg_file = os.path.join(self.temp_dir, tar_file + '.gpg')
        # get settings for encryption function
        recipients, kwargs = _get_gpg_settings_by_tenant(self.settings)
        with open(tar_file, 'rb') as file:
            encrypt_file(file, recipients, gpg_file, **kwargs)
        return gpg_file

    def _get_tar_file_name(self):
        filename = str(uuid.uuid4())
        return os.path.join(self.temp_dir, filename + '.tar')

    def create_checksum(self, source_file):
        ''' creates a md5 checksum file for `source_file`. '''
        checksum_value = self.hasher.get_file_hash(source_file)
        return FileUtil.create_checksum_file(source_file, checksum_value)

    def create_gpg(self, dir_path):
        tar_file = self.compress_directory(dir_path)
        encrypted_file = self.encrypt(tar_file)
        return encrypted_file

    def create_gpg_and_checksum(self, dir_path):
        encrypted_file = self.create_gpg(dir_path)
        checksum = self.create_checksum(encrypted_file)
        return (encrypted_file, checksum)

    def __del__(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
