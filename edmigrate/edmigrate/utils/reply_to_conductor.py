'''
Created on Mar 13, 2014

@author: tosako
'''
from kombu.connection import Connection
from edmigrate.utils.constants import Constants
from kombu.entity import Exchange


def register_slave(node_id, url, exchange, routing_key):
    __send_message_to_conductor(node_id, Constants.ACK_COMMAND_FIND_SLAVE, url, exchange, routing_key)

def acknowledgement_pgpool_disconnected(node_id, url, exchange, routing_key):
    __send_message_to_conductor(node_id, Constants.ACK_COMMAND_DISCONNECT_PGPOOL, url, exchange, routing_key)

def acknowledgement_pgpool_connected(node_id, url, exchange, routing_key):
    __send_message_to_conductor(node_id, Constants.ACK_COMMAND_CONNECT_PGPOOL, url, exchange, routing_key)

def acknowledgement_master_disconnected(node_id, url, exchange, routing_key):
    __send_message_to_conductor(node_id, Constants.ACK_COMMAND_DISCONNECT_MASTER, url, exchange, routing_key)

def acknowledgement_master_connected(node_id, url, exchange, routing_key):
    __send_message_to_conductor(node_id, Constants.ACK_COMMAND_CONNECT_MASTER, url, exchange, routing_key)

def __send_message_to_conductor(node_id, command, url, exchange, routing_key):
    message = {}
    message[Constants.MESSAGE_NODE_ID]=node_id
    message[Constants.MESSAGE_ACK_COMMAND]=command
    with Connection(url) as conn:
        producer = conn.Producer(serializer='json')
        producer.publish(message, exchange=exchange, routing_key=routing_key)
        
if __name__ == '__main__':
    exchange = Exchange('edmigrate_conductor', type='direct')
    register_slave(123, 'amqp://guest:guest@localhost:5672', exchange, 'edmigrate.conductor')