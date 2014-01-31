__author__ = 'sravi'

import collections
from edmigrate.celery_dev import celery

Node = collections.namedtuple('Node', 'host group')
print('Type of node:', type(Node))
registered_slaves = set()

# test data for now till we implement the registration for slave nodes
registered_slaves.add(Node(host='dbpgdwr0.qa.dum.edwdc.net', group='A'))
registered_slaves.add(Node(host='dbpgdwr0s1.qa.dum.edwdc.net', group='B'))
# end of test data


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


@celery.task(name='task.edmigrate.nodes.register_node')
def register_slave_node(host, group):
    '''
    register a slave node based on host and group info
    '''
    registered_slaves.add(Node(host=host, group=group))
