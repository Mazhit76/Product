import sys
from unittest import TestCase, main
from Apps.client import Client
from Apps.utils import ClientServer
from data_for_tests import DataTests
from unittest.mock import patch, create_autospec, Mock



class MyTestCase(TestCase):
    def setUp(self):
        self.client_server = ClientServer()
        self.test_client = Client()
        self.data_test = DataTests()

    def tearDown(self):
        pass

    def test_message_account_name_time(self):
        test_account_name = 'Guest'
        with patch.dict(self.test_client.create_presence_message(test_account_name), {'time': 12345}) as foo:
            self.assertEqual(foo, self.data_test.test_message_client_to_server, 'Error create presence message. '
                                                                                'A name or time is bad')


    def test_message_account_name_type(self):
        test_account_name = 'test'
        out = self.test_client.create_presence_message(test_account_name)
        self.assertIsInstance(out.get('user').get('account_name'), str, 'Error type name presence message.'
                                                                        ' Name must is string ')
    @patch.object(DataTests, 'test_message_server_ok', {'test':200})
    def test_handle_response_in_message(self):
        with self.assertRaises(ValueError) as e:
            self.test_client.handle_responce(self.data_test.test_message_server_ok)
        self.assertEqual('No response in message!!!', e.exception.args[0])

    @patch.object(DataTests, 'test_message_server_ok', {'response': 300})
    def test_handle_kod_response(self):
        with self.assertRaises(ValueError) as e:
            self.test_client.handle_responce(self.data_test.test_message_server_ok)
        self.assertEqual('Unknown kode in response!!!', e.exception.args[0])

    @patch('sys.argv', ['client.py', '1.1.1.1', '900'])
    def test_get_great_port_console_input(self):
        with self.assertRaises(ValueError) as e:
            self.test_client.get_ip_port_on_console()
        self.assertEqual('Порт должен находится в переделах о 1024 до 65535', e.exception.args[0])

    @patch('sys.argv', ['client.py', '11.1.1', '9000'])
    def test_get_bad_ip_console_input(self):
        with self.assertRaises(TypeError) as e:
            self.test_client.get_ip_port_on_console()
        self.assertEqual('You input IP address unsuitable!!!', e.exception.args[0])


if __name__ == '__main__':
    main()