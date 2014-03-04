from edmigrate.tasks.base import BaseTask
__author__ = 'sravi'

from edmigrate.celery import celery, logger
from edmigrate.utils.constants import Constants

# format {Key1: [list], Key2: [list]}
# Eg: {'A' : [1,3], 'B' : [2,4]}
registered_slaves = {Constants.SLAVE_GROUP_A: [], Constants.SLAVE_GROUP_B: []}


def get_registered_slave_nodes_for_group(group):
    '''
    return slave nodes for the given group if group exists else None
    '''
    return registered_slaves.get(group)


def get_all_registered_slave_nodes():
    '''
    returns all registered slave nodes as a list
    '''
    all_nodes = []
    for group in registered_slaves.keys():
        all_nodes.extend(registered_slaves[group])
    return all_nodes


@celery.task(name='task.edmigrate.nodes.register_node', base=BaseTask)
def register_slave_node(host, group):
    '''
    register a slave node based on host and group info
    '''
    global registered_slaves
    logger.info("Registering host %s group %s to master" % (host, group))
    if group not in registered_slaves.keys():
        logger.error("Invalid group specified")
    else:
        known_slaves = registered_slaves[group]
        if host not in known_slaves:
            known_slaves.append(host)
