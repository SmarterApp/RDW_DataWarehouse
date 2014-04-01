'''
Created on Mar 31, 2014

@author: ejen
'''
import subprocess
import socket
from edmigrate.utils.utils import Singleton
from edmigrate.utils.constants import Constants
from edmigrate.exceptions import IptablesCommandError


class Iptables(metaclass=Singleton):

    def __init__(self, input_port=5432, output_port=5432, target=Constants.IPTABLES_TARGET):
        self._input_port = input_port
        self._output_port = output_port
        self._localhost = '127.0.0.1'
        self._timeout = 1
        self._target = target

    @classmethod
    def cleanup(cls):
        Iptables._instances = {}

    def _modify_rule(self, mode, chain):
        try:
            subprocess.check_output([Constants.IPTABLES_SUDO, Constants.IPTABLES_COMMAND,
                                     Constants.IPTABLES_TABLE, Constants.IPTABLES_FILTER,
                                     mode, chain,
                                     Constants.IPTABLES_JUMP, self._target],
                                    universal_newlines=True)
        except subprocess.CalledProcessError as e:
            # we just skip. we use the connection checking to verify rule changes are effective or not
            pass

    def block_pgsql_INPUT(self):
        self._modify_rule(Constants.IPTABLES_INSERT, Constants.IPTABLES_INPUT_CHAIN)

    def block_pgsql_OUTPUT(self):
        self._modify_rule(Constants.IPTABLES_INSERT, Constants.IPTABLES_OUTPUT_CHAIN)

    def unblock_pgsql_INPUT(self):
        self._modify_rule(Constants.IPTABLES_DELETE, Constants.IPTABLES_INPUT_CHAIN)

    def unblock_pgsql_OUTPUT(self):
        self._modify_rule(Constants.IPTABLES_DELETE, Constants.IPTABLES_OUTPUT_CHAIN)

    def _check_block(self, host, port):
        connected = True
        s = None
        try:
            s = socket.create_connection((host, port), 1)
        except ConnectionRefusedError:
            connected = False
        finally:
            if s is not None:
                s.close()
        return connected

    def check_block_output(self, host):
        return self._check_block(host, self._output_port)

    def check_block_input(self, host):
        return self._check_block(host, self._input_port)
