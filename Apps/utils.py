import json
import logging
import os.path
import sys
import time
from json.decoder import JSONDecodeError
from decos import Log
from Logs import log_config_utils

LOG = logging.getLogger('utils')

sys.path.append('/home/mazhit76/Рабочий стол/Lession/client_server/Lesson_serv_app/Product/Data/..')


class ClientServer:
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
