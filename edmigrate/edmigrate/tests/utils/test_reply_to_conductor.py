'''
Created on Mar 16, 2014

@author: tosako
'''
import unittest
from kombu import Connection
from kombu.entity import Exchange, Queue
from edmigrate.utils.reply_to_conductor import register_slave,\
    acknowledgement_pgpool_disconnected, acknowledgement_pgpool_connected,\
    acknowledgement_master_disconnected, acknowledgement_master_connected
from kombu.tests.mocks import Transport
from edmigrate.utils.constants import Constants
import json


class Test(unittest.TestCase):

    def setUp(self):
        self.__conn = Connection(transport=Transport)
        self.__conn.connect()
        self.__exchange = Exchange('test_exchange')
        self.__routing_key = 'test.routing'
        self.__queue = Queue('test_queue', self.__exchange, routing_key=self.__routing_key)

    def test_register_slave(self):
        message, exchange, routing_key = register_slave(111, self.__conn, self.__exchange, self.__routing_key)
        body = json.loads(message['body'])
        self.assertEqual(Constants.ACK_COMMAND_FIND_SLAVE, body[Constants.MESSAGE_ACK_COMMAND])
        self.assertEqual(111, body[Constants.MESSAGE_NODE_ID])
        self.assertEqual(self.__exchange.name, exchange)
        self.assertEqual(self.__routing_key, routing_key)

    def test_acknowledgement_pgpool_disconnected(self):
        message, exchange, routing_key = acknowledgement_pgpool_disconnected(111, self.__conn, self.__exchange, self.__routing_key)
        body = json.loads(message['body'])
        self.assertEqual(Constants.ACK_COMMAND_DISCONNECT_PGPOOL, body[Constants.MESSAGE_ACK_COMMAND])
        self.assertEqual(111, body[Constants.MESSAGE_NODE_ID])
        self.assertEqual(self.__exchange.name, exchange)
        self.assertEqual(self.__routing_key, routing_key)

    def test_acknowledgement_pgpool_connected(self):
        message, exchange, routing_key = acknowledgement_pgpool_connected(111, self.__conn, self.__exchange, self.__routing_key)
        body = json.loads(message['body'])
        self.assertEqual(Constants.ACK_COMMAND_CONNECT_PGPOOL, body[Constants.MESSAGE_ACK_COMMAND])
        self.assertEqual(111, body[Constants.MESSAGE_NODE_ID])
        self.assertEqual(self.__exchange.name, exchange)
        self.assertEqual(self.__routing_key, routing_key)

    def test_acknowledgement_master_disconnected(self):
        message, exchange, routing_key = acknowledgement_master_disconnected(111, self.__conn, self.__exchange, self.__routing_key)
        body = json.loads(message['body'])
        self.assertEqual(Constants.ACK_COMMAND_DISCONNECT_MASTER, body[Constants.MESSAGE_ACK_COMMAND])
        self.assertEqual(111, body[Constants.MESSAGE_NODE_ID])
        self.assertEqual(self.__exchange.name, exchange)
        self.assertEqual(self.__routing_key, routing_key)

    def test_acknowledgement_master_connected(self):
        message, exchange, routing_key = acknowledgement_master_connected(111, self.__conn, self.__exchange, self.__routing_key)
        body = json.loads(message['body'])
        self.assertEqual(Constants.ACK_COMMAND_CONNECT_MASTER, body[Constants.MESSAGE_ACK_COMMAND])
        self.assertEqual(111, body[Constants.MESSAGE_NODE_ID])
        self.assertEqual(self.__exchange.name, exchange)
        self.assertEqual(self.__routing_key, routing_key)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
