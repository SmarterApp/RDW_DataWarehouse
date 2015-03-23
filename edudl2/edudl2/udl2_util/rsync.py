'''
Created on Aug 14, 2014

@author: tosako
'''
import subprocess
import logging
import tempfile
import os
import shutil
from edudl2.udl2_util.file_archiver import archive_files


logger = logging.getLogger('edudl2')


def rsync(*args, **kwargs):
    '''
    executing rsync command
    '''
    with tempfile.TemporaryDirectory(prefix='file_grabber') as tmp:
        settings = args[0]
        rsync_command = ['rsync', '-rltzu', '--exclude', '*.partial', '--remove-source-files']
        remote_user = settings.get('file-grabber.args.remote_user')
        remote_host = settings.get('file-grabber.args.remote_host')
        remote_dir = settings.get('file-grabber.args.remote_dir')
        landing = settings.get('file-grabber.args.landing')
        s3_bucket = settings.get('file-grabber.args.archive_s3_bucket_name')
        s3_to_glacier_after_days = int(settings.get('file-grabber.args.archive_s3_to_glacier_after_days', '30'))
        private_key = settings.get('file-grabber.args.private_key')
        ssh_option = "ssh -o StrictHostKeyChecking=no"
        if private_key is not None:
            ssh_option += " -i " + private_key
        rsync_command.append("-e")
        rsync_command.append(ssh_option)

        if not remote_dir.endswith('/'):
            remote_dir += '/'
        if not landing.endswith('/'):
            landing += '/'
        rsync_command.append(remote_user + '@' + remote_host + ':' + remote_dir)
        rsync_command.append(tmp)
        returncode = subprocess.call(rsync_command)
        if returncode is not 0:
            logger.error('failed rsync. return code: ' + str(returncode))
        else:
            # copy from temporary directory to actual landing directory
            # using 2 steps copy because of archiving
            backup_of_backup_tmp_dir = os.path.join(tempfile.gettempdir(), 's3_backup')
            for dirpath, dirs, files in os.walk(tmp):
                for filename in files:
                    fname = os.path.abspath(os.path.join(dirpath, filename))
                    dest_path = os.path.join(landing, dirpath[len(tmp) + 1:])
                    os.makedirs(dest_path, mode=0o750, exist_ok=True)
                    shutil.copy2(fname, dest_path)
            archive_files(tmp, s3_bucket, s3_to_glacier_after_days, backup_of_backup=backup_of_backup_tmp_dir)
        archive_files(backup_of_backup_tmp_dir, s3_bucket, s3_to_glacier_after_days)
