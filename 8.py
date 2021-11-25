# from threading import Thread
# import time
#
# class ClockThread(Thread):
#     def __init__(self, interval):
#         super().__init__()
#         self.daemon = False
#         self.interval = interval
#
#     def run(self):
#         while True:
#             print("Текущее время: %s" % time.ctime())
#             time.sleep(self.interval)
#
# t = ClockThread(2)
# t.start()




# # И как определить свой класс, производный от Process (файл examples/02_multiprocess/02_proc_subclass.py):
# import multiprocessing
# import time
#
# class ClockProcess(multiprocessing.Process):
#     def __init__(self, interval):
#         multiprocessing.Process.__init__(self)
#         self.interval = interval
#
#
#     def run(self):
#         while True:
#             print("The time is %s" % time.ctime())
#             time.sleep(self.interval)
#
# if __name__ == "__main__":
#     p = ClockProcess(2)
#     p.start()

#
#
# import multiprocessing
# from time import sleep
#
#
# def consumer(input_q):
#     while True:
#         item = input_q.get()
#         # Обработать элемент
#         print(item) # <- Здесь может быть обработка элемента
#         sleep(3)
#         # Сообщить о завершении обработки
#         input_q.task_done()
#
# def producer(sequence, output_q):
#     for item in sequence:
#         output_q.put(item)     # Добавить элемент в очередь
#
# if __name__ == '__main__':
#     q = multiprocessing.JoinableQueue()
#     # Запустить несколько процессов-потребителей
#     cons_p1 = multiprocessing.Process(target=consumer, args=(q, ))
#     cons_p1.daemon = True
#     cons_p1.start()
#     cons_p2 = multiprocessing.Process(target=consumer, args=(q, ))
#     cons_p2.daemon = True
#     cons_p2.start()
#
#     # Воспроизвести элементы.
#     # Переменная sequence представляет последовательность элементов, которые
#     # будут передаваться потребителю. На практике вместо переменной можно
#     # использовать генератор или воспроизводить элементы другим
#     # способом.
#     sequence = [1, 2, 3, 4]
#     producer(sequence, q)
#
#     # Дождаться, пока все элементы не будут обработаны
#     q.join()




import multiprocessing

# Серверный процесс
import time


def adder(pipe):
    server_p, client_p = pipe
    client_p.close()
    while True:
        time.sleep(2)
        try:
            x, y = server_p.recv()
        except EOFError:
            break
        result = x + y
        server_p.send(result)
    time.sleep(3)
    print("Сервер завершил работу")    # Завершение

if __name__ == '__main__':
    server_p, client_p = multiprocessing.Pipe()
    # Запустить серверный процесс
    adder_p = multiprocessing.Process(target=adder, args=((server_p, client_p), ))
    adder_p.start()
    server_p.close()    # Закрыть серверный канал в клиенте
    # Послать серверу несколько запросов
    client_p.send((3, 4))
    print(client_p.recv())
    client_p.send(("Hello", "World"))
    print(client_p.recv())
    client_p.close()    # Конец. Закрыть канал
    print(f'{__name__} закончил работу')
    # adder_p.join()