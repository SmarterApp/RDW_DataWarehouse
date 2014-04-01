'''
Created on Mar 21, 2014

@author: ejen
'''
from edmigrate.queues import conductor
import logging
from edmigrate.utils.utils import get_broker_url, get_node_id_from_hostname, \
    get_my_master_by_id
from edmigrate.utils.constants import Constants
from edmigrate.settings.config import Config, get_setting
import edmigrate.utils.reply_to_conductor as reply_to_conductor
from kombu import Connection
import socket
from edmigrate.edmigrate_celery import celery
from edmigrate.utils.utils import Singleton
from edmigrate.utils.iptables import IptablesChecker, IptablesController


logger = logging.getLogger(Constants.WORKER_NAME),
admin_logger = logging.getLogger(Constants.EDMIGRATE_ADMIN_LOGGER)


class Player(metaclass=Singleton):
    def __init__(self,
                 connection=Connection(get_broker_url()),
                 exchange=conductor.exchange,
                 routing_key=Constants.CONDUCTOR_ROUTING_KEY):
        self.connection = connection
        self.exchange = exchange
        self.routing_key = routing_key
        self.COMMAND_HANDLERS = {
            Constants.COMMAND_REGISTER_PLAYER: self.register_player,
            Constants.COMMAND_START_REPLICATION: self.connect_master,
            Constants.COMMAND_STOP_REPLICATION: self.disconnect_master,
            Constants.COMMAND_CONNECT_PGPOOL: self.connect_pgpool,
            Constants.COMMAND_DISCONNECT_PGPOOL: self.disconnect_pgpool,
            Constants.COMMAND_RESET_PLAYERS: self.reset_players
        }
        self.hostname = socket.gethostname()
        self.node_id = get_node_id_from_hostname(self.hostname)
        self.master_hostname = get_my_master_by_id(self.node_id)

    def __enter__(self):
        return self

    def __exit__(self, _type, value, tb):
        pass

    def run_command(self, command, nodes):
        if command in self.COMMAND_HANDLERS:
            try:
                if nodes is None:
                    if command in [Constants.COMMAND_REGISTER_PLAYER, Constants.COMMAND_RESET_PLAYERS]:
                        self.COMMAND_HANDLERS[command]()
                        logger.debug("executed {command}".format(command=command))
                        admin_logger.debug("{name} at {hostname} with node id {node_id} executed {command} successfully".
                                           format(name=self.__class__.__name__, hostname=self.hostname,
                                                  node_id=self.node_id, command=command))
                    else:
                        logger.warning("{command} require nodes".format(command=command))
                        admin_logger.warning("{name} at {hostname} with node id {node_id} failed to execute {command} due to no nodes specified".
                                             format(name=self.__class__.__name__, hostname=self.hostname,
                                                    node_id=self.node_id, command=command))
                else:
                    if self.node_id in nodes:
                        self.COMMAND_HANDLERS[command]()
                        logger.info("{node_id} executed {command}".format(command=command, node_id=self.node_id))
                        admin_logger.info("{name} at {hostname} with node id {node_id} executed {command} {nodes} successfully".
                                          format(name=self.__class__.__name__, hostname=self.hostname,
                                                 node_id=self.node_id, command=command, nodes=str(nodes)))
                    else:
                        # ignore the command
                        logger.warning("{command} is ignored because {node_id} is not in {nodes}".
                                       format(command=command, node_id=self.node_id, nodes=str(nodes)))
                        admin_logger.warning("{name} at {hostname} with node id {node_id} ignored {command} {nodes}".
                                             format(name=self.__class__.__name__, hostname=self.hostname,
                                                    node_id=self.node_id, command=command, nodes=str(nodes)))
            except Exception as e:
                logger.error("error during executing {command}".format(command=command))
                admin_logger.error("error during executing {command}".format(command=command))
        else:
            logger.warning("{command} is not implemented".format(command=command))
            admin_logger.warning("{name} at {hostname} with node id {node_id} did not process {command} {nodes} due to command is not implemented".
                                 format(name=self.__class__.__name__, hostname=self.hostname,
                                        node_id=self.node_id, command=command, nodes=str(nodes)))

    def connect_pgpool(self):
        '''
        remove iptables rules to enable pgpool access slave database
        '''
        with IptablesController() as iptables:
            iptables.unblock_pgsql_INPUT()
            # localhost is not block by iptables, so we need to use the hostname to
            status = IptablesChecker().check_block_input(self.hostname)
            if status:
                reply_to_conductor.acknowledgement_pgpool_connected(self.node_id, self.connection,
                                                                    self.exchange, self.routing_key)
                logger.debug("Unblock pgpool")
                admin_logger.debug("{name} at {hostname} with node id {node_id} unblocked pgpool machine ( {pgpool}).".
                                   format(name=self.__class__.__name__, hostname=self.hostname, node_id=self.node_id))
            else:
                logger.error("Failed to unblock pgpool)")
                admin_logger.error("{name} at {hostname} with node id {node_id} failed to unblock pgpool machine ( {pgpool} ).".
                                   format(name=self.__class__.__name__, hostname=self.hostname, node_id=self.node_id))

    def disconnect_pgpool(self):
        '''
        insert iptables rules to block pgpool to access postgres db
        '''
        with IptablesController() as iptables:
            iptables.block_pgsql_INPUT()
            # localhost is not block by iptables, so we need to use the hostname to
            status = IptablesChecker().check_block_input(self.hostname)
            if status:
                reply_to_conductor.acknowledgement_pgpool_disconnected(self.node_id, self.connection,
                                                                       self.exchange, self.routing_key)
                logger.debug("Block pgpool")
                admin_logger.debug("{name} at {hostname} with node id {node_id} blocked pgpool machine.".
                                   format(name=self.__class__.__name__, hostname=self.hostname, node_id=self.node_id))
            else:
                logger.error("Failed to block pgpool")
                admin_logger.error("{name} at {hostname} with node id {node_id} failed to block pgpool machine.".
                                   format(name=self.__class__.__name__, hostname=self.hostname, node_id=self.node_id))

    def connect_master(self):
        '''
        remove iptable rules to unblock master from access slave database
        '''
        with IptablesController() as iptables:
            iptables.unblock_pgsql_OUTPUT()
            status = IptablesChecker().check_block_output(self.master_hostname)
            if status:
                reply_to_conductor.acknowledgement_master_connected(self.node_id, self.connection,
                                                                    self.exchange, self.routing_key)
                logger.debug("Unblock master database ( {master} )".format(master=self.master_hostname))
                admin_logger.debug("{name} at {hostname} with node id {node_id} unblocked master database ( {master}).".
                                   format(name=self.__class__.__name__, hostname=self.hostname,
                                          node_id=self.node_id, master=self.master_hostname))
            else:
                logger.error("Failed to unblock master ( {master} )".format(master=self.master_hostname))
                admin_logger.errro("{name} at {hostname} with node id {node_id} failed to unblock master database ( {master} ).".
                                   format(name=self.__class__.__name__, hostname=self.hostname,
                                          node_id=self.node_id, master=self.master_hostname))

    def disconnect_master(self):
        '''
        insert iptable rules to block master to access slave database
        '''
        with IptablesController() as iptables:
            iptables.block_pgsql_OUTPUT()
            status = IptablesChecker().check_block_output(self.master_hostname)
            if status:
                reply_to_conductor.acknowledgement_master_disconnected(self.node_id, self.connection,
                                                                       self.exchange, self.routing_key)
                logger.debug("Block master database ( {master} )".format(master=self.master_hostname))
                admin_logger.debug("{name} at {hostname} with node id {node_id} blocked master database ( {master}).".
                                   format(name=self.__class__.__name__, hostname=self._hostname(),
                                          node_id=self._node_id(), master=self.master_hostname))
            else:
                logger.error("{name}: Failed to block master( {master} )".format(master=self.master_hostname))
                admin_logger.error("{name} at {hostname} with node id {node_id} failed to block master database ( {master} ).".
                                   format(name=self.__class__.__name__, hostname=self._hostname(),
                                          node_id=self._node_id(), master=self.master_hostname))

    def reset_players(self):
        '''
        reset players. so it will not block pgpool and master database
        '''
        self.connect_pgpool()
        self.connect_master()

    def register_player(self):
        '''
        register player to conductor
        '''
        if self.node_id:
            reply_to_conductor.register_player(self.node_id, self.connection, self.exchange, self.routing_key)
            logger.debug("Register as node_id ({node_id})".format(node_id=self.node_id))
            admin_logger.debug("{name} at {hostname} with node id {node_id} registered to conductor.".
                               format(name=self.__class__.__name__, hostname=self.hostname,
                                      node_id=self.node_id))
        else:
            # log errors
            logger.error("{hostname} has no node_id".format(hostname=self.hostname))
            admin_logger.error("{name} at {hostname} with node id {node_id} failed to register to conductor. Please check {hostname}".
                               format(name=self.__class__.__name__, hostname=self.hostname, node_id=self.node_id))


@celery.task(name=Constants.PLAYER_TASK, ignore_result=True)
def player_task(command, nodes):
    """
    This is a player task that runs on slave database. It assumes only one celery worker per node. So task
    will be a singleton
    Please see https://docs.google.com/a/amplify.com/drawings/d/14K89SK6FLTPCFi0clvmnrTFMaIkc0eDDwQ0kt8CsTCE/
    for architecture
    Two tasks, COMMAND_FIND_PLAYER and COMMAND_REST_PLAYER are executed regardless player nodes are included or not
    For other tasks. Player task checks membership of current player node in nodes argument represented as a list
    of node_id. Those tasks are executed if and only if membership is true.
    """
    with Player() as player:
        player.run_command(command, nodes)
