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
    '''
    Consume messages from slaves
    '''
    routing_key = Constants.CONDUCTOR_ROUTING_KEY
    exchange = Exchange(Constants.CONDUCTOR_EXCHANGE, type='direct')

    queue = Queue('edmigrate_conductor', exchange=exchange, routing_key=routing_key, durable=False)

    def __init__(self, connection):
        self.connection = connection
        self.__slave_tracker = SlaveTracker()
        self.__CONSUMER_COMMAND_HANDLERS = {
            Constants.ACK_COMMAND_FIND_SLAVE: self.__slave_tracker.add_slave,
            Constants.ACK_COMMAND_START_REPLICATION: self.__slave_tracker.set_replication_started,
            Constants.ACK_COMMAND_CONNECT_PGPOOL: self.__slave_tracker.set_pgpool_connected,
            Constants.ACK_COMMAND_STOP_REPLICATION: self.__slave_tracker.set_replication_stopped,
            Constants.ACK_COMMAND_DISCONNECT_PGPOOL: self.__slave_tracker.set_pgpool_disconnected
        }

    def get_consumers(self, Consumer, channel):
        consumer = Consumer(self.queue, callbacks=[self.on_message])
        consumer.purge()
        return [consumer]

    def on_message(self, body, message):
        message_ack_command = body[Constants.MESSAGE_ACK_COMMAND]
        node_id = body[Constants.MESSAGE_NODE_ID]
        logger.debug('Message Received from node_id[' + str(node_id) + '] message[' + message_ack_command + ']')
        try:
            function = self.__CONSUMER_COMMAND_HANDLERS.get(message_ack_command)
            if function:
                function(node_id)
            else:
                logger.debug('No handler for message[' + message_ack_command + '] from node_id[' + str(node_id) + ']')
        except SlaveNotRegisteredException as e:
            logger.error(e)
        finally:
            message.ack()
