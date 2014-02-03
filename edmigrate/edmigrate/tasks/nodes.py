__author__ = 'sravi'

import collections
from edmigrate.celery import celery
import logging

log = logging.getLogger('edmigrate')

Node = collections.namedtuple('Node', 'host group')
registered_slaves = set()


def get_slave_node_host_names_for_group(group, slaves):
    '''
    return all slave node hostnames belonging to group group
    '''
    return [slave.host for slave in slaves if slave.group == group]


def get_all_slave_node_host_names(slaves):
    '''
    return all slave node hostnames belonging to group group
    '''
    return [slave.host for slave in slaves]


def get_registered_slave_nodes():
    '''
    returns registered slave nodes in the format needed
    '''
    return registered_slaves


@celery.task(name='task.edmigrate.nodes.register_node')
def register_slave_node(host, group):
    '''
    register a slave node based on host and group info
    '''
    registered_slaves.add(Node(host=host, group=group))
