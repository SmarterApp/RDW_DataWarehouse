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

    def _check_rules(self, chain):
        rule_exists = False
        try:
            output = subprocess.check_output([Constants.IPTABLES_SUDO, Constants.IPTABLES_SAVE_COMMAND],
                                             universal_newlines=True)
            for line in output.split('\n'):
                if line == " ".join([Constants.IPTABLES_APPEND, chain, Constants.IPTABLES_JUMP, self._target]) or \
                   line == " ".join([Constants.IPTABLES_INSERT, chain, Constants.IPTABLES_JUMP, self._target]):
                    rule_exists = True
                    break
        except subprocess.CalledProcessError as e:
            # we can't do anything except let rule_exists to be True so no action will be taken
            pass
        return rule_exists

    def block_pgsql_INPUT(self):
        check = self._check_rules(Constants.IPTABLES_INPUT_CHAIN)
        if not check:
            self._modify_rule(Constants.IPTABLES_INSERT, Constants.IPTABLES_INPUT_CHAIN)

    def block_pgsql_OUTPUT(self):
        check = self._check_rules(Constants.IPTABLES_OUTPUT_CHAIN)
        if not check:
            self._modify_rule(Constants.IPTABLES_INSERT, Constants.IPTABLES_OUTPUT_CHAIN)

    def unblock_pgsql_INPUT(self):
        check = self._check_rules(Constants.IPTABLES_INPUT_CHAIN)
        if check:
            self._modify_rule(Constants.IPTABLES_DELETE, Constants.IPTABLES_INPUT_CHAIN)

    def unblock_pgsql_OUTPUT(self):
        check = self._check_rules(Constants.IPTABLES_OUTPUT_CHAIN)
        if check:
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
