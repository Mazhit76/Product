import json
import socket
import sys
import time

from utils import ClientServer

class Client(ClientServer):

    def __init__(self, is_server=False):
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
            return f'400:{message[self.CONFIG.get("ERROR")]}'
        raise ValueError


def main():
    global CONFIGS
    server = ClientServer()
    CONFIGS = server.load_config()
    client = Client()
    try:
        server_address = sys.argv[1]

        server_port = int(sys.argv[2])
        if not 65535 >= server_port >= 1024:
            raise ValueError
    except IndexError:
        server_address = CONFIGS.get('DEFAULT_IP_ADDRESS')
        server_port = CONFIGS.get('DEFAULT_IP_PORT')
    except ValueError:
        print('Порт должен находится в переделах о 1024 до 65535')
        sys.exit(1)

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