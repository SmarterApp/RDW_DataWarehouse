'''
Created on Mar 13, 2014

@author: tosako
'''
from edmigrate.utils.constants import Constants
from kombu import Producer
import logging


logger = logging.getLogger('edmigrate')


def register_slave(node_id, connection, exchange, routing_key):
    return __send_message_to_conductor(node_id, Constants.ACK_COMMAND_FIND_SLAVE, connection, exchange, routing_key)


def acknowledgement_pgpool_disconnected(node_id, connection, exchange, routing_key):
    return __send_message_to_conductor(node_id, Constants.ACK_COMMAND_DISCONNECT_PGPOOL, connection, exchange, routing_key)


def acknowledgement_pgpool_connected(node_id, connection, exchange, routing_key):
    return __send_message_to_conductor(node_id, Constants.ACK_COMMAND_CONNECT_PGPOOL, connection, exchange, routing_key)


def acknowledgement_master_disconnected(node_id, connection, exchange, routing_key):
    return __send_message_to_conductor(node_id, Constants.ACK_COMMAND_DISCONNECT_MASTER, connection, exchange, routing_key)


def acknowledgement_master_connected(node_id, connection, exchange, routing_key):
    return __send_message_to_conductor(node_id, Constants.ACK_COMMAND_CONNECT_MASTER, connection, exchange, routing_key)


def acknowledgement_reset_slaves(node_id, connection, exchange, routing_key):
    return __send_message_to_conductor(node_id, Constants.ACK_COMMAND_RESET_SLAVES, connection, exchange, routing_key)


def __send_message_to_conductor(node_id, command, connection, exchange, routing_key):
    '''
    return should be None unless you are Unit Testing with Connection which uses Mock Transport
    '''
    message = {}
    message[Constants.MESSAGE_NODE_ID] = node_id
    message[Constants.MESSAGE_ACK_COMMAND] = command
    logger.debug('Publishing Message to routing_key[' + routing_key + '] command[' + command + ']')
    producer = Producer(connection, serializer='json')
    return producer.publish(message, exchange=exchange, routing_key=routing_key)
