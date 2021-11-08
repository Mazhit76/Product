import json
import logging
import os
import socket
import sys
import time
from decos import Log
sys.path.append(os.path.join(os.getcwd(), '..'))
from Logs import log_config_server
from utils import ClientServer


LOG = logging.getLogger('server')
@Log()
def global_configs():
    global CONFIGS
    client = ClientServer()
    CONFIGS = client.load_config()
    return CONFIGS

class Server(ClientServer):

    def __init__(self, is_server=True, CONFIGS=global_configs()):
        super().__init__(is_server)
        self.CONFIG = CONFIGS
    @Log()
    def handle_message(self, message):

        if self.CONFIG.get('ACTION') in message \
                and message[self.CONFIG.get('ACTION')] == self.CONFIG.get('PRESENCE')\
                and self.CONFIG.get('TIME') in message \
                and isinstance(message[self.CONFIG.get('TIME')], float) \
                and message[self.CONFIG.get('TIME')] >= time.time()-self.CONFIG.get('DELTA_TIME_SERVER_ANSWER')\
                and self.CONFIG.get('USER') in message \
                and message[self.CONFIG.get('USER')][self.CONFIG.get('ACCOUNT_NAME')] == 'Guest':
            return {self.CONFIG.get('RESPONSE'): 200}

        return {
            self.CONFIG.get('RESPONSE'): 400,
            self.CONFIG.get('ERROR'): 'Bad Request'
        }

@Log()
def main_server():
    LOG.debug('START APPS server.py')

    client = ClientServer()
    CONFIGS = global_configs()
    server = Server()

    try:

        if '-p' in sys.argv:

            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = CONFIGS.get('DEFAULT_IP_PORT')
        if not 65535 >= listen_port >= 1024:
            raise ValueError
    except IndexError:
        LOG.warning('После -\'р\' необходимо указать порт')
        sys.exit(1)
    except ValueError:
        LOG.warning(f'Порт должен находится в переделах о 1024 до 65535. Получено: {sys.argv}')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = CONFIGS.get('DEFAULT_IP_ADDRESS')

    except IndexError:
        LOG.warning(f'После \'a\' - необходимо ставить ip адрес соедения. Получено: {sys.argv}')
        sys.exit(1)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((listen_address, int(listen_port)))

        s.listen(CONFIGS.get('MAX_CONNECTIONS'))

        while True:
            client_socket, client_address = s.accept()
            try:
                byte_str = server.get_message(client_socket, CONFIGS)
                message = server.serializer_off_byte(byte_str, CONFIGS)

                LOG.debug(f'Отправленно сообщение: {message}')
                response = server.handle_message(message)

                byte_str = server.serializer_to_byte(response, CONFIGS)
                client.send_messages(client_socket, byte_str)

            except (ValueError, json.JSONDecodeError):
                LOG.warning('Принято неккоректное сообщение от клиента')

            finally:
                client_socket.close()


if __name__ == '__main__':
    main_server()
