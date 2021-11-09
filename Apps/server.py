import json
import logging
import os
import select
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

    def __init__(self, is_server=True, configs=global_configs(), client_socket = None, server = None):
        super().__init__(is_server)
        self.client_socket = client_socket
        self.server = server
        self.CONFIG = configs
    @Log()
    def handle_message(self, message, messages_list, client):

        if self.CONFIG.get('ACTION') in message \
                and message[self.CONFIG.get('ACTION')] == self.CONFIG.get('PRESENCE')\
                and self.CONFIG.get('TIME') in message \
                and isinstance(message[self.CONFIG.get('TIME')], float) \
                and message[self.CONFIG.get('TIME')] >= time.time()-self.CONFIG.get('DELTA_TIME_SERVER_ANSWER')\
                and self.CONFIG.get('USER') in message \
                and message[self.CONFIG.get('USER')][self.CONFIG.get('ACCOUNT_NAME')] == 'Guest':
            return {self.CONFIG.get('RESPONSE'): 200}
        elif self.CONFIG.get('ACTION') in message \
                and message[self.CONFIG.get('ACTION')] == self.CONFIG.get('MESSAGE') \
                and self.CONFIG.get('TIME') in message \
                and self.CONFIG.get('MESSAGE') in message:
            messages_list.append((message[self.CONFIG.get('ACCOUNT_NAME')], message[self.CONFIG.get('MESSAGE_TEXT')]))
            return
        else:
            bad_request = {
            self.CONFIG.get('RESPONSE'): 400,
            self.CONFIG.get('ERROR'): 'Bad Request'
        }
            byte_str = self.server.serializer_to_byte(bad_request, CONFIGS)
            client.send_messages(self.client_socket, byte_str)
            LOG.debug(f'Отправленно сообщение: {message}')

@Log()
def main_server():
    LOG.debug('START APPS server.py')

    client = ClientServer()
    CONFIGS = global_configs()
    server = Server()

    listen_address, listen_port = client.get_ip_port_on_console()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((listen_address, int(listen_port)))
        s.listen(CONFIGS.get('MAX_CONNECTIONS'))
        clients = []
        messages = []

        # set timeout reset with OSError
        s.settimeout(1)

        while True:
            try:
                client.client_socket, client.client_address = s.accept()
            except OSError:
                pass
            else:
                LOG.debug(f'Установлено соедение с Клиентом {client.client_address}')
                clients.append(client.client_address)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []
            try:
                if clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, err_lst, 0)
            except OSError:
                pass
            # take messages to dict. and send to every clients? if error exclude client.
            if recv_data_lst:
                for client_with_messages in recv_data_lst:
                    try:
                        # append message to list. If not else send bad request.
                        byte_str = server.get_message(client.client_socket, CONFIGS)
                        message = server.serializer_off_byte(byte_str, CONFIGS)
                        server.handle_message(message)

                    except:
                        LOG.debug(f'Клиент {client_with_messages.getpeername()} отключился от сервера')
                        clients.remove()


            if messages and send_data_lst:
                try:
                    message = {
                        CONFIGS.get('ACTION'): 'MESSAGE',
                        CONFIGS.get('SENDER'): messages[0][0],
                        CONFIGS.get('TIME'): time.time(),
                        CONFIGS.get('MESSAGE_TEXT'): messages[0][1]
                    }
                    del messages[0]
                    for waiting_client in send_data_lst:
                        try:
                            byte_str = server.serializer_to_byte(message, CONFIGS)
                            client.send_messages(client.client_socket, byte_str)
                            LOG.debug(f'Отправленно сообщение: {message}')
                        except:
                            LOG.debug(f'Клиент {client_with_messages.getpeername()} отключился от сервера')
                            waiting_client.close()
                            clients.remove(waiting_client)

                except (ValueError, json.JSONDecodeError):
                    LOG.warning('Принято неккоректное сообщение от клиента')



if __name__ == '__main__':
    main_server()
