import time
import unittest
from dataclasses import dataclass, asdict, astuple, field
from unittest.mock import Mock, call, MagicMock, patch
from Apps.lesson_4_server import Server


@dataclass
class DataTests:
    message: dict[str, str] = field(default_factory=dict)
    value_limits_ip_port: tuple = field(default=(1024, 65535))
    test_ip_address: str = '127.0.0.1'
    test_ip_port: int = 7777
    test_message_server_ok = {'response': 200}
    test_message_server_err = {'response': 400, 'ERROR': 'Bad Request'}
    test_message_client_to_server = {'action': 'presence', 'time': time.time(),
                                          'user': {'account_name': 'Guest'}}
    test_message_client_to_server_good = {'action': 'presence', 'time': time.time(),
                                                       'user': {'account_name': 'Guest'}}
    test_message_client_to_server_bag_action = {'action': '', 'time': time.time(),
                                      'user': {'account_name': 'Guest'}}
    test_message_client_to_server_bag_time = {'action': 'presence', 'time': 12345.12345,
                                                'user': {'account_name': 'Guest'}}

    test_message_client_to_server_bag_user = {'action': 'presence', 'time': time.time(),
                                              'user': {'account_name': ''}}

