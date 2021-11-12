import json
import logging
import os
import re
import socket
import sys
import time
from decos import Log

sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append('/home/mazhit76/Рабочий стол/Lession/client_server/Lesson_serv_app/Product/Logs')

from Logs import log_config_client
from utils import ClientServer

LOG = logging.getLogger('client')


@Log()
def global_configs():
    global CONFIGS
    server = ClientServer()
    CONFIGS = server.load_config()
    return CONFIGS


class Client(ClientServer):

    def __init__(self, is_server=False, CONFIG=global_configs()):
        self.is_server = is_server
        super().__init__()
        self.CONFIG = CONFIG

    @Log()
    def create_presence_message(self, account_name):
        message = {
            self.CONFIG.get('ACTION'): self.CONFIG.get('PRESENCE'),
            self.CONFIG.get('TIME'): time.time(),
            self.CONFIG.get('USER'): {
                self.CONFIG.get('ACCOUNT_NAME'): account_name
            }
        }
        return message
    @Log()
    def handle_responce(self, message):
        if self.CONFIG.get('RESPONSE') in message:
            if message[self.CONFIG.get('RESPONSE')] == 200:
                return '200: OK'
            elif message[self.CONFIG.get('RESPONSE')] == 400:
                return f'400:{message[self.CONFIG.get("ERROR")]}'
            else:
                raise ValueError('Unknown kode in response!!!')
        raise ValueError('No response in message!!!')


@Log()
def main():
    LOG.debug('Start app client.py')

    global CONFIG
    server = ClientServer()
    CONFIG = global_configs()
    client = Client()

    server_address, server_port = server.get_ip_port_on_console()
    LOG.debug(f'IP:  {server_address}, port:  {server_port}')
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))
    presence_message = client.create_presence_message('Guest')

    byte_str = server.serializer_to_byte(presence_message, CONFIGS)
    server.send_messages(transport, byte_str)

    try:
        byte_str = server.get_message(transport, CONFIGS)
        response = server.serializer_off_byte(byte_str, CONFIGS)

        handled_response = client.handle_responce(response)
        LOG.debug(f'Ответ от сервера: {response} handled_response: {handled_response}')
        input()
    except(ValueError, json.JSONDecodeError):
        LOG.error('Ошибка декодирования')


if __name__ == '__main__':
    main()
