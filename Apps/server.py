
import logging
import os
import select
import socket
import sys
import time
from decos import Log

sys.path.append(os.path.join(os.getcwd(), '..'))

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
    def process_client_message(self, message, messages_list, client, clients, names):

        """
        :param message: сообщение от клинета
        :param messages_list:  список сообщений на отправку
        :param client: новый запрос на подключение
        :param clients: список из сокетов, активных подключений
        :param names: словарь имен и соккетов пользователей активных подключений
        :return: словарь сообщение
        """

        if self.CONFIG.get('ACTION') in message \
                and message[self.CONFIG.get('ACTION')] == self.CONFIG.get('PRESENCE') \
                and self.CONFIG.get('TIME') in message \
                and isinstance(message[self.CONFIG.get('TIME')], float) \
                and message[self.CONFIG.get('TIME')] >= time.time() - self.CONFIG.get('DELTA_TIME_SERVER_ANSWER'):
            # Если клиент нет в списке, то регистрирум и отправляем сообщение о подключении
            # Иначе удаляем и отправляем ошибку запроса
            if self.CONFIG.get('USER') in message \
                    and (message[self.CONFIG.get('USER')][self.CONFIG.get('ACCOUNT_NAME')] not in names.keys()):
                names[message[self.CONFIG.get('USER')][self.CONFIG.get('ACCOUNT_NAME')]] = client
                self.send({self.CONFIG.get('RESPONSE'): 200}, client)
            else:
                _response = {
                    self.CONFIG.get('RESPONSE'): 400,
                    self.CONFIG.get('ERROR'): 'Username is already takenBad Request'
                }
                self.send(_response, client)
                clients.remove(client)
                client.close()
            return
        #     Если это сообщение, то добавляем в очередь сообщений. Овета клиенту нет.
        elif self.CONFIG.get('ACTION') in message \
                and message[self.CONFIG.get('ACTION')] == self.CONFIG.get('MESSAGE') \
                and self.CONFIG.get('TIME') in message \
                and self.CONFIG.get('SENDER') in message \
                and self.CONFIG.get('DESTINATION') in message \
                and self.CONFIG.get('MESSAGE_TEXT') in message:
            messages_list.append(message)
            return
        # Если поступило сообщение о выходе клиента удаляем его
        elif self.CONFIG.get('ACTION') in message and message[self.CONFIG.get('ACTION')] == self.CONFIG.get("EXIT") \
                and (self.CONFIG.get('ACCOUNT_NAME') in message):
            clients.remove(names[message[self.CONFIG.get('ACCOUNT_NAME')]])
            names[message.get(self.CONFIG.get('ACCOUNT_NAME'))].close()
            del names[message.get(self.CONFIG.get('ACCOUNT_NAME'))]
            return
        # Иначе отправляем Bad request
        else:
            _response = {
                self.CONFIG.get('RESPONSE'): 400,
                self.CONFIG.get('ERROR'): 'Bad Request'
            }
            self.send(_response, client)
            clients.remove(client)
            client.close()
            return


    @Log()
    def process_messages(self, message, names, listen_socks):
        """
        Метод отправки определенному клиенту.
        На входе: сообщение, имя кому отправить, список слушающих сокетов
        """
        if message[self.CONFIG.get('DESTINATION')] in names and names[message[self.CONFIG.get('DESTINATION')]] in listen_socks:
            self.send(message, names[message[self.CONFIG.get('DESTINATION')]])
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
    clients = []
    messages_list = []
    # dict off names and for sockets
    names = {}



    listen_address, listen_port, server_name = client.get_ip_port_on_console()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((listen_address, int(listen_port)))
        s.listen(CONFIGS.get('MAX_CONNECTIONS'))

        # List clients and queue
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
                for client_with_message in recover_data_lst:
                    try:

                        # append message to list. If not else send bad request.
                        byte_str = server.get_message(client_with_message, CONFIGS)
                        message = server.serializer_off_byte(byte_str, CONFIGS)

                        server.process_client_message(message, messages_list, client_with_message, clients, names)
                        LOG.debug(f'messages = {message}')

                    except ValueError:
                        LOG.debug(f'Клиент {client_with_message} отключился от сервера')
                        clients.remove(client_with_message)


                for message_to_client in messages_list:
                    try:

                        server.process_messages(message_to_client, names, send_data_lst)
                        LOG.debug(f'Отправленно сообщение: {message_to_client}')

                    except (ValueError, BrokenPipeError):
                        LOG.info(f'Клиент {message_to_client["DESTINATION"]} отключился от сервера')
                        clients.remove(names[message_to_client['DESTINATION']])
                        del names[message_to_client['DESTINATION']]
                messages_list.clear()

if __name__ == '__main__':
    main_server()
