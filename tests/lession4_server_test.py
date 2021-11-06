import unittest
from unittest import TestCase, main
from Apps.lesson_4_server import Server
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


    def setUp(self):
        self.client_server = ClientServer()
        self.test_server = Server()
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
        self.assertDictEqual(self.test_server.handle_message(self.data_test.test_message_client_to_server_good),
                             self.data_test.test_message_server_ok)

    def _test_message_from_client_answer_bad_action(self):
        self.assertDictEqual(self.test_server.handle_message(self.data_test.test_message_client_to_server_bag_action),
                             self.data_test.test_message_server_err)

    def _test_message_from_client_answer_bad_time(self):
        self.assertDictEqual(self.test_server.handle_message(self.data_test.test_message_client_to_server_bag_time),
                             self.data_test.test_message_server_err)

    def _test_message_from_client_answer_time_bad_type(self):
        self.assertIsInstance(self.data_test.test_message_client_to_server_bag_time['time'], float, 'Test date type '
                                                                                                    'is not float!!!')

    def _test_message_from_client_answer_bad_user(self):
        self.assertDictEqual(self.test_server.handle_message(self.data_test.test_message_client_to_server_bag_user),
                             self.data_test.test_message_server_err)

    def test_handle_message_server(self):
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
