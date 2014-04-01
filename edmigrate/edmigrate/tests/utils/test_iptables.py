'''
Created on Mar 31, 2014

@author: ejen
'''
import unittest
from edmigrate.utils.iptables import Iptables
from edmigrate.exceptions import IptablesCommandError
from unittest.mock import patch, MagicMock
from edmigrate.utils.constants import Constants
import socket
from mocket.mocket import MocketSocket
import mocket
import subprocess


class IptableTest(unittest.TestCase):

    def setUp(self):
        self.iptables = Iptables()

    def tearDown(self):
        Iptables.cleanup()

    @patch('subprocess.check_output')
    def test_block_pgsql_input(self, MockSubprocess):
        MockSubprocess.return_value = lambda: None
        self.iptables.block_pgsql_INPUT()
        MockSubprocess.assert_called_once_with([Constants.IPTABLES_SUDO, Constants.IPTABLES_COMMAND,
                                                Constants.IPTABLES_TABLE, Constants.IPTABLES_FILTER,
                                                Constants.IPTABLES_INSERT, Constants.IPTABLES_INPUT_CHAIN,
                                                Constants.IPTABLES_JUMP, Constants.IPTABLES_TARGET],
                                               universal_newlines=True)
        #

    @patch('subprocess.check_output')
    def test_block_pgsql_output(self, MockSubprocess):
        MockSubprocess.return_value = lambda: None
        self.iptables.block_pgsql_OUTPUT()
        MockSubprocess.assert_called_once_with([Constants.IPTABLES_SUDO, Constants.IPTABLES_COMMAND,
                                                Constants.IPTABLES_TABLE, Constants.IPTABLES_FILTER,
                                                Constants.IPTABLES_INSERT, Constants.IPTABLES_OUTPUT_CHAIN,
                                                Constants.IPTABLES_JUMP, Constants.IPTABLES_TARGET],
                                               universal_newlines=True)

    @patch('subprocess.check_output')
    def test_unblock_pgsql_input(self, MockSubprocess):
        MockSubprocess.return_value = lambda: None
        self.iptables.unblock_pgsql_INPUT()
        MockSubprocess.assert_called_once_with([Constants.IPTABLES_SUDO, Constants.IPTABLES_COMMAND,
                                                Constants.IPTABLES_TABLE, Constants.IPTABLES_FILTER,
                                                Constants.IPTABLES_DELETE, Constants.IPTABLES_INPUT_CHAIN,
                                                Constants.IPTABLES_JUMP, Constants.IPTABLES_TARGET],
                                               universal_newlines=True)

    @patch('subprocess.check_output')
    def test_unblock_pgsql_output(self, MockSubprocess):
        MockSubprocess.return_value = lambda: None
        self.iptables.unblock_pgsql_OUTPUT()
        MockSubprocess.assert_called_once_with([Constants.IPTABLES_SUDO, Constants.IPTABLES_COMMAND,
                                                Constants.IPTABLES_TABLE, Constants.IPTABLES_FILTER,
                                                Constants.IPTABLES_DELETE, Constants.IPTABLES_OUTPUT_CHAIN,
                                                Constants.IPTABLES_JUMP, Constants.IPTABLES_TARGET],
                                               universal_newlines=True)

    @patch.object(mocket.mocket.MocketSocket, 'close')
    @patch('socket.create_connection')
    def test_check_block_input_non_blocked(self, MockSocket, MockMethod):
        MockSocket.side_effect = None
        MockSocket.return_value = mocket.mocket.MocketSocket(socket.AF_INET, socket.SOCK_STREAM)
        MockMethod.return_value = lambda: None
        block_status = self.iptables.check_block_input('localhost')
        self.assertTrue(block_status)

    @patch.object(mocket.mocket.MocketSocket, 'close')
    @patch('socket.create_connection')
    def test_check_block_output_non_blocked(self, MockSocket, MockMethod):
        MockSocket.side_effect = None
        MockSocket.return_value = mocket.mocket.MocketSocket(socket.AF_INET, socket.SOCK_STREAM)
        MockMethod.return_value = lambda: None
        block_status = self.iptables.check_block_output('localhost')
        self.assertTrue(block_status)

    @patch.object(mocket.mocket.MocketSocket, 'close')
    @patch('socket.create_connection')
    def test_check_block_input_blocked(self, MockSocket, MockMethod):
        MockSocket.side_effect = ConnectionRefusedError()
        MockSocket.return_value = mocket.mocket.MocketSocket(socket.AF_INET, socket.SOCK_STREAM)
        MockMethod.return_value = lambda: None
        block_status = self.iptables.check_block_input('localhost')
        self.assertFalse(block_status)

    @patch.object(mocket.mocket.MocketSocket, 'close')
    @patch('socket.create_connection')
    def test_check_block_output_blocked(self, MockSocket, MockMethod):
        MockSocket.side_effect = ConnectionRefusedError()
        MockSocket.return_value = mocket.mocket.MocketSocket(socket.AF_INET, socket.SOCK_STREAM)
        MockMethod.return_value = lambda: None
        block_status = self.iptables.check_block_output('localhost')
        self.assertFalse(block_status)

    @patch('subprocess.check_output')
    def test_subprocess_exception(self, MockSubprocess):
        MockSubprocess.side_effect = subprocess.CalledProcessError(-1, 'iptables')
        self.iptables._modify_rule(Constants.IPTABLES_INSERT, Constants.IPTABLES_INPUT_CHAIN)
        self.assertTrue(True)
