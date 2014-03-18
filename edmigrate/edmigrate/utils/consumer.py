'''
Created on Mar 13, 2014

@author: tosako
'''
from kombu.mixins import ConsumerMixin
from kombu.entity import Queue, Exchange
from edmigrate.utils.constants import Constants
from edmigrate.utils.slave_tracker import SlaveTracker
import threading
import logging
from edmigrate.exceptions import SlaveNotRegisteredException

logger = logging.getLogger('edmigrate')


class ConsumerThread(threading.Thread):
    def __init__(self, connection):
        super().__init__()
        self.__connection = connection
        self.__consumer = Consumer(self.__connection)

    def run(self):
        self.__consumer.run()

    def stop(self):
        self.__consumer.should_stop = True


class Consumer(ConsumerMixin):
    routing_key = Constants.CONDUCTOR_ROUTING_KEY
    exchange = Exchange(Constants.CONDUCTOR_EXCHANGE, type='direct')
    queue = Queue('edmigrate_conductor', exchange, routing_key=routing_key)

    def __init__(self, connection):
        self.connection = connection
        self.__slave_tracker = SlaveTracker()

    def get_consumers(self, Consumer, channel):
        return [Consumer(self.queue, callbacks=[self.on_message])]

    def on_message(self, body, message):
        message_ack_command = body[Constants.MESSAGE_ACK_COMMAND]
        node_id = body[Constants.MESSAGE_NODE_ID]
        logger.debug('Message Received from node_id[' + str(node_id) + ' message[' + message_ack_command + ']')
        # print("on_mesage " + str(node_id)+" msg " + message_ack_command)
        try:
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
        except SlaveNotRegisteredException as e:
            logger.error(e)
        message.ack()

# if __name__ == "__main__":
#    with BrokerConnection("amqp://guest:guest@localhost:5672") as connection:
#        try:
#            Consumer(connection).run()
#        except KeyboardInterrupt:
#            print('bye!')
