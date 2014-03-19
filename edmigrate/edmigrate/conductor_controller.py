'''
Created on Mar 17, 2014

@author: tosako
'''
import threading
from edmigrate.utils.slave_tracker import SlaveTracker
from edmigrate.utils.conductor import Conductor
import time
import logging
from edmigrate.utils.constants import Constants
from edmigrate.exceptions import EdMigrateException


logger = logging.getLogger('edmigrate')


class ConductorController(threading.Thread):
    def __init__(self, connection, slave_find_wait=5, interval=300):
        threading.Thread.__init__(self)
        self.__connection = connection
        self.__slave_find_wait = slave_find_wait
        self.__interval = interval
        self.__slave_tracker = SlaveTracker()
        self.__conductor = Conductor()

    def run(self):
        while True:
            self.process(slave_find_wait=self.__slave_find_wait)
            time.sleep(self.__interval)

    def process(self, slave_find_wait=5):
        self.__slave_tracker.reset()
        self.__conductor.reset_slaves()
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
        logger.debug('Starting regular slave migration process')
        try:
            logger.debug('regular_process: 1')
            self.__conductor.grouping_slaves()
            logger.debug('regular_process: 2')
            self.__conductor.send_disconnect_PGPool(slave_group=Constants.SLAVE_GROUP_A)
            logger.debug('regular_process: 3')
            self.__conductor.wait_PGPool_disconnected(slave_group=Constants.SLAVE_GROUP_A)
            logger.debug('regular_process: 4')
            self.__conductor.send_disconnect_master(slave_group=Constants.SLAVE_GROUP_B)
            logger.debug('regular_process: 5')
            self.__conductor.wait_master_disconnected(slave_group=Constants.SLAVE_GROUP_B)
            logger.debug('regular_process: 6')
            self.__conductor.migrate()
            logger.debug('regular_process: 7')
            self.__conductor.monitor_replication_status(slave_group=Constants.SLAVE_GROUP_A)
            logger.debug('regular_process: 8')
            self.__conductor.send_connect_PGPool(slave_group=Constants.SLAVE_GROUP_A)
            logger.debug('regular_process: 9')
            self.__conductor.wait_PGPool_connected(slave_group=Constants.SLAVE_GROUP_A)
            logger.debug('regular_process: 10')
            self.__conductor.send_disconnect_PGPool(slave_group=Constants.SLAVE_GROUP_B)
            logger.debug('regular_process: 11')
            self.__conductor.wait_PGPool_disconnected(slave_group=Constants.SLAVE_GROUP_B)
            logger.debug('regular_process: 12')
            self.__conductor.send_connect_master(slave_group=Constants.SLAVE_GROUP_B)
            logger.debug('regular_process: 13')
            self.__conductor.wait_master_connected(slave_group=Constants.SLAVE_GROUP_B)
            logger.debug('regular_process: 14')
            self.__conductor.monitor_replication_status(slave_group=Constants.SLAVE_GROUP_B)
            logger.debug('regular_process: 15')
            self.__conductor.send_connect_PGPool(slave_group=Constants.SLAVE_GROUP_B)
            logger.debug('regular_process: 16')
            self.__conductor.wait_PGPool_connected(slave_group=Constants.SLAVE_GROUP_B)
        except EdMigrateException as e:
            logger.info(e)
        logger.debug('End of regular slave migration process')

    def single_slave_process(self):
        logger.debug('Starting single slave migration process')
        try:
            self.__conductor.migrate()
            self.__conductor.monitor_replication_status()
        except EdMigrateException as e:
            logger.info(e)
        logger.debug('End of single slave migration process')
