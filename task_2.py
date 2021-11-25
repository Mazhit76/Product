"""
2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
Меняться должен только последний октет каждого адреса.
По результатам проверки должно выводиться соответствующее сообщение.
"""
import ipaddress
import re
import os
import multiprocessing
import subprocess
from socket import gaierror, gethostbyname

devices = ['192.168.100.1', '192.168.100.155', '8.8.8.8', '4.4.4.4', 'yandex.ru', 'google.com', 'jhjkhkjh',
           'delevoper.ru']
DNULL = open(os.devnull, 'w')


def assert_ip(ip):
    if not re.match(r'^(\d|[1-9]\d|1\d\d|2([0-4]\d|5[0-5]))\.'
                    r'(\d|[1-9]\d|1\d\d|2([0-4]\d|5[0-5]))\.'
                    r'(\d|[1-9]\d|1\d\d|2([0-4]\d|5[0-5]))\.'
                    r'(\d|[1-9]\d|1\d\d|2([0-4]\d|5[0-5]))$', ip):
        raise TypeError('You input IP address unsuitable!!!')
    return True


def last_oktet_zero(ip):
    return ip.rpartition('.')[0] + '.0'


def host_range_ping():
    user_ip = input('Введите ip address, последний октет будет обнулен: ')
    list_ip = []
    if assert_ip(user_ip):
        user_last_oktet = last_oktet_zero(user_ip)
        subnet = ipaddress.ip_network(user_last_oktet + '/28')
        list_ip = list(subnet.hosts())
        return list_ip


def ping(host, mp_queue):
    try:
        ip_adr_str = str(ipaddress.ip_address(gethostbyname(host)))
    except gaierror:
        print(f'Хост: {host} не определился!!!')
        mp_queue.put((False, host))
        return
    except ValueError:
        ip_adr_str = host
    response = subprocess.call(["ping", "-c", "2", "-w", '2', ip_adr_str], shell=False, stdout=DNULL)
    if response == 0:
        print(f'host: {host}, ip: {ip_adr_str}, is up!')
        result = True
    else:
        print(f'host: {host}, ip: {ip_adr_str}, is down!')
        result = False
    mp_queue.put((result, host))


def host_ping(devices):
    mp_queue = multiprocessing.Queue()
    processes = []
    for device1 in devices:
        device = str(device1)
        p = multiprocessing.Process(target=ping, args=(device, mp_queue))
        processes.append(p)
        p.daemon = False
        p.start()
    for p in processes:
        p.join()
    results = {True: [], False: []}
    for p in processes:
        key, value = mp_queue.get()
        results[key] += [value]
        p.close()
    return results[True], results[False]


devices_new = host_range_ping()

success, failed = host_ping(devices_new)

print(f'Список доступных хостов: {success}')
print(f'Список недоступных хостов: {failed}')

# """Python для сетевых инженеров"""
#
# # операции с объектом-сетью
# from ipaddress import ip_network
#
# # Функция ipaddress.ip_network() позволяет создать объект,
# # который описывает сеть (IPv4 или IPv6)
#
# # атрибут получения широковещательного адреса для сети - broadcast_address
# # пакет посланный по этому адресу получат все машины в этой сети
# SUBNET = ip_network('1.0.0.0/24')
# BA = SUBNET.broadcast_address
# print(BA)
#
# # просмотр всех хостов для объекта-сети - метод hosts()
# print(list(SUBNET.hosts()))
#
# # разбиение сети на подсети (по умолчанию на 2) - метод subnets()
# print(list(SUBNET.subnets()))
#
# # обращение к любому адресу в сети
# # объект-сеть в Python представляется в виде списка ip-адресов, к каждому из которых
# # можно обратиться по индексу
# print(SUBNET[1])
