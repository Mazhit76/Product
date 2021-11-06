from unittest import TestCase, main
from unittest.mock import patch, create_autospec, Mock
from data_for_tests import DataTests
from Apps.utils import ClientServer

class TestUtils(TestCase):

    def setUp(self):
        self.client_server = ClientServer()
        self.config_test = self.client_server.load_config()

    def tearDown(self) -> None:
        pass

    def test_serializer_to_byte_dict_on_input(self):
        with self.assertRaises(ValueError) as e:
            self.client_server.serializer_to_byte('Error', self.client_server.load_config())
        self.assertEqual('Ошибка. На вход подан не словарь для преобразования в json.', e.exception.args[0])

    def test_serializer_to_byte_error_encode(self):
        with self.assertRaises(ValueError) as e:
            self.config_test['ENCODING'] = 'test1'
            self.client_server.serializer_to_byte({}, self.config_test)
        self.assertEqual('Ошибка преобразования файла в json. Возможно тип кодировки непраильный.', e.exception.args[0])

    def test_serializer_off_byte_byte_on_input(self):
        with self.assertRaises(ValueError) as e:
            self.client_server.serializer_off_byte('test', self.config_test)
        self.assertEqual('Ошибка. На вход подан не байтовая строк для преобразования в словарь.', e.exception.args[0])

    def test_serializer_off_byte_error_encode(self):
        with self.assertRaises(ValueError) as e:
            self.config_test['ENCODING'] = 'test1'
            self.client_server.serializer_off_byte(b'test', self.config_test)
        self.assertEqual('Ошибка преобразования файла из json в словарь. Возможно тип кодировки неправильный.', e.exception.args[0])

    def test_serializer_off_byte_no_dict_output(self):
        with self.assertRaises(ValueError) as e:
            self.client_server.serializer_off_byte(b'test', self.config_test)
        self.assertEqual('Ошибка. На выходе преобразования json, находится не словарь.', e.exception.args[0])

    def test_send_messages_socket_send(self):
        create_autospec(self.client_server.send_messages, side_effect=Exception)
        with self.assertRaises(ValueError) as e:
            self.client_server.send_messages(DataTests.clint_socket_with_default_ip_address_port, b'test')
        self.assertEqual('Ошибка отправки соккета возможно, соккет закрыт.', e.exception.args[0])

    def test_send_messages_no_bytes_in_input(self):
        with self.assertRaises(ValueError) as e:
            self.client_server.send_messages(DataTests.clint_socket_with_default_ip_address_port, str('test'))
        self.assertEqual('На вход поступило не байтовая строка', e.exception.args[0])

    def test_get_message_error_type_len(self):
        self.config_test = {'MAX_PACKAGE_LENGTH': 'test'}
        with self.assertRaises(ValueError) as e:
            self.client_server.get_message(DataTests.clint_socket_with_default_ip_address_port, self.config_test)
        self.assertEqual('Размер данных для сокете не в виде числа', e.exception.args[0])

    def test_get_message_error_max_len(self):
        self.config_test = {'MAX_PACKAGE_LENGTH': 2000}
        with self.assertRaises(ValueError) as e:
            self.client_server.get_message(DataTests.clint_socket_with_default_ip_address_port, self.config_test)
        self.assertEqual('Размер данных для сокете слишком большой или отрицательный', e.exception.args[0])


    def test_get_message_error_min_len(self):
        self.config_test = {'MAX_PACKAGE_LENGTH': -1}
        with self.assertRaises(ValueError) as e:
            self.client_server.get_message(DataTests.clint_socket_with_default_ip_address_port, self.config_test)
        self.assertEqual('Размер данных для сокете слишком большой или отрицательный', e.exception.args[0])

    def test_get_message_error_socket(self):
        with self.assertRaises(ValueError) as e:
            self.client_server.get_message(DataTests.clint_socket_with_default_ip_address_port, self.config_test)
        self.assertEqual('Ошибка. Возможно сокке закрыт.', e.exception.args[0])

if __name__ == '__main__':
    main()