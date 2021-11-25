# """Простейший декоратор-функция"""
#
# import time
# from functools import wraps
#
#
# def decorator(func):
#     """Сам декоратор"""
#     # @wraps(func)
#     def wrapper():
#         """Обертка"""
#         print('Сейчас выполняется функция-обёртка')
#         time.sleep(2)
#         print(f'Это просто ссылка на экземпляр оборачиваемой функции: {func.__name__}')
#         time.sleep(2)
#         print('Выполняем оборачиваемую (исходную) функцию...')
#         time.sleep(2)
#         f = func()
#         time.sleep(2)
#         print('Выходим из обёртки')
#         return f
#
#     return wrapper
#
#
# @decorator
# def some_text():
#     """Какая-то логика"""
#     print('вычисления')
#     return 5
#
#
# # some_text()
#
# # some_text = decorator(some_text)
# # some_text()
# #
# #
# # print(type(some_text), some_text.__name__)
# # print(type(some_text), some_text.__doc__)
#
# # ==========================================
# # how to get the function result?
# print(some_text())



#
# """Простейший декоратор-функция"""
#
# import time
# import requests
#
#
# def decorator(func):
#     """Сам декоратор"""
#     def wrapper(*args, **kwargs):
#         """Обертка"""
#         start = time.time()
#         return_value = func(*args, **kwargs)
#         end = time.time()
#         print(f'Отправлен запрос на адрес {args[0]}. '
#               f'Время выполнения: {round(end-start, 2)} секунд')
#         return return_value
#     return wrapper
#
#
# @decorator
# def get_wp(url):
#     """Делаем запрос"""
#     res = requests.get(url)
#     return res
#
#
# print(get_wp('https://google.com'))



#
# """Простейший декоратор-функция"""
#
# import time
#
#
# def decorator(func):
#     """Сам декоратор"""
#     def wrapper(*args, **kwargs):
#         """Обертка"""
#         start = time.time()
#         return_value = func(*args, **kwargs)
#         end = time.time()
#         print(f'Расчёт для функции {func.__name__}. '
#               f'Время выполнения: {end-start} секунд')
#         return return_value
#     return wrapper
#
#
# @decorator
# def get_list_loop(x):
#     ll = []
#     for idx in range(x):
#         ll.append(idx)
#     return ll
#
#
# @decorator
# def get_list_comp(x):
#     return [idx for idx in range(x)]
#
#
# value = 10 ** 6
# get_list_loop(value)
# get_list_comp(value)




# """
# Простейший декоратор-функция
# Работаем с параметрами исходной функции
# """
#
#
# def log(func):
#     """Декоратор"""
#     def decorated(*args, **kwargs):
#         """Обертка"""
#         res = func(*args, **kwargs)
#         print(f'log: {func.__name__}({args}, {kwargs}) = {res}')
#         return res
#     return decorated
#
#
# @log
# def my_func(val_1, val_2):
#     """Простое вычисление"""
#     return val_1 * val_2
#
#
# print('-- Функции с декораторами --')
# # my_func(14, 15)
# #
# # print(my_func(14, 15))
#
# # другой подход применения декоратора к функции func = log(func)
# #
# # func = log(func)
# # func(14, 15)


#
# """Простейший декоратор-функция с параметром"""
#
# import time
#
#
# def sleep(timeout):
#     """Внешняя функция (формально - декоратор)"""
#     def decorator(func):
#         """Сам декоратор"""
#         def decorated(*args, **kwargs):
#             """Обертка"""
#
#             time.sleep(timeout)
#             res = func(*args, **kwargs)
#
#             print(f'Функция {func.__name__} зависла')
#             return res
#         return decorated
#     return decorator
#
#
# @sleep(3)
# def factorial(param):
#     """Вычисляем факториал"""
#     if param <= 1:
#         return 1
#     else:
#         return param * factorial(param - 1)
#
#
# print(' -- Использован декоратор, реализованный через функцию --')
# print('!!! Обратите внимание на то, сколько раз будет вызван декоратор (рекурсия) !!!')
# print(factorial(5))
# print()




class Log():
    def __init__(self):
        pass

    # Магический метод __call__ позволяет обращаться к объекту класса, как к функции
    def __call__(self, func):
        def decorated(*args, **kwargs):
            res = func(*args, **kwargs)
            print(f'log: {func.__name__}({args}, {kwargs})= {res}')
            return res

        return decorated

@Log()
def square(x):
    return x * x

square(3)

# другой подход применения декоратора к функции func2 = Log()(func2)
func2 = Log()(square)
func2(5)



#
# """Простейший декоратор-функция с параметром"""
#
# import time
# import requests
#
#
# def decorator(iters):
#     print('Этот декоратор!!!!')
#     """Внешняя функция (формально - декоратор)"""
#     def real_decorator(func):
#         """Сам декоратор"""
#         def wrapper(*args, **kwargs):
#             """Обертка"""
#             total_time = 0
#             for i in range(iters):
#                 start = time.time()
#                 func(*args, **kwargs)
#                 end = time.time()
#                 delta = end - start
#                 total_time += delta
#                 print(f'#{i + 1}: {delta:.2f} sec')
#
#             print(f'Среднее время выполнения: {total_time / iters:.2f} секунд')
#
#         return wrapper
#     return real_decorator
#
#
# @decorator(10)
# def get_wp(url):
#     """Запрос"""
#     res = requests.get(url)
#     return res
#
#
# get_wp('https://google.com')

#
# """
# Два декоратора
#
# (<ext_tag> [<int_tag> <Какой-то текст> </int_tag>] </ext_tag>)
# """
#
#
# def make_ext(func):
#     """Первый декоратор"""
#     return lambda: "(<ext_tag> " + func() + " </ext_tag>)"
#
#
# def make_int(func):
#     """Второй декоратор"""
#     return lambda: "[<int_tag> " + func() + " </int_tag>]"
#
#
# @make_ext
# @make_int
# def my_func():
#     """Какая-то логика"""
#     return "Какой-то текст"


# # порядок выполнения декораторов
# # сначала make_ext, потом make_int
# # func = make_ext(make_int(my_func))
#
# print(my_func())
#
#
# # def make_ext(func):
# #     """Первый декоратор"""
# #     def wrap(*args, **kwargs):
# #         return "(<ext_tag> " + func() + " </ext_tag>)"
# #     return wrap

# from deco_params_func_6 import decorator