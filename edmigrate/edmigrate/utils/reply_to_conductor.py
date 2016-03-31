# (c) 2014 Amplify Education, Inc. All rights reserved, subject to the license
# below.
#
# Education agencies that are members of the Smarter Balanced Assessment
# Consortium as of August 1, 2014 are granted a worldwide, non-exclusive, fully
# paid-up, royalty-free, perpetual license, to access, use, execute, reproduce,
# display, distribute, perform and create derivative works of the software
# included in the Reporting Platform, including the source code to such software.
# This license includes the right to grant sublicenses by such consortium members
# to third party vendors solely for the purpose of performing services on behalf
# of such consortium member educational agencies.

'''
Created on Mar 13, 2014

@author: tosako
'''
import logging
logger = logging.getLogger('edmigrate')
from edmigrate.utils.constants import Constants
from kombu import Producer


def register_player(node_id, connection, exchange, routing_key):
    return __send_message_to_conductor(node_id, Constants.ACK_COMMAND_FIND_PLAYER, connection, exchange, routing_key)


def acknowledgement_pgpool_disconnected(node_id, connection, exchange, routing_key):
    return __send_message_to_conductor(node_id, Constants.ACK_COMMAND_DISCONNECT_PGPOOL, connection, exchange, routing_key)


def acknowledgement_pgpool_connected(node_id, connection, exchange, routing_key):
    return __send_message_to_conductor(node_id, Constants.ACK_COMMAND_CONNECT_PGPOOL, connection, exchange, routing_key)


def acknowledgement_master_disconnected(node_id, connection, exchange, routing_key):
    return __send_message_to_conductor(node_id, Constants.ACK_COMMAND_STOP_REPLICATION, connection, exchange, routing_key)


def acknowledgement_master_connected(node_id, connection, exchange, routing_key):
    return __send_message_to_conductor(node_id, Constants.ACK_COMMAND_START_REPLICATION, connection, exchange, routing_key)


def acknowledgement_reset_players(node_id, connection, exchange, routing_key):
    return __send_message_to_conductor(node_id, Constants.ACK_COMMAND_RESET_PLAYERS, connection, exchange, routing_key)


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
