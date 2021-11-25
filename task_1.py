"""
1. Написать функцию host_ping(), в которой с помощью утилиты ping
будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел
должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять
их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес
сетевого узла должен создаваться с помощью функции ip_address().
"""
import ipaddress
import threading
from socket import gethostbyname


import os
import multiprocessing
import subprocess
from socket import gaierror


devices = ['192.168.100.1', '192.168.100.155', '8.8.8.8', '4.4.4.4', 'yandex.ru', 'google.com',
           'jhjkhkjh', 'delevoper.ru', 'vodokanalsamara.ru', 'truboprochistka.ru', 'arendatekhnik.ru']
DNULL = open(os.devnull, 'w')





def ping(host,mp_queue):
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
# Преподователь обьяснил, что использование multiprocessing здесь неуместно, так как речь идет вводе выводе данных из
# из внешней программы, для которой лучше подходит threading. Спорить не буду так и объясняли. Но все же
def host_ping(devices):
    mp_queue = multiprocessing.Queue()
    processes = []
    for device in devices:
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

success, failed = host_ping(devices)

print(f'Список доступных хостов: {success}')
print(f'Список недоступных хостов: {failed}')