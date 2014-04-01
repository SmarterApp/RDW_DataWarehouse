'''
Created on Mar 31, 2014

@author: ejen
'''
import subprocess
import socket
from edmigrate.utils.utils import Singleton
from edmigrate.utils.constants import Constants
from edmigrate.exceptions import IptablesCommandError


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
            # we just skip. we use the connection checking to verify rule changes are effective or not
            raise IptablesCommandError('iptables failed by mode[' + mode + '] chain[' + chain + ']')

    def block_pgsql_INPUT(self):
        self._modify_rule(Constants.IPTABLES_INSERT, Constants.IPTABLES_INPUT_CHAIN)

    def block_pgsql_OUTPUT(self):
        self._modify_rule(Constants.IPTABLES_INSERT, Constants.IPTABLES_OUTPUT_CHAIN)

    def unblock_pgsql_INPUT(self):
        self._modify_rule(Constants.IPTABLES_DELETE, Constants.IPTABLES_INPUT_CHAIN)

    def unblock_pgsql_OUTPUT(self):
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
        return not self._check_block(host, port)
