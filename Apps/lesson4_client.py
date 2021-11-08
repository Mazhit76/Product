import json
import logging
import os
import re
import socket
import sys
import time

sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append('/home/mazhit76/Рабочий стол/Lession/client_server/Lesson_serv_app/Product/Logs')
from Logs import log_config_client
from utils import ClientServer

LOG = logging.getLogger('app_client.main')


def global_configs():
    global CONFIGS
    server = ClientServer()
    CONFIGS = server.load_config()
    return CONFIGS


def assert_ip(ip):
    if not re.match(r'^(\d|[1-9]\d|1\d\d|2([0-4]\d|5[0-5]))\.'
                    r'(\d|[1-9]\d|1\d\d|2([0-4]\d|5[0-5]))\.'
                    r'(\d|[1-9]\d|1\d\d|2([0-4]\d|5[0-5]))\.'
                    r'(\d|[1-9]\d|1\d\d|2([0-4]\d|5[0-5]))$', ip):
        raise TypeError('You input IP address unsuitable!!!')
    return True


class Client(ClientServer):

    def __init__(self, is_server=False, CONFIGS=global_configs()):
        super().__init__(is_server)
        self.CONFIG = CONFIGS

    def create_presence_message(self, account_name):
        message = {
            self.CONFIG.get('ACTION'): self.CONFIG.get('PRESENCE'),
            self.CONFIG.get('TIME'): time.time(),
            self.CONFIG.get('USER'): {
                self.CONFIG.get('ACCOUNT_NAME'): account_name
            }
        }
        return message

    def handle_responce(self, message):
        if self.CONFIG.get('RESPONSE') in message:
            if message[self.CONFIG.get('RESPONSE')] == 200:
                return '200: OK'
            elif message[self.CONFIG.get('RESPONSE')] == 400:
                return f'400:{message[self.CONFIG.get("ERROR")]}'
            else:
                raise ValueError('Unknown kode in response!!!')
        raise ValueError('No response in message!!!')

    def get_ip_port_on_console(self):
        try:
            server_address = sys.argv[1]
            if not assert_ip(server_address):
                print('IP адресс неверная размерность')
                sys.exit(1)
            server_port = int(sys.argv[2])
            if not 65535 >= server_port >= 1024:
                raise ValueError
            return server_address, server_port
        except IndexError:
            server_address = self.CONFIG.get('DEFAULT_IP_ADDRESS')
            server_port = self.CONFIG.get('DEFAULT_IP_PORT')
            return server_address, server_port
        except ValueError:
            raise ValueError('Порт должен находится в переделах о 1024 до 65535')
            sys.exit(1)


def main():
    LOG.debug('Start app client.py')

    global CONFIGS
    server = ClientServer()
    CONFIGS = global_configs()
    client = Client()

    server_address, server_port = client.get_ip_port_on_console()
    print(f'{server_address}, {type(server_port)}')
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    presence_message = client.create_presence_message('Guest')

    byte_str = server.serializer_to_byte(presence_message, CONFIGS)
    server.send_messages(transport, byte_str)

    try:
        byte_str = server.get_message(transport, CONFIGS)
        response = server.serializer_off_byte(byte_str, CONFIGS)

        handled_response = client.handle_responce(response)
        print(f'Ответ от сервера: {response}')
        print(handled_response)
    except(ValueError, json.JSONDecodeError):
        print('Ошибка декодирования')


if __name__ == '__main__':
    main()
