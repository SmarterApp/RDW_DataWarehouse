'''
Created on Mar 13, 2014

@author: tosako
'''
from kombu.mixins import ConsumerMixin
from kombu.entity import Queue, Exchange
from kombu.connection import BrokerConnection
from edmigrate.utils.constants import Constants
from edmigrate.utils.slave_tracker import SlaveTracker


class Consumer(ConsumerMixin):
    exchange = Exchange('edmigrate_conductor', type='direct')
    queue = Queue('edmigrate_conductor', exchange, routing_key='edmigrate.conductor')

    def __init__(self, connection):
        self.connection = connection
        self.__slave_tracker = SlaveTracker()

    def get_consumers(self, Consumer, channel):
        return [Consumer(self.queue, callbacks=[self.on_message])]

    def on_message(self, body, message):
        message_ack_command = body[Constants.MESSAGE_ACK_COMMAND]
        node_id = body[Constants.MESSAGE_NODE_ID]
        if message_ack_command == Constants.ACK_COMMAND_FIND_SLAVE:
            self.__slave_tracker.add_slave(node_id)
        elif message_ack_command == Constants.ACK_COMMAND_CONNECT_MASTER:
            self.__slave_tracker.set_master_connected(node_id)
        elif message_ack_command == Constants.ACK_COMMAND_CONNECT_PGPOOL:
            self.__slave_tracker.set_pgpool_connected(node_id)
        elif message_ack_command == Constants.ACK_COMMAND_DISCONNECT_MASTER:
            self.__slave_tracker.set_master_disconnected(node_id)
        elif message_ack_command == Constants.ACK_COMMAND_DISCONNECT_PGPOOL:
            self.__slave_tracker.set_pgpool_disconnected(node_id)
        print("received body: %r" % (body))
        print("received message: %r" % (message))
        message.ack()

if __name__ == "__main__":
    with BrokerConnection("amqp://guest:guest@localhost:5672") as connection:
        try:
            Consumer(connection).run()
        except KeyboardInterrupt:
            print('bye!')
