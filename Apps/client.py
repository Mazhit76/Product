import json
import logging
import os
import socket
import threading

import sys
import time

from utils import ClientServer
from decos import Log
from errors import IncorrectDataRecivedError
from metaclasses import ClientMaker

sys.path.append('../')
sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append('/home/mazhit76/Рабочий стол/Lession/client_server/Lesson_serv_app/Product/Logs')

from utils import ClientServer

LOG = logging.getLogger('client')
from utils import *

@Log()
def global_configs():
    global CONFIGS
    server = ClientServer()
    CONFIGS = server.load_config()
    return CONFIGS


class Client(ClientServer, metaclass=ClientMaker):
    # __slots__ = ('CONFIG', 'is_server', 'config_keys')

    def __init__(self, is_server=False):
        super().__init__()
        self.is_server = is_server
        self.CONFIG = global_configs()

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
    def create_message(self, sock, account_name):
        """
        Функция запрашивает кому отправить сообщение и само сообщение,
        и отправляет полученные данные на сервер
        :param sock:
        :param account_name:
        :return:
        """
        to_user = input('Введите получателя сообщения: ')
        message = input('Введите сообщение для отправки: ')
        message_dict = {
            self.CONFIG.get('ACTION'): 'message',
            self.CONFIG.get('SENDER'): account_name,
            self.CONFIG.get('DESTINATION'): to_user,
            self.CONFIG.get('TIME'): time.time(),
            self.CONFIG.get('MESSAGE_TEXT'): message
        }
        LOG.debug(f'Сформирован словарь сообщения: {message_dict}')
        try:

            byte_str = self.serializer_to_byte(message_dict, CONFIGS)
            self.send_messages(sock, byte_str)
            LOG.info(f'Отправлено сообщение для пользователя {to_user}')
        except:
            LOG.critical('Потеряно соединение с сервером.')
            sys.exit(1)

    def print_help(self):
        """Функция выводящяя справку по использованию"""

        print('Поддерживаемые команды:')
        print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
        print('help - вывести подсказки по командам')
        print('exit - выход из программы')

    @Log()
    def user_interactive(self, sock, username):
        """Функция взаимодействия с пользователем, запрашивает команды, отправляет сообщения"""
        self.print_help()
        while True:
            command = input('Введите команду: ')
            if command == 'message':
                self.create_message(sock, username)
            elif command == 'help':
                self.print_help()
            elif command == 'exit':
                presence_message = self.create_presence_message(username)
                byte_str = self.serializer_to_byte(presence_message, CONFIGS)
                self.send_messages(sock, byte_str)
                print('Завершение соединения.')
                LOG.info('Завершение работы по команде пользователя.')
                # Задержка неоходима, чтобы успело уйти сообщение о выходе
                time.sleep(0.5)
                break
            else:
                print('Команда не распознана, попробойте снова. help - вывести поддерживаемые команды.')

    @Log()
    def message_from_server(self, sock, my_username):
        """Функция - обработчик сообщений других пользователей, поступающих с сервера"""
        while True:
            try:
                byte_str = self.get_message(sock, CONFIGS)
                message = self.serializer_off_byte(byte_str, CONFIGS)
                if self.CONFIG.get('ACTION') in message and message[self.CONFIG.get('ACTION')] == self.CONFIG.get(
                        'MESSAGE') and \
                        self.CONFIG.get('SENDER') in message and self.CONFIG.get('DESTINATION') in message \
                        and self.CONFIG.get('MESSAGE_TEXT') in message and message[
                    self.CONFIG.get('DESTINATION')] == my_username:
                    print(f'\nПолучено сообщение от пользователя {message[self.CONFIG.get("SENDER")]}:'
                          f'\n{message[self.CONFIG.get("MESSAGE_TEXT")]}')
                    LOG.info(f'Получено сообщение от пользователя {message[self.CONFIG.get("SENDER")]}:'
                             f'\n{message[self.CONFIG.get("MESSAGE_TEXT")]}')
                else:
                    LOG.error(f'Получено некорректное сообщение с сервера: {message}')
            except IncorrectDataRecivedError:
                LOG.error(f'Не удалось декодировать полученное сообщение.')
            except (OSError, ConnectionError, ConnectionAbortedError,
                    ConnectionResetError, json.JSONDecodeError):
                LOG.critical(f'Потеряно соединение с сервером.')
                break


@Log()
def main():
    LOG.debug('Start app client.py')

    global CONFIG
    server = ClientServer()
    CONFIG = global_configs()
    client = Client()
    server_address, server_port, client_name = server.get_ip_port_on_console()

    """Сообщаем о запуске"""
    print(f'Консольный месседжер. Клиентский модуль. Имя пользователя: {client_name}')

    # Если имя пользователя не было задано, необходимо запросить пользователя.
    if not client_name:
        client_name = input('Введите имя пользователя: ')
    LOG.debug(f'IP:  {server_address}, port:  {server_port} имя пользователя: {client_name}')

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))

    presence_message = client.create_presence_message(client_name)
    byte_str = client.serializer_to_byte(presence_message, CONFIGS)
    client.send_messages(transport, byte_str)

    try:
        byte_str = client.get_message(transport, CONFIGS)
        response = client.serializer_off_byte(byte_str, CONFIGS)
        handled_response = client.handle_responce(response)
        LOG.debug(f'Установленно соединение. Ответ от сервера: {response} handled_response: {handled_response}')
    except(ValueError, json.JSONDecodeError):
        LOG.error('Ошибка декодирования')
    else:
        # Start connect with server and threading process
        receiver = threading.Thread(target=client.message_from_server, args=(transport, client_name))
        receiver.daemon = True
        receiver.start()

        # Start send messages and interactive with user
        client.user_interactive(transport, client_name)
        user_interface = threading.Thread(target=client.user_interactive, args=(transport, client_name))
        user_interface.daemon = True
        user_interface.start()
        LOG.debug('Запущены процессы')

        # Loop while two threading is alive
        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break

if __name__ == '__main__':
    main()

