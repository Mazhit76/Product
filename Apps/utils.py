import json
import os.path
import sys
import time


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

    def serializer_to_byte(self, message, CONFIG):
        if isinstance(message, dict):
            try:
                json_message = json.dumps(message)
            except ValueError:
                print('Ошибка преобразования файла в json.')
                return
            return json_message.encode(CONFIG.get('ENCODING'))
        else:
            raise ValueError

    def serializer_off_byte(self, byte_str, CONFIG):
        if isinstance(byte_str, bytes):
            json_response = byte_str.decode(CONFIG.get('ENCODING'))
            response_dict = json.loads(json_response)
            response_dict['time'] = time.time()
            if isinstance(response_dict, dict):
                return response_dict
            else:
                raise ValueError
        else:
            raise ValueError

    def send_messages(self, opened_socked, byte_str):
        if isinstance(byte_str, bytes):
            opened_socked.send(byte_str)
        else:
            raise ValueError

    def get_message(self, opened_socket, CONFIG):
        try:
            response = opened_socket.recv(CONFIG.get('MAX_PACKAGE_LENGTH'))
            if isinstance(response, bytes):
                return response
            else:
                raise ValueError
        except Exception:
            print('Error converting to send socket!!!')