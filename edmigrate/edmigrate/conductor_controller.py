'''
Created on Mar 17, 2014

@author: tosako
'''
import threading
from edmigrate.utils.consumer import ConsumerThread
from edmigrate.utils.slave_tracker import SlaveTracker
from edmigrate.utils.conductor import Conductor
import time
import logging
from edmigrate.utils.constants import Constants


logger = logging.getLogger('edmigrate')


class ConductorController(threading.Thread):
    def __init__(self, connection):
        self.__connenctor = connection
        self.__thread = ConsumerThread(self.__connection)
        self.__thread.start()
        self.__slave_tracker = SlaveTracker()
        self.__slave_tracker.reset()
        self.__conductor = Conductor()

    def start(self, slave_find_wait=5):
        self.__conductor.find_slaves()
        time.sleep(slave_find_wait)
        slaves_ids = self.__slave_tracker.get_slave_ids()
        if slaves_ids:
            number_of_slaves = len(slaves_ids)
            if number_of_slaves == 1:
                self.single_slave_process()
            else:
                self.regular_process()
        else:
            logger.info('No slave was detected')

    def regular_process(self):
        self.__conductor.grouping_slaves()
        self.__conductor.send_disconnect_PGPool(slave_group=Constants.SLAVE_GROUP_A)
        self.__conductor.wait_PGPool_disconnected(slave_group=Constants.SLAVE_GROUP_A)
        self.__conductor.send_disconnect_master(slave_group=Constants.SLAVE_GROUP_B)
        self.__conductor.wait_master_disconnected(slave_group=Constants.SLAVE_GROUP_B)
        self.__conductor.migrate()
        self.__conductor.monitor_replication_status(slave_group=Constants.SLAVE_GROUP_A)
        self.__conductor.send_connect_PGPool(slave_group=Constants.SLAVE_GROUP_A)
        self.__conductor.wait_PGPool_connected(slave_group=Constants.SLAVE_GROUP_A)
        self.__conductor.send_disconnect_PGPool(slave_group=Constants.SLAVE_GROUP_B)
        self.__conductor.wait_PGPool_disconnected(slave_group=Constants.SLAVE_GROUP_B)
        self.__conductor.send_connect_master(slave_group=Constants.SLAVE_GROUP_B)
        self.__conductor.wait_master_connected(slave_group=Constants.SLAVE_GROUP_B)
        self.__conductor.monitor_replication_status(slave_group=Constants.SLAVE_GROUP_B)
        self.__conductor.send_connect_PGPool(slave_group=Constants.SLAVE_GROUP_B)
        self.__conductor.wait_master_connected(slave_group=Constants.SLAVE_GROUP_B)

    def single_slave_process(self):
        self.__conductor.migrate()
        self.__conductor.monitor_replication_status()
