"""
Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
Но в данном случае результат должен быть итоговым по всем ip-адресам, представленным в табличном формате
(использовать модуль tabulate). Таблица должна состоять из двух колонок и выглядеть примерно так:
"""

"""
Преподователь прав по поводу того, что неуместно использовать multiprocessing в операциях ввода вывода(записи и чтения)
, так при больших объемах данных, колисчетво запускаемых процессов, с выдачей им системных ресурсов ведет к 
их исчерапинию и зависанию системы, в отличии от Thread потоков, большое количесвто ведет только к временной задержке,
 в зависимости от ОП, но система не расходует системные ресурсы(цп).
"""



import ipaddress
import re
import os
import multiprocessing
import subprocess
import threading
from socket import gaierror, gethostbyname

import tabulate

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


def host_range_ping(ip='165.22.94.213'):
    user_ip = input(f'Введите ip address, последний октет будет обнулен(по умолчанию {ip}): ') or ip
    list_ip = []
    if assert_ip(user_ip):
        user_last_oktet = last_oktet_zero(user_ip)
        subnet = ipaddress.ip_network(user_last_oktet + '/24')
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
        # p = multiprocessing.Process(target=ping, args=(device, mp_queue))
        p = threading.Thread(target=ping, args=(device, mp_queue))
        processes.append(p)
        p.daemon = False
        p.start()
    for p in processes:
        p.join()
    results = {True: [], False: []}
    for p in processes:
        key, value = mp_queue.get()
        results[key] += [value]
    # p.close()
    return results[True], results[False]


devices_new = host_range_ping()

success, failed = host_ping(devices_new)

print(f'Список доступных хостов: ')
print(tabulate.tabulate(success))
print(f'Список недоступных хостов:')
print(tabulate.tabulate(failed))