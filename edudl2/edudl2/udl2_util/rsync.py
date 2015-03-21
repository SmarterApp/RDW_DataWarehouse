'''
Created on Aug 14, 2014

@author: tosako
'''
import subprocess
import logging
import tempfile
import os
import shutil
from edcore.utils.aws import s3_backup


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
        s3_bucket = settings.get('file-grabber.args.archive_S3_bucket')
        private_key = settings.get('file-grabber.args.private_key')
        backup_of_backup_tmp_dir = os.path.join(tempfile.gettempdir(), 's3_backup')
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
            backup_filenames = []
            for dirpath, dirs, files in os.walk(tmp):
                for filename in files:
                    fname = os.path.abspath(os.path.join(dirpath, filename))
                    backup_filenames.append(fname)
                    dest_path = os.path.join(landing, dirpath)
                    os.makedirs(dest_path, mode=0o760, exist_ok=True)
                    shutil.copy2(fname, dest_path)
            try:
                saved = s3_backup(s3_bucket, tmp, backup_filenames)
                if saved:
                    # Empty list.
                    del backup_filenames[:]
                    leftover_backupfiles = []
                    for dirpath, dirs, files in os.walk(backup_of_backup_tmp_dir):
                        fname = os.path.abspath(os.path.join(dirpath, filename))
                        leftover_backupfiles.append(fname)
                    saved_again = s3_backup(s3_bucket, backup_of_backup_tmp_dir, leftover_backupfiles)
                    if saved_again:
                        shutil.rmtree(backup_of_backup_tmp_dir)
            except:
                # backup has an issue.  save somewhere else.
                if backup_filenames:
                    if not os.path.exists(backup_of_backup_tmp_dir):
                        os.makedirs(backup_of_backup_tmp_dir, mode=0o760, exist_ok=True)
                    for file in backup_filenames:
                        shutil.copy2(file, backup_of_backup_tmp_dir)
