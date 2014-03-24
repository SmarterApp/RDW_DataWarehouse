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


#CR Use cron instead of sleep

class ConductorController(threading.Thread):
    def __init__(self, connection, slave_find_wait=5, run_interval=300):
        threading.Thread.__init__(self)
        self.__connection = connection
        self.__slave_find_wait = slave_find_wait
        self.__run_interval = run_interval
        self.__slave_tracker = SlaveTracker()
        self.__conductor = Conductor()

    def run(self):
        while True:
            self.process(slave_find_wait=self.__slave_find_wait)
            time.sleep(self.__run_interval)

    def __reset_all(self):
        self.__slave_tracker.reset()
        self.__conductor.reset_slaves()

    def process(self, slave_find_wait=5):
        self.__reset_all()
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
            logger.debug('regular_process: 1 of 16')
            self.__conductor.grouping_slaves()
            logger.debug('regular_process: 2 of 16')
            self.__conductor.send_disconnect_PGPool(slave_group=Constants.PLAYER_GROUP_A)
            logger.debug('regular_process: 3 of 16')
            self.__conductor.wait_PGPool_disconnected(slave_group=Constants.PLAYER_GROUP_A)
            logger.debug('regular_process: 4 of 16')
            self.__conductor.send_stop_replication(slave_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 5 of 16')
            self.__conductor.wait_replication_stopped(slave_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 6 of 16')
            self.__conductor.migrate()
            logger.debug('regular_process: 7 of 16')
            self.__conductor.monitor_replication_status(slave_group=Constants.PLAYER_GROUP_A)
            logger.debug('regular_process: 8 of 16')
            self.__conductor.send_connect_PGPool(slave_group=Constants.PLAYER_GROUP_A)
            logger.debug('regular_process: 9 of 16')
            self.__conductor.wait_PGPool_connected(slave_group=Constants.PLAYER_GROUP_A)
            logger.debug('regular_process: 10 of 16')
            self.__conductor.send_disconnect_PGPool(slave_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 11 of 16')
            self.__conductor.wait_PGPool_disconnected(slave_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 12 of 16')
            self.__conductor.send_start_replication(slave_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 13 of 16')
            self.__conductor.wait_replication_started(slave_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 14 of 16')
            self.__conductor.monitor_replication_status(slave_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 15 of 16')
            self.__conductor.send_connect_PGPool(slave_group=Constants.PLAYER_GROUP_B)
            logger.debug('regular_process: 16 of 16')
            self.__conductor.wait_PGPool_connected(slave_group=Constants.PLAYER_GROUP_B)
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
