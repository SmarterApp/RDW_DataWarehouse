'''
Created on Aug 14, 2014

@author: tosako
'''
import subprocess
import logging


logger = logging.getLogger('edudl2')


def rsync(*args, **kwargs):
    '''
    executing rsync command
    '''
    settings = args[0]
    rsync_command = ['rsync', '-rltzu', '--exclude', '*.partial', '--remove-source-files']
    remote_user = settings.get('file-grabber.args.remote_user')
    remote_host = settings.get('file-grabber.args.remote_host')
    remote_dir = settings.get('file-grabber.args.remote_dir')
    landing = settings.get('file-grabber.args.landing')
    private_key = settings.get('file-grabber.args.private_key')
    if private_key is not None:
        rsync_command.append("-e")
        rsync_command.append("ssh -i " + private_key)

    if not remote_dir.endswith('/'):
        remote_dir += '/'
    if not landing.endswith('/'):
        landing += '/'
    rsync_command.append(remote_user + '@' + remote_host + ':' + remote_dir)
    rsync_command.append(landing)
    returncode = subprocess.call(rsync_command)
    if returncode is not 0:
        logger.error('failed rsync. return code: ' + str(returncode))
