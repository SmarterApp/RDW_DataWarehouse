'''
Created on Aug 14, 2014

@author: tosako
'''
import subprocess



def rsync(*args, **kwargs):
    '''
    executing rsync command
    '''
    settings = args[0]
    rsyc_command = ['rsync', '-az', '--exclude', '*.partial', '--remove-source-files']
    remote_user = settings.get('rsync.args.remote_user')
    remote_host = settings.get('rsync.args.remote_host')
    remote_dir = settings.get('rsync.args.remote_dir')
    landing = settings.get('rsync.args.landing')
    private_key = settings.get('rsync.args.private_key')
    if private_key is not None:
        rsyc_command.append("-e 'ssh -i " + private_key + "'")
    else:
        rsyc_command.append("-e 'ssh -i " + private_key + "'")

    rsyc_command.append(remote_user + '@' + remote_host + ':' + remote_dir)
    rsyc_command.append(landing)
    subprocess.call(rsyc_command)
