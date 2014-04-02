'''
Created on Mar 31, 2014

@author: ejen
'''
import subprocess
import socket
from edmigrate.utils.utils import Singleton
from edmigrate.utils.constants import Constants
from edmigrate.exceptions import IptablesCommandError, IptablesSaveCommandError


class IptablesController(metaclass=Singleton):

    def __init__(self, target=Constants.IPTABLES_CHAIN):
        self._target = target

    def __enter__(self):
        return self

    def __exit__(self, _type, value, tb):
        pass

    def _modify_rule(self, mode, chain):
        try:
            subprocess.check_output([Constants.IPTABLES_SUDO, Constants.IPTABLES_COMMAND,
                                     Constants.IPTABLES_TABLE, Constants.IPTABLES_FILTER,
                                     mode, chain,
                                     Constants.IPTABLES_JUMP, self._target],
                                    universal_newlines=True)
        except Exception:
            raise IptablesCommandError('iptables failed by mode[' + mode + '] chain[' + chain + ']')

    def _check_rules(self, chain):
        rule_exists = False
        try:
            output = subprocess.check_output([Constants.IPTABLES_SUDO, Constants.IPTABLES_SAVE_COMMAND],
                                             universal_newlines=True)
            for line in output.split('\n'):
                line = line.strip()
                if line == " ".join([Constants.IPTABLES_APPEND, chain, Constants.IPTABLES_JUMP, self._target]) or \
                   line == " ".join([Constants.IPTABLES_INSERT, chain, Constants.IPTABLES_JUMP, self._target]):
                    rule_exists = True
                    break
        except Exception:
            raise IptablesSaveCommandError('iptables-save failed by chain[' + chain + ']')
        return rule_exists

    def block_pgsql_INPUT(self):
        rule_exists = self._check_rules(Constants.IPTABLES_INPUT_CHAIN)
        if not rule_exists:
            self._modify_rule(Constants.IPTABLES_INSERT, Constants.IPTABLES_INPUT_CHAIN)

    def block_pgsql_OUTPUT(self):
        rule_exists = self._check_rules(Constants.IPTABLES_OUTPUT_CHAIN)
        if not rule_exists:
            self._modify_rule(Constants.IPTABLES_INSERT, Constants.IPTABLES_OUTPUT_CHAIN)

    def unblock_pgsql_INPUT(self):
        rule_exists = self._check_rules(Constants.IPTABLES_INPUT_CHAIN)
        if rule_exists:
            self._modify_rule(Constants.IPTABLES_DELETE, Constants.IPTABLES_INPUT_CHAIN)

    def unblock_pgsql_OUTPUT(self):
        rule_exists = self._check_rules(Constants.IPTABLES_OUTPUT_CHAIN)
        if rule_exists:
            self._modify_rule(Constants.IPTABLES_DELETE, Constants.IPTABLES_OUTPUT_CHAIN)


class IptablesChecker(metaclass=Singleton):
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

    def check_block_output(self, host, port=5432):
        return self._check_block(host, port)

    def check_block_input(self, host, port=5432):
        return self._check_block(host, port)
