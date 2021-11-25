import argparse
import json
import logging
import os.path
import re
from json.decoder import JSONDecodeError
from Apps.metaclasses import ServerMaker
import sys
import time

from decos import Log

LOG = logging.getLogger('utils')
sys.path.append('../')
sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append('/home/mazhit76/Рабочий стол/Lession/client_server/Lesson_serv_app/Product/')


@Log()
def assert_ip(ip):
    if not re.match(r'^(\d|[1-9]\d|1\d\d|2([0-4]\d|5[0-5]))\.'
                    r'(\d|[1-9]\d|1\d\d|2([0-4]\d|5[0-5]))\.'
                    r'(\d|[1-9]\d|1\d\d|2([0-4]\d|5[0-5]))\.'
                    r'(\d|[1-9]\d|1\d\d|2([0-4]\d|5[0-5]))$', ip):
        raise TypeError('You input IP address unsuitable!!!')
    return True

class ClientServer():
    __slots__ = ['CONFIG', 'is_server', 'config_keys', 'client_socket', 'client_address', 'server', 'name']
    def __init__(self, is_server=False):
        self.CONFIG = {}
        self.is_server = is_server
        self.config_keys = [
            "DEFAULT_IP_PORT",
            "MAX_CONNECTIONS",
            "MAX_PACKAGE_LENGTH",
            "ENCODING",
            "LOGGING_LEVEL",
            "ACTION",
            "TIME",
            "USER",
            "ACCOUNT_NAME",
            "SENDER",
            "DESTINATION",
            "PRESENCE",
            "RESPONSE",
            "ERROR",
            "MESSAGE",
            "MESSAGE_TEXT",
            "EXIT",
            "RESPONSE_200",
            "RESPONSE_400"
        ]

    @Log()
    def load_config(self):

        if not self.is_server:
            self.config_keys.append('DEFAULT_IP_ADDRESS')

        if not os.path.exists('../Data/config.json'):
            LOG.error(f'File configuration not find. os.path:  {os.path},  sys.path:   {sys.path}')
            sys.exit()
        with open('../Data/config.json', "r", encoding='utf-8') as config_file:
            CONFIG = json.load(config_file)
        loaded_config_keys = list(CONFIG.keys())
        for key in self.config_keys:
            if key not in loaded_config_keys:
                LOG.error(f'In file configuration keys missing {key}')
                sys.exit()
        return CONFIG

    @Log()
    def serializer_to_byte(self, message, CONFIG) -> bytes:
        if isinstance(message, dict):
            try:
                json_message = json.dumps(message)
                return json_message.encode(CONFIG.get('ENCODING'))
            except Exception:
                LOG.error(
                    f'Ошибка преобразования файла в json. Возможно тип кодировки непраильный. message: {message} , кодировка {CONFIG.get("ENCODING")}')
                raise ValueError('Ошибка преобразования файла в json. Возможно тип кодировки непраильный.')
        else:
            LOG.error(
                f'Ошибка преобразования файла в json. Возможно тип кодировки непраильный. message: {message} , кодировка {CONFIG.get("ENCODING")}')
            raise ValueError('Ошибка. На вход подан не словарь для преобразования в json.')

    @Log()
    def serializer_off_byte(self, byte_str, CONFIG) -> dict:
        if isinstance(byte_str, bytes):
            try:
                json_response = byte_str.decode(CONFIG.get('ENCODING'))
                try:
                    response = json.loads(json_response)
                    response['time'] = time.time()
                    return response
                except Exception:
                    LOG.error(
                        f'Ошибка. На выходе преобразования json, находится не словарь. {byte_str} , кодировка {CONFIG.get("ENCODING")}')
                    raise ValueError('Ошибка. На выходе преобразования json, находится не словарь.')

            except (JSONDecodeError, LookupError):
                LOG.error(
                    f'Ошибка преобразования файла из json в словарь. Возможно тип кодировки неправильный. {byte_str} , кодировка {CONFIG.get("ENCODING")}')
                raise ValueError('Ошибка преобразования файла из json в словарь. Возможно тип кодировки неправильный.')
        else:
            LOG.error(
                f'Ошибка. На вход подан не байтовая строк для преобразования в словарь. {byte_str} , кодировка {CONFIG.get("ENCODING")}')
            raise ValueError('Ошибка. На вход подан не байтовая строк для преобразования в словарь.')

    @Log()
    def send_messages(self, opened_socked, byte_str):
        if isinstance(byte_str, bytes):
            try:
                opened_socked.send(byte_str)
            except Exception:
                LOG.error(f'Ошибка отправки соккета возможно, соккет закрыт. {byte_str} socket: {opened_socked}')
                raise ValueError('Ошибка отправки соккета возможно, соккет закрыт.')
        else:
            LOG.error(f'На вход поступило не байтовая строка {byte_str} socket: {opened_socked}')
            raise ValueError('На вход поступило не байтовая строка')

    @Log()
    def get_message(self, opened_socket, CONFIG):
        if isinstance(CONFIG.get('MAX_PACKAGE_LENGTH'), int):
            if CONFIG.get('MAX_PACKAGE_LENGTH') <= 1024 and CONFIG.get('MAX_PACKAGE_LENGTH') > 0:
                try:
                    return opened_socket.recv(CONFIG.get('MAX_PACKAGE_LENGTH'))
                except Exception:
                    LOG.error(f'Ошибка. Возможно соккет закрыт.socket: {opened_socket}')
                    raise ValueError('Ошибка. Возможно сокке закрыт.')
            LOG.error(
                f'Размер данных для сокете слишком большой или отрицательный {CONFIG.get("MAX_PACKAGE_LENGTH")} socket: {opened_socket}')
            raise ValueError('Размер данных для сокете слишком большой или отрицательный')
        LOG.error(
            f'Размер данных для сокете не в виде числа {CONFIG.get("MAX_PACKAGE_LENGTH")} socket: {opened_socket}')
        raise ValueError('Размер данных для сокете не в виде числа')


    @Log()
    def get_ip_port_on_console(self):
        try:
            parser = argparse.ArgumentParser()
            parser.add_argument('addr', default=self.load_config().get('DEFAULT_IP_ADDRESS'), nargs='?')
            parser.add_argument('port', default=self.load_config().get('DEFAULT_IP_PORT'), type=int, nargs='?')
            parser.add_argument('-n', '--name', default=None, nargs='?')
            namespace = parser.parse_args(sys.argv[1:])
            client_name = namespace.name
            server_address = namespace.addr
            if not assert_ip(server_address):
                LOG.error('IP адресс неверная размерность')
                sys.exit(1)
            server_port = namespace.port
            if not 65535 >= server_port >= 1024:
                raise ValueError
            return server_address, server_port, client_name
        except IndexError:
            # self.CONFIG = self.load_config()
            # server_address = self.CONFIG.get('DEFAULT_IP_ADDRESS')
            # server_port = self.CONFIG.get('DEFAULT_IP_PORT')
            return server_address, server_port, None
        except ValueError:
            LOG.error('Порт должен находится в переделах о 1024 до 65535')
            raise ValueError('Порт должен находится в переделах о 1024 до 65535')

    @Log()
    def send(self, message, to_client):
        """
        :param message: message to client
        :param to_client: client socket to server
        :return: None
        """
        byte_str = self.serializer_to_byte(message, self.CONFIG)
        self.send_messages(to_client, byte_str)