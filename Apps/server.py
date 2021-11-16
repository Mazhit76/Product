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
    __slots__ = ('client_socket', 'client_address', 'server')

    def __init__(self, is_server=True, configs=global_configs(), client_socket=None, server=None):
        super().__init__(server)
        self.client_socket = client_socket
        self.server = server
        self.CONFIG = configs
        self.server = server

    @Log()
    def handle_message(self, message, client, server):
        """
        :param message: message from client
        :param messages_list:  list out messages. If message bad send bad request
        :param client: class
        :return: None
        """

        if self.CONFIG.get('ACTION') in message \
                and message[self.CONFIG.get('ACTION')] == self.CONFIG.get('PRESENCE') \
                and self.CONFIG.get('TIME') in message \
                and isinstance(message[self.CONFIG.get('TIME')], float) \
                and message[self.CONFIG.get('TIME')] >= time.time() - self.CONFIG.get('DELTA_TIME_SERVER_ANSWER') \
                and self.CONFIG.get('USER') in message:
            # and message[self.CONFIG.get('USER')][self.CONFIG.get('ACCOUNT_NAME')] == 'Guest':
            return {self.CONFIG.get('RESPONSE'): 200}
        elif self.CONFIG.get('ACTION') in message \
                and message[self.CONFIG.get('ACTION')] == self.CONFIG.get('MESSAGE') \
                and self.CONFIG.get('TIME') in message \
                and self.CONFIG.get('MESSAGE') in message:
            client.to_message.append(
                (message[self.CONFIG.get('ACCOUNT_NAME')], str.upper(message[self.CONFIG.get('MESSAGE_TEXT')])))
            return
        else:
            return {
                self.CONFIG.get('RESPONSE'): 400,
                self.CONFIG.get('ERROR'): 'Bad Request'
            }
        # byte_str = server.serializer_to_byte(bad_request, self.CONFIG)
        # client.send_messages(self.client_socket, byte_str)
        # LOG.debug(f'Отправленно сообщение: {message}')

    @Log()
    def send(self, message, to_client):
        byte_str = self.serializer_to_byte(message, CONFIGS)
        self.send_messages(to_client, byte_str)



    @Log()
    def process_messages(self, message, names, listen_socks):
        """
        Метод отправки определенному клиенту.
        На входе: сообщение, имя кому отправить, список слушающих сокетов
        """
        if message.get('DESTINATION') in names and names[message.get('DESTINATION')] in listen_socks:
            self.send(message, names[message.get('DESTINATION')])
            LOG.info('f Отправленно сообщение пользователю message.get("DESTINATION") '
                     f'от пользователя:  {message.get("SENDER")}')
        elif message.get('DESTINATION') in names and names[message.get('DESTINATION')] not in listen_socks:
            raise ConnectionError
        else:
            LOG.error(f'Пользователь {message.get("DESTINATION")} не зарегистрирован на сервере, '
                      f'отправка сообщения невозможна.')

# @Log()
def main_server():
    LOG.debug('START APPS server.py')
    CONFIGS = global_configs()
    server = Server()
    client = ClientServer()

    listen_address, listen_port, server_name = client.get_ip_port_on_console()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((listen_address, int(listen_port)))
        s.listen(CONFIGS.get('MAX_CONNECTIONS'))
        clients = []
        to_client_message = []

        # set timeout reset with OSError
        s.settimeout(1)

        while True:
            try:
                client.client_socket, client.client_address = s.accept()
            except OSError:
                pass
            else:
                LOG.debug(f'Установлено соедение с Клиентом {client.client_address}')
                clients.append(client.client_socket)

            recover_data_lst = []
            send_data_lst = []
            err_lst = []
            try:
                if clients:
                    recover_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
            except OSError:
                pass

            # take messages to dict. and send to every clients? if error exclude client.
            if recover_data_lst:
                for client_with_messages in recover_data_lst:
                    try:

                        # append message to list. If not else send bad request.
                        byte_str = server.get_message(client_with_messages, CONFIGS)
                        message = server.serializer_off_byte(byte_str, CONFIGS)

                        to_client_message = server.handle_message(message, client, server)
                        LOG.debug(f'to_client_message = {to_client_message}')
                        # if to_client_message.get('action') == 'presence':

                    except ValueError:
                        LOG.debug(f'Клиент {client_with_messages} отключился от сервера')
                        clients.remove(client_with_messages)

            if to_client_message and send_data_lst:
                message = {
                    CONFIGS.get('RESPONSE'): 200,
                    CONFIGS.get('ACTION'): 'MESSAGE',
                    CONFIGS.get('SENDER'): list(to_client_message.keys())[0],
                    CONFIGS.get('TIME'): time.time(),
                    CONFIGS.get('MESSAGE_TEXT'): list(to_client_message.values())[0]
                }
                to_client_message.pop(list(to_client_message.keys())[0])
                for waiting_client in send_data_lst:
                    try:

                        server.send(message, waiting_client)

                        LOG.debug(f'Отправленно сообщение: {message}')
                    except (ValueError, BrokenPipeError):
                        LOG.debug(f'Клиент {client_with_messages} отключился от сервера')
                        waiting_client.close()
                        clients.remove(client_with_messages)


if __name__ == '__main__':
    main_server()
