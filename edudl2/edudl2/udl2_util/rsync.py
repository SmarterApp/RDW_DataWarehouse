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
    rsyc_command = ['rsync', '-rltzu', '--exclude', '*.partial', '--remove-source-files']
    remote_user = settings.get('udl2_rsync.args.remote_user')
    remote_host = settings.get('udl2_rsync.args.remote_host')
    remote_dir = settings.get('udl2_rsync.args.remote_dir')
    landing = settings.get('udl2_rsync.args.landing')
    private_key = settings.get('udl2_rsync.args.private_key')
    if private_key is not None:
        rsyc_command.append("-e")
        rsyc_command.append("ssh -i " + private_key)

    rsyc_command.append(remote_user + '@' + remote_host + ':' + remote_dir)
    rsyc_command.append(landing)
    returncode = subprocess.call(rsyc_command)
    if returncode is not 0:
        logger.error('failed rsync. return code: ' + str(returncode))
