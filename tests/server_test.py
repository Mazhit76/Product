from unittest import TestCase, main
from unittest.mock import patch, Mock, MagicMock

import utils
from Apps.server import Server
from Apps.client import Client
from Apps.utils import ClientServer
from data_for_tests import DataTests


class TestSocket:
    """
    Test class for create tests sockets
    On input test dict off message
    """

    def __init__(self, test_message):
        self.test_message = test_message
        self.byte_str = None
        self.received_message = None


class TestMyCase(TestCase):

    def __init__(self, methodName: str = ...):
        super().__init__(methodName)

    def setUp(self):
        self.client_server = ClientServer()
        self.test_server = Server()
        self.test_client = Client()
        self.data_from_config: dict = self.test_server.load_config()
        self.data_test = DataTests()
        self.testListNone = None

    def tearDown(self):
        pass

    def setUpModule(self):
        pass

    def test_limits_value(self):
        self.assertNotEqual(Server, True)

    def test_dict_CONFIG_ClientServer(self):
        self.assertIsInstance(self.client_server.CONFIG, dict, 'CONFIG must is dict')

    def test_dict_CONFIG_is_not_empty(self):
        self.assertNotEqual(self.data_from_config, {}, 'Dictionary is empty!!!')

    def test_CONFIG_default_ip_address(self):
        self.assertEqual(self.data_from_config.get('DEFAULT_IP_ADDRESS'), self.data_test.test_ip_address,
                         'default ip is not '
                         '127.0.0.1')

    def test_CONFIG_default_port(self):
        self.assertEqual(self.data_from_config.get('DEFAULT_IP_PORT'), self.data_test.test_ip_port,
                         'Default ip port is not 7777')

    def test_message_from_client_answer_ok(self):
        Server.send = MagicMock()
        Server.send.return_value = None
        self.test_server.process_client_message(self.data_test.test_message_client_to_server_good, [],
                                                self.data_test.clint_socket_with_default_ip_address_port, [], {})
        self.test_server.send.assert_called_with({'response': 200},
                                                 self.data_test.clint_socket_with_default_ip_address_port)


    def _test_message_from_client_answer_bad_action(self):
        with self.assertRaises(ValueError) as err:
            Server.send = MagicMock()
            Server.send.return_value = None
            self.test_server.process_client_message(self.data_test.test_message_client_to_server_bag_action, [],
                                                    self.data_test.clint_socket_with_default_ip_address_port, [], {})
            self.assertEqual('Не существует клиент, кому отправлять Bad request', str(err.exception))

    def _test_message_from_client_answer_bad_time(self):
        with self.assertRaises(ValueError) as err:
            Server.send = MagicMock()
            Server.send.return_value = None
            self.test_server.process_client_message(self.data_test.test_message_client_to_server_bag_time, [],
                                                    self.data_test.clint_socket_with_default_ip_address_port, [], {})
            self.assertEqual('There is no client in the list', err.exception.args[0])

    def _test_message_from_client_answer_time_bad_type(self):
        self.assertIsInstance(self.data_test.test_message_client_to_server_bag_time['time'], float, 'Test date type '
                                                                                                    'is not float!!!')

    def _test_message_from_client_answer_bad_user(self):
        with self.assertRaises(ValueError) as err:
            self.test_server.process_client_message(self.data_test.test_message_client_to_server_bag_user, [],
                                                    self.data_test.clint_socket_with_default_ip_address_port, [], {})
            self.assertEqual('Name client is bad!!!', str(err.exception))
            self.test_server.send.assert_called_with(self.data_test.test_message_server_err_bad_user,
                                                     self.data_test.clint_socket_with_default_ip_address_port)

    def test_send_byte_exchange(self):
        self.assertIsInstance(
            self.client_server.serializer_to_byte(self.data_test.test_message_server_ok, self.data_from_config),
            bytes)

    @patch.object(ClientServer, 'serializer_to_byte', b'str', spec=ClientServer)
    @patch.object(ClientServer, 'send_messages', 'ok', spec=ClientServer)
    def test_send(self):
        self.assertEqual(self.client_server.serializer_to_byte, b'str')
        self.assertEqual(self.client_server.send_messages, 'ok')

    def test_handle_message_server(self):
        Server.send = MagicMock()
        Server.send.return_value = None
        self._test_message_from_client_answer_bad_action()
        self._test_message_from_client_answer_bad_time()
        self._test_message_from_client_answer_time_bad_type()
        self._test_message_from_client_answer_bad_user()

    def _test_load_config_no_empty(self):
        self.assertNotEqual(self.data_from_config, {}, "Output dict from test load_data_from_config is empty")

    def test_load_config_from_utils(self):
        self._test_load_config_no_empty()
        with self.assertRaises(Exception) as ctx:
            self.test_server.load_config()
            self.assertEqual('Error test load_data_from_config', str(ctx.exception))

    def tearDownModule(self):
        pass


if __name__ == "__main__":
    main()
