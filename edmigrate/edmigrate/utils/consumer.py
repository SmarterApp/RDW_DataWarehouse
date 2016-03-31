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
from kombu.mixins import ConsumerMixin
from edmigrate.utils.constants import Constants
from edmigrate.utils.player_tracker import PlayerTracker
import threading
import logging
from edmigrate.queues import conductor

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
    Consume messages from players
    '''

    def __init__(self, connection):
        self.connection = connection
        self.__player_tracker = PlayerTracker()
        self.__CONSUMER_COMMAND_HANDLERS = {
            Constants.ACK_COMMAND_FIND_PLAYER: self.__player_tracker.add_player,
            Constants.ACK_COMMAND_START_REPLICATION: self.__player_tracker.set_replication_started,
            Constants.ACK_COMMAND_CONNECT_PGPOOL: self.__player_tracker.set_pgpool_connected,
            Constants.ACK_COMMAND_STOP_REPLICATION: self.__player_tracker.set_replication_stopped,
            Constants.ACK_COMMAND_DISCONNECT_PGPOOL: self.__player_tracker.set_pgpool_disconnected
        }

    def get_consumers(self, Consumer, channel):
        consumer = Consumer(conductor.queue, callbacks=[self.on_message])
        consumer.purge()
        return [consumer]

    def on_message(self, body, message):
        try:
            message_ack_command = body[Constants.MESSAGE_ACK_COMMAND]
            node_id = body[Constants.MESSAGE_NODE_ID]
            logger.debug('Message Received from node_id[' + str(node_id) + '] message[' + message_ack_command + ']')
            function = self.__CONSUMER_COMMAND_HANDLERS.get(message_ack_command)
            if function:
                function(node_id)
            else:
                logger.debug('No handler for message[' + message_ack_command + '] from node_id[' + str(node_id) + ']')
        except Exception as e:
            logger.error(e)
        finally:
            message.ack()
