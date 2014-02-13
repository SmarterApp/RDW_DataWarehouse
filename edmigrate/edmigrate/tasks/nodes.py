__author__ = 'sravi'

from edmigrate.celery import celery, logger
from edmigrate.utils.constants import Constants

# format {Key1: [list], Key2: [list]}
# Eg: {'A' : [1,3], 'B' : [2,4]}
registered_slaves = {}


def get_registered_slave_nodes_for_group(group):
    '''
    return slave nodes for the given group if group exists else None
    '''
    if group not in registered_slaves.keys():
        return None
    return list(registered_slaves[group])


def get_all_registered_slave_nodes():
    '''
    returns all registered slave nodes as a list
    '''
    all_nodes = []
    for group in registered_slaves.keys():
        all_nodes.extend(registered_slaves[group])
    return all_nodes


@celery.task(name='task.edmigrate.nodes.register_node')
def register_slave_node(host, group):
    '''
    register a slave node based on host and group info
    '''
    logger.info("Registering host %s group %s to master" % (host, group))
    if group not in registered_slaves.keys():
        registered_slaves[group] = set()
    registered_slaves[group].add(host)
