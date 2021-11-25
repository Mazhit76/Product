import logging
import os
import select
import socket
import sys
import time
from decos import Log
from descriptors import Port
from metaclasses import ServerMaker

sys.path.append(os.path.join(os.getcwd(), '..'))

from utils import ClientServer

LOG = logging.getLogger('server')


@Log()
def global_configs():
    global CONFIGS
    client = ClientServer()
    CONFIGS = client.load_config()
    return CONFIGS


class Server(ClientServer, metaclass=ServerMaker):
    # __slots__ = ['listen_address', 'name']
    listen_port = Port()

    def __init__(self, listen_address=None, listen_port=None, is_server=True):
        super().__init__(is_server)
        self.listen_address = listen_address
        self.listen_port = listen_port
        self.CONFIG = global_configs()

        self.clients = []
        self.messages_list = []
        # dict off names and for sockets
        self.names = {}

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
                    and (message[self.CONFIG.get('USER')][self.CONFIG.get('ACCOUNT_NAME')]) != '' \
                    and isinstance(message[self.CONFIG.get('USER')][self.CONFIG.get('ACCOUNT_NAME')], str) \
                    and (message[self.CONFIG.get('USER')][self.CONFIG.get('ACCOUNT_NAME')] not in names.keys()):
                names[message[self.CONFIG.get('USER')][self.CONFIG.get('ACCOUNT_NAME')]] = client
                self.send({self.CONFIG.get('RESPONSE'): 200}, client)
            else:
                try:
                    _response = {
                        self.CONFIG.get('RESPONSE'): 400,
                        self.CONFIG.get('ERROR'): 'Username is already takenBad Request'
                    }
                    self.send(_response, client)
                    clients.remove(client)
                    client.close()
                except AttributeError:
                    LOG.error('Не существует клиент, кому отправлять Bad request')
                except ValueError:
                    LOG.error('Name client is bad!!!')
                    raise ValueError('Name client is bad!!!')

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
            try:
                clients.remove(names[message[self.CONFIG.get('ACCOUNT_NAME')]])
                names[message.get(self.CONFIG.get('ACCOUNT_NAME'))].close()
                del names[message.get(self.CONFIG.get('ACCOUNT_NAME'))]
            except ValueError:
                LOG.error('Отсутствует список  clients  для удаления.')
            return
        # Иначе отправляем Bad request
        else:
            _response = {
                self.CONFIG.get('RESPONSE'): 400,
                self.CONFIG.get('ERROR'): 'Bad Request'
            }
            try:
                self.send(_response, client)
                clients.remove(client)
                client.close()
            except AttributeError:
                LOG.error('Не существует клиент, кому отправлять Bad request')
            except ValueError:
                raise ValueError('There is no client in the list')

            return

    @Log()
    def process_messages(self, message, names, listen_socks):
        """
        Метод отправки определенному клиенту.
        На входе: сообщение, имя кому отправить, список слушающих сокетов
        """
        if message[self.CONFIG.get('DESTINATION')] in names and names[
            message[self.CONFIG.get('DESTINATION')]] in listen_socks:
            self.send(message, names[message[self.CONFIG.get('DESTINATION')]])
            LOG.info('f Отправленно сообщение пользователю message.get("DESTINATION") '
                     f'от пользователя:  {message.get("SENDER")}')
        elif message.get('DESTINATION') in names and names[message.get('DESTINATION')] not in listen_socks:
            raise ConnectionError
        else:
            LOG.error(f'Пользователь {message.get("DESTINATION")} не зарегистрирован на сервере, '
                      f'отправка сообщения невозможна.')

    def init_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.listen_address, int(self.listen_port)))
        # List clients and queue
        # set timeout reset with OSError
        self.sock.settimeout(1)
        self.sock.listen(CONFIGS.get('MAX_CONNECTIONS'))

    def main_loop(self):
        self.init_socket()

        while True:
            try:
                client_socket, client_address = self.sock.accept()
            except OSError:
                pass
            else:
                LOG.debug(f'Установлено соедение с Клиентом {client_address}')
                self.clients.append(client_socket)
            recover_data_lst = []
            send_data_lst = []
            err_lst = []
            try:
                if self.clients:
                    recover_data_lst, send_data_lst, err_lst = select.select(self.clients, self.clients, [], 0)
            except OSError:
                pass
            # take messages to dict. and send to every self.clients? if error exclude client.
            if recover_data_lst:
                for client_with_message in recover_data_lst:
                    try:
                        # append message to list. If not else send bad request.
                        byte_str = self.get_message(client_with_message, CONFIGS)
                        message = self.serializer_off_byte(byte_str, CONFIGS)
                        self.process_client_message(message, self.messages_list, client_with_message,
                                                    self.clients, self.names)
                        LOG.debug(f'messages = {message}')
                    except ValueError:
                        LOG.debug(f'Клиент {client_with_message} отключился от сервера')
                        self.clients.remove(client_with_message)
                for message_to_client in self.messages_list:
                    try:
                        self.process_messages(message_to_client, self.names, send_data_lst)
                        LOG.debug(f'Отправленно сообщение: {message_to_client}')
                    except (ValueError, BrokenPipeError):
                        LOG.info(f'Клиент {message_to_client["DESTINATION"]} отключился от сервера')
                        self.clients.remove(self.names[message_to_client['DESTINATION']])
                        del self.names[message_to_client['DESTINATION']]
                self.messages_list.clear()

@Log()
def main_server():
    LOG.debug('START APPS server.py')
    CONFIGS = global_configs()
    client = ClientServer()

    listen_address, listen_port, server_name = client.get_ip_port_on_console()
    server = Server(listen_address, listen_port)
    LOG.info(f'Запущен сервер, на адресе: {listen_address}, порт для подключений {listen_port}')

    server.main_loop()


if __name__ == '__main__':
    main_server()
