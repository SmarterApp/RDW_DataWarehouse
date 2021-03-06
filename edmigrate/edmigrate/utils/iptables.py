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
        blocked = False
        s = None
        try:
            s = socket.create_connection((host, port), 1)
        except ConnectionRefusedError:
            blocked = True
        finally:
            if s is not None:
                s.close()
        return blocked

    def check_block_output(self, host, port=5432):
        return self._check_block(host, port)

    def check_block_input(self, host, port=5432):
        return self._check_block(host, port)
