import sys

import time
import unittest
from dataclasses import dataclass, asdict, astuple, field
from unittest.mock import Mock, call, MagicMock, patch
from Apps.server import Server


@dataclass
class DataTests:
    message: dict[str, str] = field(default_factory=dict)
    value_limits_ip_port: tuple = field(default=(1024, 65535))
    test_ip_address: str = '127.0.0.1'
    MAX_PACKAGE_LENGTH = 2000
    test_ip_port: int = 7777
    clint_socket_with_default_ip_address_port = {'fd': 7, 'family': 'AddressFamily.AF_INET', type: 'SocketKind.SOCK_STREAM',
                                                        'proto': 0, 'laddr': {'127.0.0.1', 7777}, 'raddr': {'127.0.0.1', 58960}}
    test_message_server_ok = dict(response=200)
    byte_message_server_ok: bytes = b"{'response': 200}"
    test_message_server_err = {'response': 400, 'ERROR': 'Bad Request'}
    test_message_server_err_bad_user = {'response': 400, 'ERROR': 'Username is already takenBad Request'}
    byte_test_message_server_err = b"{response': 400, 'ERROR': 'Bad Request'}"
    test_message_client_to_server = {'action': 'presence', 'time': 12345,
                                          'user': {'account_name': 'Guest'}}
    test_message_client_to_server_good = {'action': 'presence', 'time': time.time(),
                                                       'user': {'account_name': 'Guest'}}
    test_message_client_to_server_bag_action = {'action': '', 'time': time.time(),
                                      'user': {'account_name': 'Guest'}}
    test_message_client_to_server_bag_time = {'action': 'presence', 'time': 12345.12345,
                                                'user': {'account_name': 'Guest'}}

    test_message_client_to_server_bag_user = {'action': 'presence', 'time': time.time(),
                                              'user': {'account_name': ''}}

    test_sys_argv = ['client.py', '1.1.1.1', '9000']

