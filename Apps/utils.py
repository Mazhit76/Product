import json
import os.path
import sys
import time
from json.decoder import JSONDecodeError

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

    def load_config(self):

        if not self.is_server:
            self.config_keys.append('DEFAULT_IP_ADDRESS')

        if not os.path.exists('../Data/config.json'):
            print('File configuration not find.')
            sys.exit()
        with open('../Data/config.json', "r", encoding='utf-8') as config_file:
            CONFIG = json.load(config_file)
        loaded_config_keys = list(CONFIG.keys())
        for key in self.config_keys:
            if key not in loaded_config_keys:
                print(f'In file configuration keys missing {key}')
                sys.exit()
        return CONFIG

    def serializer_to_byte(self, message, CONFIG) -> bytes:
        if isinstance(message, dict):
            try:
                json_message = json.dumps(message)
                return json_message.encode(CONFIG.get('ENCODING'))
            except Exception:
                raise ValueError('Ошибка преобразования файла в json. Возможно тип кодировки непраильный.')
        else:
            raise ValueError('Ошибка. На вход подан не словарь для преобразования в json.')

    def serializer_off_byte(self, byte_str, CONFIG) -> dict:
        if isinstance(byte_str, bytes):
            try:
                json_response = byte_str.decode(CONFIG.get('ENCODING'))
                try:
                    response = json.loads(json_response)
                    response['time'] = time.time()
                    return response
                except Exception:
                    raise ValueError('Ошибка. На выходе преобразования json, находится не словарь.')

            except (JSONDecodeError, LookupError):
                raise ValueError('Ошибка преобразования файла из json в словарь. Возможно тип кодировки неправильный.')
        else:
            raise ValueError('Ошибка. На вход подан не байтовая строк для преобразования в словарь.')

    def send_messages(self, opened_socked, byte_str):
        if isinstance(byte_str, bytes):
            try:
                opened_socked.send(byte_str)
            except Exception:
                raise ValueError('Ошибка отправки соккета возможно, соккет закрыт.')
        else:
            raise ValueError('На вход поступило не байтовая строка')

    def get_message(self, opened_socket, CONFIG):
        if isinstance(CONFIG.get('MAX_PACKAGE_LENGTH'), int):
            if CONFIG.get('MAX_PACKAGE_LENGTH') <= 1024 and CONFIG.get('MAX_PACKAGE_LENGTH') > 0:
                try:
                    return opened_socket.recv(CONFIG.get('MAX_PACKAGE_LENGTH'))
                except Exception:
                    raise ValueError('Ошибка. Возможно сокке закрыт.')
            raise ValueError('Размер данных для сокете слишком большой или отрицательный')
        raise ValueError('Размер данных для сокете не в виде числа')