# class C:
#     def _get_x(self):
#         """I'm the 'x' property."""
#         return self._x
#
#     def _set_x(self, value):
#         self._x = value
#
#     def _del_x(self):
#         del self._x
#
#     x = property(_get_x, _set_x, _del_x)

# Дескрипторы атрибутов
# При использовании свойств (@property) доступ к атрибутам управляется серией пользовательских функций
# get, set и delete.# Такой способ не вполне универсален, так как для каждого однотипного атрибута должен быть
# свой набор get/set/delete-методов.
# Более универсально использование объекта дескриптора. Это обычный объект, представляющий значение атрибута.
# За счет реализации одного или более специальных методов __get__(), __set__() и __delete__()
# он может подменять механизмы доступа к атрибутам и влиять на выполнение этих операций.
# Рассмотрим пример дескриптора, который контролирует тип значения для атрибута и препятствует удалению атрибута
# из экземпляра объекта (файл листинг 1):
# class TypedProperty:
#     def __init__(self, name, type_name, default=None):
#         self.name = "_" + name
#         self.type = type_name
#         self.default = default if default else type_name()
#
#     def __get__(self, instance, cls):
#         return getattr(instance, self.name, self.default)
#
#     def __set__(self, instance, value):
#         if not isinstance(value, self.type):
#             raise TypeError("Значение должно быть типа %s" % self.type)
#         setattr(instance, self.name, value)
#
#     def __delete__(self, instance):
#         raise AttributeError("Невозможно удалить атрибут")
#
# class Foo:
#     name = TypedProperty("name", str)
#     num = TypedProperty("num", int, 42)
#
# f = Foo()
# a = f.name
# f.name = "Гвидо"
# # del f.name
#
# f.num += 10

# Хранить данные в отдельном словаре объекта дескриптора — ключом будет служить сам объект внешнего класса
# from weakref import WeakKeyDictionary
#
#
# class Grade:
#     def __init__(self):
#         self._values = WeakKeyDictionary()   # вместо обычного dict нужно использовать класс weakref.WeakKeyDictionary
#     # создает словарь, в котором ключи представлены слабыми ссылками. Когда обычных ссылок на объект ключа не остается,
#     # соответствующий элемент словаря автоматически удаляется
#
#     def __get__(self, instance, instance_type):
#         if instance is None:
#             return self
#         return self._values.get(instance, 0)
#
#     def __set__(self, instance, value):
#         if not (1 <= value <= 5):
#             raise ValueError("Оценка должна быть от 1 до 5")
#         self._values[instance] = value
#
#         # Хранить данные в отдельном словаре объекта дескриптора
#         # — ключом будет служить сам объект внешнего класса
#
# class Exam():
#     ''' Класс Экзамен.
#         Для простоты хранит только оценку за экзамен.
#     '''
#     grade = Grade()
#
# # Но не стоит забывать, что при таком подходе
# # данные будут сохранены на уровне атрибута класса Экзамен!!!
# # Т.е. будут общими для всех экземпляров класса Экзамен.
#
# # Для демонстрации создадим два Экзамена:
# math_exam = Exam()
# math_exam.grade = 3
# language_exam = Exam()
# language_exam.grade = 5
#
# print("  Проверим результаты: ")
# print("Первый экзамен ", math_exam.grade, " — верно?")
# print("Второй экзамен ", language_exam.grade, " — верно?")
# print('Потому что... ')
# print('math_exam.grade is language_exam.grade =', math_exam.grade is language_exam.grade)


# Хранить данные в отдельном атрибуте внешнего класса — требуется только определить способ именования атрибута.
# Такой подход позволяет во внешнем классе создавать несколько объектов-дескрипторов одного класса:
# class Grade:
#     def __init__(self, name):
#         # Для данного подхода необходимо сформировать отдельное имя атрибута
#         self.name = '_' + name
#
#     def __get__(self, instance, instance_type):
#         if instance is None:
#             return self
#         return "*{}*".format(getattr(instance, self.name))
#
#     def __set__(self, instance, value):
#         if not (1 <= value <= 100):
#             raise ValueError("Балл ЕГЭ должен быть от 1 до 100")
#         setattr(instance, self.name, value)
#
# class ExamEGE():
#     ''' Комплексный экзамен, на котором оцениваются разные критерии. '''
#     # Для обновленного Grade нужно добавить строковые имена
#     math_grade = Grade('math_grade')
#     writing_grade = Grade('writing_grade')
#     science_grade = Grade('science')
#
# # Для демонстрации создадим два Экзамена:
# math_exam = ExamEGE()
# math_exam.grade = 3
# language_exam = ExamEGE()
# language_exam.grade = 5
#
# print("  Проверим результаты: ")
# print("Первый экзамен ", math_exam.grade, " — верно?")
# print("Второй экзамен ", language_exam.grade, " — верно?")
# print('Потому что... ')
# print('math_exam.grade is language_exam.grade =', math_exam.grade is language_exam.grade)


# —————  __getattr__ + __getattribute__
# class ValidatingDB:
#     def __init__(self):
#         self.exists = 5
#
#     def __getattr__(self, name):
#         print(' ValidatingDB.__getattr__(%s)' % name)
#         value = 'Super %s' % name
#         setattr(self, name, value)
#         return value
#
#     def __getattribute__(self, name):
#         print(' ValidatingDB.__getattribute__(%s)' % name)
#         return super().__getattribute__(name)
#
#
# data = ValidatingDB()
# print('Атрибут exists:', data.exists)
# print('Атрибут foo: ', data.foo)
# print('Снова атрибут foo: ', data.foo)
# print('Есть ли атрибут zoom в объекте:', hasattr(data, 'zoom'))
# print('Атрибут face в объекте, доступ через getattr:', getattr(data, 'face'))
#
#
# # Использование метода __setattr__
# class SavingDB:
#     def __setattr__(self, name, value):
#         print(' SavingDB.__setattr__(%s, %r)' % (name, value))
#         # Сохранение данных в БД
#         # ...
#         super().__setattr__(name, value)
#
#
# data = SavingDB()
# print('data.__dict__ до установки атрибута: ', data.__dict__)
# data.foo = 5
# print('data.__dict__ после установки атрибута: ', data.__dict__)
# data.foo = 7
# print('data.__dict__ в итоге:', data.__dict__)

# При реализации методов __getattribute__ и __setattr__ можно столкнуться с ситуацией рекурсии,
# когда методы вызываются при каждом обращении к атрибуту объекта.
# В итоге Python исчерпывает стек вызовов и прерывает работу:
# Загвоздка в том, что метод __getattribute__ обращается к self._data, что снова приводит к вызову __getattribute__,
# а он вновь — к self._data. И так пока не остановится работа интерпретатора.
# Для решения этой проблемы внутри методов __getattribute__ и __setattr__ необходимо обращаться к атрибуту
# объекта через объект super: super().__getattribute__ или super().__setattr__.

#
# class BrokenDictionaryDB(object):
#     def __init__(self, data):
#         self._data = data
#
#     def __getattribute__(self, name):
#         print('Called __getattribute__(%s)' % name)
#         return self._data[name]  # Вызывает сам себя бесконечно
#
#
# data = BrokenDictionaryDB({'foo': 3})
# print(data.foo)
#
#
# class DictionaryDB(object):
#     def __init__(self, data):
#         self._data = data
#
#     def __getattribute__(self, name):
#         data_dict = super().__getattribute__('_data')  # Переопределил и уже вызывает другой экземлпляр
#         return data_dict[name]
#
#
# data = DictionaryDB({'foo': 'This is the right way!'})
# print(data.foo)


#
# class DocMeta(type):
#     def __init__(self, clsname, bases, clsdict):
#         for key, value in clsdict.items():
#             # Пропустить специальные и частные методы
#             if key.startswith("__"):
#                 print(key, value)
#                 continue
#
#             # Пропустить любые невызываемые объекты
#             if not hasattr(value, "__call__"):
#
#                 continue
#
#             # Проверить наличие строки документирования
#             if not getattr(value, "__doc__"):
#                 raise TypeError("%s must have a docstring" % key)
#
#         type.__init__(self, clsname, bases, clsdict)
#
# class Documented(metaclass=DocMeta):
#     pass
#
# class Foo(Documented):
#     def spam(self, a , b):
#         """
#
#         :param a:
#         :param b:
#         :return:
#         """
#         pass
#     def boo(self):
#         # """:cvar"""
#         print('A little problem!!!')



# class TypedProperty_v2: # Не работает
#     ''' Дескриптор атрибутов, контролирующий принадлежность указанному типу '''
#     def __init__(self, type_name, default=None):
#         self.name = None
#         self.type = type_name
#         if default:
#             self.default = default
#         else:
#             self.default = type_name()
#
#     def __get__(self, instance, cls):
#         return getattr(instance, self.name, self.default)
#
#     def __set__(self, instance, value):
#         if not isinstance(value, self.type):
#             raise TypeError("Значение должно быть типа %s" % self.type)
#         setattr(instance, self.name, value)
#
#
#     def __delete__(self, instance):
#         raise AttributeError("Невозможно удалить атрибут")
#
#
# class TypedMeta(type):
#     def __new__(cls, clsname, bases, clsdict):
#         slots = []
#         for key, value in clsdict.items():
#             if isinstance(value, TypedProperty_v2):
#                 value.name = "_" + key
#             slots.append(value.name)
#         clsdict['__slots__'] = slots
#         return type.__new__(cls, clsname, bases, clsdict)
#
# class Typed(metaclass=TypedMeta):
#     ''' Базовый класс для объектов, определяемых пользователем '''
#     pass
#
# class Foo(Typed):
#     name = TypedProperty_v2('name', str)
#     num = TypedProperty_v2('num', int, 42)
#     zzz = 15


#
# print(' ---- Шаблон Одиночка с использованием __call__ метакласса ---- ')
#
# # Объявляем метакласс, который будет контролировать создание нового класса
# class Singleton(type):
#
#     def __init__(self, *args, **kwargs):
#         print('__init__ in Metaclass. ', self, args, kwargs)
#         self.__instance = None
#         super().__init__(*args, **kwargs)
#
#     def __call__(self, *args, **kwargs):
#         print('__call__ in Metaclass')
#         print(' ', self, args, kwargs)
#         if self.__instance is None:
#             self.__instance = super().__call__(*args, **kwargs)
#             return self.__instance
#         else:
#             return self.__instance
#
#
# class BaseA(metaclass=Singleton):
#     def __init__(self):
#         print('Class BaseA')
#
#
# class BaseB(metaclass=Singleton):
#     def __init__(self):
#         print('Class BaseB')
#
#
# a_1 = BaseA()
# a_2 = BaseA()
#
# b_1 = BaseB()
# b_2 = BaseB()
#
# print('a_1 is a_2 - ', a_1 is a_2)
# print('b_1 is b_2 - ', b_1 is b_2)
# print('a_1 is b_1 - ', a_1 is b_1)
# print('a_2 is b_2 - ', a_2 is b_2)
# print('a_1 is b_2 - ', a_1 is b_2)
# print('a_2 is b_1 - ', a_2 is b_1)



#
# class NonNegative:
#
#     def __get__(self, instance, owner):
#         return instance.__dict__[self.my_attr]
#
#     def __set__(self, instance, value):
#         if value < 0:
#             raise ValueError("Не может быть отрицательным")
#         instance.__dict__[self.my_attr] = value
#
#     def __delete__(self, instance):
#         del instance.__dict__[self.my_attr]
#
#     def __set_name__(self, owner, my_attr):
#         # owner - владелец атрибута - <class '__main__.Worker'>
#         # my_attr - имя атрибута владельца - hours, rate
#         self.my_attr = my_attr
#
#
# class Worker:
#     # имя атрибута, который делаем дескриптором, в конструктор не передаем
#     hours = NonNegative()
#     rate = NonNegative()
#
#     def __init__(self, name, surname, hours, rate):
#         self.name = name
#         self.surname = surname
#         self.hours = hours
#         self.rate = rate
#
#     def total_profit(self):
#         return self.hours * self.rate
#
#
# OBJ = Worker('Иван', 'Иванов', 10, 100)
# print(OBJ.total_profit())
#
# OBJ.hours = 10
# OBJ.rate = 100
# print(OBJ.total_profit())
#
# # работает, как надо
# OBJ = Worker('Иван', 'Иванов', 100, -100)
# print(OBJ.total_profit())

# OBJ.hours = 10
# OBJ.rate = -100
# print(OBJ.total_profit())

# работает, как требуется
# проблема решена




# Все, что вы видите в Python – объекты.
# В том числе и строки, числа, классы и функции.
# ЭТО ВЕДЬ КЛАССЫ! ОКАЗЫВАЕТСЯ У КАЖДОГО ИЗ ЭТИХ КЛАССОВ ТОЖЕ ЕСТЬ КЛАСС - СВЕРХКЛАСС

# начнем
# AGE = 35
# print(AGE.__class__)
#
# NAME = 'Иван'
# print(NAME.__class__)
#
#
# def my_func():
#     pass
#
#
# print(my_func.__class__)
#
#
# class MyClass(object):
#     pass
#
#
# MC = MyClass()
# print(MC.__class__)
#
#
# # Получается каждый из этих объектов относится к классу
# # это мы знаем
# # а теперь самое интересное
#
# print(AGE.__class__.__class__)
#
# print(NAME.__class__.__class__)
#
# print(my_func.__class__.__class__)
#
# print(MC.__class__.__class__)
#
# # запускаем. вот это да!




"""А теперь посмотрим как создать метакласс для своих пользовательских классов"""
import logging

import sys

"""
Представьте, что мы устали от задания атрибутов в конструкторе 
__init__(self, *args, **kwargs). 
Как бы сделать так, чтобы мы смогли задавать атибуты непосредственно 
при создании экземпляра класса
"""

# Обычный класс такое не позволит

#
# class MyClass:
#     pass
#
#
# #MC = MyClass(param_1=100, param_2=200)
#
#
# """
# Вспомним, что объект создается через вызов класса с помощью оператора "()"
# Создадим метакласс наследованием от type
# Метакласс будет переопределять данный оператор "()"
# """
#
#
# class AttrOptim(type):
#     def __call__(self, *args, **kwargs):
#         """ Вызов класса создает новый объект. """
#         # Перво-наперво создадим сам объект...
#         obj = type.__call__(self, *args)
#         # ...и добавим ему переданные в вызове аргументы в качестве атрибутов.
#         for name in kwargs:
#             setattr(obj, name, kwargs[name])
#             # вернем готовый объект
#         return obj
#
#
# # Теперь создадим класс, использующий новый метакласс
# class MyClass(metaclass=AttrOptim):
#     pass
#
#
# # Ура!!!
# MC = MyClass(param_1=100, param_2=200)
# print(MC.param_1)
# print(MC.param_2)
#
#
# ### Внимание ###
# """
# Всё что угодно является объектом в Питоне:
# экземпляром класса или экземпляром метакласса.
#
# Кроме type!!!!!
#
# type является собственным метаклассом.
# Это нельзя воспроизвести на чистом Питоне и делается небольшим читерством на уровне реализации.
#
# Во-вторых, метаклассы сложны. Вам не нужно использовать
# их для простого изменения классов. Это можно делать двумя разными способами:
# -руками
# -декораторы классов
#
# В 99% случаев, когда вам нужно изменить класс, лучше использовать эти два.
# """


#
#
# LOG = logging.getLogger('basic')
# CRIT_HAND = logging.StreamHandler(sys.stderr)
# FORMATTER = logging.Formatter("%(levelname)-7s %(asctime)s %(message)s")
# CRIT_HAND.setFormatter(FORMATTER)
# LOG.addHandler(CRIT_HAND)
# LOG.setLevel(logging.DEBUG)
#
#
# class Logging(type):
#     # Метод on_log
#     def on_log(cls):
#         LOG.info(f'Данный метакласс фиксирует работу с классом {cls}')
#
#     # Вызываем метакласс
#     def __call__(self, *args, **kwargs):
#         # создаём новый класс как обычно
#         cls = type.__call__(self, *args)
#
#         # определяем новый метод on_log для каждого из этих классов
#         setattr(cls, "on_log", self.on_log)
#
#         # возвращаем класс
#         return cls
#
#
# # Проверяем метакласс
# class MyClass(metaclass=Logging):
#     def fixing(self):
#         self.on_log()
#
# # Создаём экземпляр метакласса. Он должен автоматически содержать метод on_log
# # хотя он не объявлен в классе вручную
# # иными словами, он объявлен за нас метаклассом
#
# MC = MyClass()
# MC.fixing()
#
# """
# Метаклассы дают нам возможность писать код, который изменяет не только данные,
# но и другой код, то есть изменяет класс во время его создания.
# В примере выше наш метакласс автоматически добавляет новый метод к новым классам,
# которые мы определяем, чтобы использовать метакласс.
# """




"""Пример метакласса, переопределяющего поведение методов __new__ и __init__ своих классов"""
#
# class MyMetaClass(type):
#     # Вызывается для создания экземпляра класса, перед вызовом __init__
#     def __new__(cls, name, bases, dct):
#         print(f'Выделение памяти для класса {name}, '
#               f'имеющего кортеж базовых классов {bases}, '
#               f'и словарь атрибутов {dct}')
#         return type.__new__(cls, name, bases, dct)
#     def __init__(cls, name, bases, dct):
#         print(f'Инициализация класса {name}')
#         super(MyMetaClass, cls).__init__(name, bases, dct)
#
#
# # родитель 1
# class Parent_1():
#     pass
#
# # родитель 2
# class Parent_2():
#     pass
#
# # пользовательский класс
# class MyClass(Parent_1, Parent_2, metaclass=MyMetaClass):
#     my_attr = 10
#
# MC = MyClass()

"""
Результат:

Выделение памяти для класса MyClass, 
имеющего кортеж базовых классов (<class '__main__.Parent_1'>, <class '__main__.Parent_2'>), 
и словарь атрибутов {'__module__': '__main__', '__qualname__': 'MyClass', 'my_attr': 10}

Инициализация класса MyClass
"""


"""Пример метакласса, переопределяющего поведение методов __new__, __init__ и __call__ своих классов"""

#
# class MyMetaClass(type):
#
#     def __new__(cls, name, bases, dict):
#         new_class = super(MyMetaClass, cls).__new__(cls, name, bases, dict)
#         print(f'__new__({name}, {bases}, {dict}) -> {new_class}')
#         return new_class
#
#     def __init__(cls, name, bases, dict):
#         super(MyMetaClass, cls).__init__(name, bases, dict)
#         print(f'__init__({name}, {bases}, {dict})')
#
#     def __call__(cls, *args, **kwargs):
#         obj = super(MyMetaClass, cls).__call__(*args, **kwargs)
#         print(f'__call__({args}, {kwargs}) -> {obj}')
#         return obj
#
# class Test(metaclass=MyMetaClass):
#     pass
#
# T_OBJ = Test()
#
# """
# __new__() вызывается для создания класса;
# __init__() для инициализации класса;
# __call__() вызывается при создании объектов класса;
#


# -------------------------- Метаклассы ----------------------------

# Классы в Python - это тоже объекты. Созданием классов заведуют метаклассы.
# В обычном случае созданием классов занимается функция type
#
# print(' ------- Создание класса функцией type ----------')
#
# # Используя функцию type можно вот так создать новый класс:
# Spam = type("Spam", (object,), {"name":'Python', "age":25})
# print('Новый класс, созданный функцией type:', Spam)
# print('Содержимое класса:', dir(Spam))
# print('Атрибуты класса:', Spam.__dict__)
# print()
#
# # -----------------------------------------------------------------------------
#
# print(' ------- Демонстрация очерёдности вызова методов метакласса ----------')
#
# class Meta(type):
#     @classmethod
#     def __prepare__(cls, clsname, bases):
#         print('>> Meta. __prepare__', cls, clsname, bases)
#         return dict()
#
#     def __new__(cls, clsname, bases, clsdict):
#         print('>> Meta.__new__', cls, clsname, bases, clsdict)
#         return type.__new__(cls, clsname, bases, clsdict)
#
#     def __init__(self, *args, **kwargs):
#         print('>> Meta.__init__', args, kwargs)
#         super().__init__(*args, **kwargs)
#
#     def __call__(cls, *args, **kwargs):
#         print('>> Meta.__call__', args, kwargs)
#         return super().__call__(*args, **kwargs)
#
# print('Перед созданием пользовательского класса Z')
#
# class Z(metaclass=Meta):
#     print('> Class Z. Начало тела класса')
#
#     def __init__(self, x):
#         print('> Z.__init__', x)
#         self.x = x
#
#     print('> Class Z. Конец тела класса')
#
#
# print('\nПеред созданием экземпляра класса Z')
#
# zorro = Z(13)
# print(zorro)


#
#
# from kivy.app import App
# from kivy.uix.button import Button
#
# class TestApp(App):
#     def build(self):
#         return Button(text='Hello world')
#
# TestApp().run()

#
# import kivy
# import random
#
# from kivy.app import App
# from kivy.uix.button import Button
# from kivy.uix.boxlayout import BoxLayout
#
# red = [1,0,0,1]
# green = [0,1,0,1]
# blue =  [0,0,1,1]
# purple = [1,0,1,1]
#
# class HBoxLayoutExample(App):
#     def build(self):
#         layout = BoxLayout(padding=10)
#         colors = [red, green, blue, purple]
#
#         for i in range(5):
#             btn = Button(text="Button #%s" % (i+1), size_hint=(.5, .5),
#                          pos_hint={'center_x': .5, 'center_y': .5},
#                          background_color=random.choice(colors)
#                          )
#             btn.bind(on_press=self.on_press_button)
#
#         return btn
#
#     def on_press_button(self, instance):
#         print('Вы нажали на кнопку!')
# if __name__ == "__main__":
#     app = HBoxLayoutExample()
#     app.run()
#
#
# from kivy.app import App
# from kivy.uix.button import Button
#
# class ButtonApp(App):
#     def build(self):
#         return Button()
#
#     def on_press_button(self):
#         print('Вы нажали на кнопку!')
#
# if __name__ == '__main__':
#     app = ButtonApp()
#     app.run()

#
#
# # --------------------- Дескрипторы атрибутов -------------------------------
#
# print(' ========== Базовый пример работы с дескриптором атрибутов ===========')
#
# class TypedProperty:
#     def __init__(self, name, type_name, default=None):
#         self.name = "_" + name
#         self.type = type_name
#         self.default = default if default else type_name()
#
#     def __get__(self, instance, cls):
#         return getattr(instance, self.name, self.default)
#
#     def __set__(self, instance, value):
#         if not isinstance(value, self.type):
#             raise TypeError("Значение должно быть типа %s" % self.type)
#         setattr(instance, self.name, value)
#
#     def __delete__(self, instance):
#         raise AttributeError("Невозможно удалить атрибут")
#
#
# class Foo:
#     name = TypedProperty("name", str)
#     num = TypedProperty("num", int, 42)
#
#
# if __name__ == '__main__':
#     f = Foo()
#     a = f.name          # Неявно вызовет Foo.name.__get__(f, Foo)
#     f.name = "Гвидо"    # Вызовет Foo.name.__set__(f, "Guido")
#     del f.name          # Вызовет Foo.name.__delete__(f)



#
# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.button import Button
# from kivy.uix.textinput import TextInput
#
# class MainApp(App):
#     def build(self):
#         self.operators = ["/", "*", "+", "-"]
#         self.last_was_operator = None
#         self.last_button = None
#         main_layout = BoxLayout(orientation="vertical")
#         self.solution = TextInput(
#             multiline=False, readonly=True, halign="right", font_size=55
#         )
#         main_layout.add_widget(self.solution)
#         buttons = [
#             ["7", "8", "9", "/"],
#             ["4", "5", "6", "*"],
#             ["1", "2", "3", "-"],
#             [".", "0", "C", "+"],
#         ]
#         for row in buttons:
#             h_layout = BoxLayout()
#             for label in row:
#                 button = Button(
#                     text=label,
#                     pos_hint={"center_x": 0.5, "center_y": 0.5},
#                 )
#                 button.bind(on_press=self.on_button_press)
#                 h_layout.add_widget(button)
#             main_layout.add_widget(h_layout)
#
#         equals_button = Button(
#             text="=", pos_hint={"center_x": 0.5, "center_y": 0.5}
#         )
#         equals_button.bind(on_press=self.on_solution)
#         main_layout.add_widget(equals_button)
#
#         return main_layout
#
#     def on_button_press(self, instance):
#         current = self.solution.text
#         button_text = instance.text
#
#         if button_text == "C":
#             # Очистка виджета с решением
#             self.solution.text = ""
#         else:
#             if current and (
#                     self.last_was_operator and button_text in self.operators):
#                 # Не добавляйте два оператора подряд, рядом друг с другом
#                 return
#             elif current == "" and button_text in self.operators:
#                 # Первый символ не может быть оператором
#                 return
#             else:
#                 new_text = current + button_text
#                 self.solution.text = new_text
#         self.last_button = button_text
#         self.last_was_operator = self.last_button in self.operators
#
#     def on_solution(self, instance):
#         text = self.solution.text
#         if text:
#             solution = str(eval(self.solution.text))
#             self.solution.text = solution
#
#
# if __name__ == "__main__":
#     app = MainApp()
#     app.run()



# -------------------------- Метаклассы -------------------------------------

# print(' ----- Демонстрация работы с методом __init__ метакласса -----')
#
# class DocMeta(type):
#     ''' Метакласс, проверяющий наличие строк документации в подконтрольном классе
#     '''
#     def __init__(self, clsname, bases, clsdict):
#         # К моменту начала работы метода __init__ метакласса
#         # словарь атрибутов контролируемого класса уже сформирован.
#         for key, value in clsdict.items():
#             # Пропустить специальные и частные методы
#             if key.startswith("__"): continue
#
#             # Пропустить любые невызываемые объекты
#             if not hasattr(value, "__call__"): continue
#
#             # Проверить наличие строки документирования
#             if not getattr(value, "__doc__"):
#                 raise TypeError("Метод %s должен иметь строку документации" % key)
#
#         type.__init__(self, clsname, bases, clsdict)
#
#
# class Documented(metaclass=DocMeta):
#     ''' Базовый класс для документированных классов. Можно оставить пустым.
#     '''
#     pass
#
#
# # Дочерний класс получает метакласс "в нагрузку" от родительского класса
# class Foo(Documented):
#     ''' Прикладной пользовательский класс.
#     '''
#     def spam(self, a, b):
#         ''' Метод spam делает кое-что '''
#         pass
#
#     def boo(self):
#         print('A little problem')




# --------------------- Дескрипторы атрибутов -------------------------------

# print(' ============ Примеры работы с дескрипторами атрибутов ===============')
#
# print(' ------------ Data-дескриптор ---------------')
#
# class DataDesc:
#     ''' Data-дескриптор
#     '''
#     def __get__(self, obj, cls=None):
#         print('  DataDesc.__get__')
#         print('  ', self, obj, cls)
#         return '**magic-descriptor**'
#
#     def __set__(self, obj, value):
#         print('  DataDesc.__set__')
#         print('  ', self, obj, value)
#         pass
#
#     def __delete__(self, obj):
#         print('  DataDesc.__delete__')
#         print('  ', self, obj)
#         pass
#
#
# class D:
#     ''' Класс с дескриптором данных
#     '''
#     d = DataDesc()
#
#
# d_obj = D()
#
# print('0. Содержимое d_obj.__dict__ в самом начале:', d_obj.__dict__)
#
# print('1. Получить значение атрибута...')
# # При доступе к атрибуту будет вызван метод __get__ дескриптора
# x = d_obj.d
# print('1. Значение атрибута (доступ через дескриптор):', x)
#
# # Создание атрибута в словаре экземпляра класса (дескриптор)
# print('2. Установить значение атрибута...')
# d_obj.d = "полезное значение"
# print('3. Содержимое d_obj.__dict__ после установки атрибута:', d_obj.__dict__)
#
# x = d_obj.d
# print('4. Значение атрибута (доступ через дескриптор):', x)
#
# # Удаление атрибута из словаря экземпляра класса
# print('5. Удалить атрибут...')
# del d_obj.d
# print('6. Содержимое d_obj.__dict__ удаления атрибута:', d_obj.__dict__)
#
#
# print('7. Получить атрибут на уровне класса...')
# x = D.d
# print('8. Значение атрибута D.d:', x)
#
# # Дескриптор будет заменён обычной строкой на уровне класса
# print('9. Установить D.d ...')
# D.d = "=A value in class="            # <<-- здесь не вызывается метод __set__
#
# print(' == \/ Обратите внимание  \/ ==')
# print('10. Значение атрибута D.d:', D.d)
# print('11. Значение атрибута d_obj.d:', d_obj.d)
#
# print()
# print(' ------------ Non-data-дескриптор ---------------')
#
# class GetonlyDesc:
#     ''' Non-data дескриптор
#     '''
#     def __get__(self, obj, cls=None):
#         return '**magic-descriptor**'
#
#
# class C:
#     ''' Класс с одним дескриптором
#     '''
#     d = GetonlyDesc()
#
#
# cobj = C()
#
# # При доступе к атрибуту будет вызван метод __get__ дескриптора
# x = cobj.d
# print('0. Содержимое объекта в самом начале:', cobj.__dict__)
# print('1. Значение атрибута (доступ через дескриптор):', x)
#
# # Создание атрибута в словаре экземпляра класса (дескриптор)
# cobj.d = "setting a value"
# x = cobj.d
# print('2. Значение атрибута (доступ через __dict__):', x)
# print('3. Содержимое объекта после  установки атрибута:', cobj.__dict__)
#
# # Удаление атрибута из словаря экземпляра класса
# del cobj.d
# print('4. Содержимое объекта после удаления атрибута:', cobj.__dict__)
#
# x = C.d
# print('5. Значение атрибута C.d:', x)
#
# # Дескриптор будет заменён обычной строкой на уровне класса
# C.d = "setting a value on class"
# print('6. Значение атрибута C.d:', C.d)




# -------------------------- Метаклассы ----------------------------

# print(' ------- Демонстрация работы с методом __new__ метакласса ----------')
#
# class TypedProperty:
#     def __init__(self, name, type_name, default=None):
#         self.name = "_" + name
#         self.type = type_name
#         self.default = default if default else type_name()
#
#     def __get__(self, instance, cls):
#         return getattr(instance, self.name, self.default)
#
#     def __set__(self, instance, value):
#         if not isinstance(value, self.type):
#             raise TypeError("Значение должно быть типа %s" % self.type)
#         setattr(instance, self.name, value)
#
#     def __delete__(self, instance):
#         raise AttributeError("Невозможно удалить атрибут")
#
#
#
# class TypedMeta(type):
#     ''' Метакласс, создающий список __slots__,
#         который будет содержать только атрибуты типа TypedProperty
#     '''
#     def __new__(cls, clsname, bases, clsdict):
#         slots = [ ]
#         for key, value in clsdict.items():
#             if isinstance(value, TypedProperty):
#                 value.name = "_" + key
#                 slots.append(value.name)
#         clsdict['__slots__'] = slots
#         return type.__new__(cls, clsname, bases, clsdict)
#
#
# class Typed(metaclass=TypedMeta):
#     ''' Базовый класс для объектов, определяемых пользователем.
#         Можно просто оставить пустым. Вся "магия" делается метаклассом.
#     '''
#     pass
#
#
# # Дочерний класс получает в "наследство" также и метакласс
# class Foo(Typed):
#     ''' Пользовательский класс с контролируемыми атрибутами
#     '''
#     name = TypedProperty('name', str)
#     num = TypedProperty('num', int, 42)
#     zzz = 15
#
#
# foo = Foo()
#
# # Попытка добавить новый атрибут объекту приведёт к исключению:
# # foo.xxx = 13          # <- раскомментируйте строку, чтобы увидеть исключение
# # print(foo.xxx)
#
# # Атрибут, который отсутствует в __slots__ становится read-only атрибутом
# print(foo.zzz)
# # foo.zzz = 77          # <- раскомментируйте строку, чтобы увидеть исключение
#
# # При этом "легитимные" атрибуты типа TypedProperty_v1
# # ведут себя обычным для атрибутов образом...
# foo.num = 99
# foo.name = 'Bigno!'
# print(foo.num, foo.name)
#
# # ... А также имеют дополнительные преимущества:
# foo.num = 'str'
# foo.name = 17



# # --------------------- Дескрипторы атрибутов -------------------------------
#
# print(' ====== Способы хранения значений при работе с дескрипторами =======')
# print(' ========== 1. Хранение в атрибуте дескриптора ==============')
#
# # Первый способ сохранить данные - просто в атрибуте объекта дескриптора.
#
# class Grade:
#     def __init__(self):
#         self._value = 0
#
#     def __get__(self, instance, instance_type):
#         return self._value
#
#     def __set__(self, instance, value):
#         if not (1 <= value <= 5):
#             raise ValueError("Оценка должна быть от 1 до 5")
#         self._value = value
#
#
# class Exam():
#     ''' Класс Экзамен.
#         Для простоты хранит только оценку за экзамен.
#     '''
#     grade = Grade()
#
# # Но не стоит забывать, что при таком подходе
# # данные будут сохранены на уровне атрибута класса Экзамен!!!
# # Т.е. будут общими для всех экземпляров класса Экзамен.
#
# # Для демонстрации создадим два Экзамена:
# math_exam = Exam()
# math_exam.grade = 3
#
# language_exam = Exam()
# language_exam.grade = 5
#
# print("  Проверим результаты: ")
# print("Первый экзамен ", math_exam.grade, " - верно?")
# print("Второй экзамен ", language_exam.grade, " - верно?")
#
# print('Потому что... ')
# print('math_exam.grade is language_exam.grade =', math_exam.grade is language_exam.grade)
#
# print()
#
# # =============================================================================
# print()
# print(' ====== 2. Хранение данных в отдельном словаре дескриптора =======')
# print('* Внимание! Хранение данных в обычном dict будет приводить к утечкам памяти! *')
#
# class Grade:
#     def __init__(self):
#         self._values = {}
#
#     def __get__(self, instance, instance_type):
#         if instance is None: return self
#         return self._values.get(instance, 0)
#
#     def __set__(self, instance, value):
#         if not (1 <= value <= 5):
#             raise ValueError("Оценка должна быть от 1 до 5")
#         self._values[instance] = value
#
#
# # Хотя данное решение достаточно простое и полноценно работает,
# # оно будет приводить к утечкам памяти!
# # Словарь _values будет хранить ссылку на каждый внешний экземпляр класса,
# # который когда-либо передавался в метод __set__.
# # Это приведет к тому, что счётчик ссылок у внешних экземпляров никогда не будет равен нулю,
# # и сборщик мусора никогда не выполнит свою работу.
#
# print()
# print(' Вместо обычного dict нужно использовать класс weakref.WeakKeyDictionary')
#
# from weakref import WeakKeyDictionary
#
# # ----------------------------------------------------------
# # Модуль weakref обеспечивает поддержку слабых ссылок.
# # В обычном случае сохранение ссылки на объект приводит к увеличению счетчика ссылок,
# # что препятствует уничтожению объекта, пока значение счетчика не достигнет нуля.
# # Слабая ссылка позволяет обращаться к объекту, не увеличивая его счетчик ссылок.
# # --------------------------------------------------------------------------------------------------
# # Класс WeakKeyDictionary([dict]) cоздает словарь, в котором ключи представлены слабыми ссылками.
# # Когда количество обычных ссылок на объект ключа становится равным нулю,
# # соответствующий элемент словаря автоматически удаляется.
# # В необязательном аргументе dict передается словарь, элементы которого добавляются
# # в возвращаемый объект типа WeakKeyDictionary.
# # Cлабые ссылки могут создаваться только для объектов определенных типов, поэтому
# # существует большое число ограничений на допустимые типы объектов ключей.
# # В частности, встроенные строки НЕ МОГУТ использоваться в качестве ключей со слабыми ссылками.
# # Однако экземпляры пользовательских классов, объявляющих метод __hash__(), могут играть роль ключей.
# # Экземпляры класса WeakKeyDictionary имеют два дополнительных метода, iterkeyrefs() и keyrefs(),
# # которые возвращают слабые ссылки на ключи.
#
# class Grade:
#     def __init__(self):
#         self._values = WeakKeyDictionary()
#
#     def __get__(self, instance, instance_type):
#         if instance is None: return self
#         return self._values.get(instance, 0)
#
#     def __set__(self, instance, value):
#         if not (1 <= value <= 5):
#             raise ValueError("Оценка должна быть от 1 до 5")
#         self._values[instance] = value
#
#
# class Exam():
#     ''' Класс Экзамен.
#         Для простоты хранит только оценку за экзамен
#     '''
#     grade = Grade()
#
#
# # Для демонстрации создадим два Экзамена:
# math_exam = Exam()
# math_exam.grade = 3
#
# language_exam = Exam()
# language_exam.grade = 5
#
# print("  Проверим результаты: ")
# print("Первый экзамен ", math_exam.grade, " - верно?")
# print("Второй экзамен ", language_exam.grade, " - верно?")
#
# print()
#
# # Недостаток конкретно данного решения - в одном классе нельзя сохранять данные дескрипторов одного типа.
# # Т.е., например, сделать экзамен с несколькими оценками.
#
#
# print(' ====== Хранение в __dict__ экземпляра внешнего класса =======')
#
# # Такой подход, помимо прочего, позволяет в одном внешнем классе
# # создавать несколько объектов-дескрипторов одного класса.
#
# class Grade:
#     def __init__(self, name):
#         # Для данного подхода необходимо сформировать отдельное имя атрибута,
#         # иначе при совпадении имени name и имени дескриптора
#         # создаваемый атрибут перезапишет объект дескриптора в данном экземпляре
#         self.name = '_' + name
#
#     def __get__(self, instance, instance_type):
#         if instance is None:
#             return self
#         return "*{}*".format(getattr(instance, self.name))
#
#     def __set__(self, instance, value):
#         if not (1 <= value <= 100):
#             raise ValueError("Балл ЕГЭ должен быть от 1 до 100")
#         setattr(instance, self.name, value)
#
#
# class ExamEGE():
#     ''' Комплексный экзамен, на котором оцениваются разные критерии.
#     '''
#     # Для обновлённого Grade нужно обновить и создание атрибутов, добавив строковые имена.
#     # Строковые имена могут не совпадать с именами атрибутов.
#     math_grade = Grade('math_grade')
#     writing_grade = Grade('writing_grade')
#     science_grade = Grade('science')
#
#
# # Проверим обновлённый дескриптор Оценку и объекты Экзамены.
# first_exam = ExamEGE()
# first_exam.writing_grade = 3
# first_exam.math_grade = 4
#
# print("Содержимое first_exam.__dict__:")
# print(' ', first_exam.__dict__)
#
# second_exam = ExamEGE()
# second_exam.writing_grade = 2
# second_exam.science_grade = 5
#
# print(' ', second_exam.__dict__)



#
# # -------------------------- Метаклассы ----------------------------
#
# print(' ---- Шаблон Одиночка с использованием __call__ метакласса ---- ')
#
# # Объявляем метакласс, который будет контролировать создание нового класса
# class Singleton(type):
#
#     def __init__(self, *args, **kwargs):
#         print('__init__ in Metaclass. ', self, args, kwargs)
#         self.__instance = None
#         super().__init__(*args, **kwargs)
#
#     def __call__(self, *args, **kwargs):
#         print('__call__ in Metaclass')
#         print(' ', self, args, kwargs)
#         if self.__instance is None:
#             self.__instance = super().__call__(*args, **kwargs)
#             return self.__instance
#         else:
#             return self.__instance
#
#
# class BaseA(metaclass=Singleton):
#     def __init__(self):
#         print('Class BaseA')
#
#
# class BaseB(metaclass=Singleton):
#     def __init__(self):
#         print('Class BaseB')


# a_1 = BaseA()
# a_2 = BaseA()
#
# b_1 = BaseB()
# b_2 = BaseB()
#
# print('a_1 is a_2 - ', a_1 is a_2)
# print('b_1 is b_2 - ', b_1 is b_2)
# print('a_1 is b_1 - ', a_1 is b_1)
# print('a_2 is b_2 - ', a_2 is b_2)
# print('a_1 is b_2 - ', a_1 is b_2)
# print('a_2 is b_1 - ', a_2 is b_1)





# class Pizza:
#     def __init__(self, ingredients):
#         self.ingredients = ingredients
#     def __repr__(self):
#         return f'Pizza({self.ingredients!r})'
#     @classmethod
#     def margherita(cls):
#         return cls(['mozzarella', 'tomatoes'])
#     @classmethod
#     def prosciutto(cls):
#         return cls(['mozzarella', 'tomatoes', 'ham'])
#
#
# m = Pizza.prosciutto()
# print(m.prosciutto())
# print(m.ingredients)
#
# n = Pizza.margherita()
# print(n.ingredients)




# -------------------------- Метаклассы ----------------------------

# Пример использования метода метакласса __prepare__
# Пример актуален для Python до версии 3.6 -
# в Python 3.6 __prepare__ по умолчанию возвращает OrderedDict

# class TypedProperty:
#     def __init__(self, name, type_name, default=None):
#         self.name = "_" + name
#         self.type = type_name
#         self.default = default if default else type_name()
#
#     def __get__(self, instance, cls):
#         return getattr(instance, self.name, self.default)
#
#     def __set__(self, instance, value):
#         if not isinstance(value, self.type):
#             raise TypeError("Значение должно быть типа %s" % self.type)
#         setattr(instance, self.name, value)
#
#     def __delete__(self, instance):
#         raise AttributeError("Невозможно удалить атрибут")


#
# class TypedProperty: # Не работает
#     ''' Дескриптор атрибутов, контролирующий принадлежность указанному типу '''
#     def __init__(self, type_name, default=None):
#         self.name = None
#         self.type = type_name
#         if default:
#             self.default = default
#         else:
#             self.default = type_name()
#
#     def __get__(self, instance, cls):
#         return getattr(instance, self.name, self.default)
#
#     def __set__(self, instance, value):
#         if not isinstance(value, self.type):
#             raise TypeError("Значение должно быть типа %s" % self.type)
#         setattr(instance, self.name, value)
#
#
#     def __delete__(self, instance):
#         raise AttributeError("Невозможно удалить атрибут")
#
#
#
# import collections
#
#
# print(' ------ Демонстрация работы с методом __prepare__ метакласса --------')
#
#
# class EntityMeta(type):
#     """ Метакласс для прикладных классов с контролируемыми полями
#     """
#     # Метод __prepare__ вызывается до чтения тела пользовательского класса,
#     # возвращает объект-отображение (dict-like) для хранения атрибутов класса
#     @classmethod
#     def __prepare__(cls, name, bases):
#         # Атрибуты класса будут теперь храниться в экземпляре OrderedDict
#         return collections.OrderedDict()
#
#     def __init__(cls, name, bases, clsdict):
#         super().__init__(name, bases, clsdict)
#
#         # Aтрибут _fieid_names создаётся в конструируемом классе
#         cls._field_names = []
#         for key, attr in clsdict.items():
#             if isinstance(attr, TypedProperty):
#                 # Заполняем список только атрибутами типа TypedProperty
#                 type_name = type(attr).__name__
#                 attr.name = '_{}_{}'.format(type_name, key)
#                 cls._field_names.append((key, attr.name))
#
#
# class Entity(metaclass=EntityMeta):
#     """ Прикладной класс с контролируемыми полями
#     """
#     @classmethod
#     def field_names(cls):
#         ''' Просто возвращает поля в порядке добавления '''
#         for name in cls._field_names:
#             yield name
#
#
# class LineItem(Entity):
#     ''' Класс-пример со множеством атрибутов
#     '''
#     reading_short = TypedProperty(int, 13)
#     description_very_long = TypedProperty(str, 'Simple Line')
#     here_are_numerous_simple = TypedProperty(int, 1)
#     price_ho_ho = TypedProperty(float, 19.99)
#     after_the_introduction = TypedProperty(int, 73)
#     await_it_is_not_a_weight = TypedProperty(int, 3)
#
#
# print('Атрибуты пользовательского класса: ')



#
# class TypedProperty_v1:
#     def __init__(self, name, type_name, default=None):
#         self.name = "_" + name
#         self.type = type_name
#         self.default = default if default else type_name()
#
#     def __get__(self, instance, cls):
#         return getattr(instance, self.name, self.default)
#
#     def __set__(self, instance, value):
#         if not isinstance(value, self.type):
#             raise TypeError("Значение должно быть типа %s" % self.type)
#         setattr(instance, self.name, value)
#
#     def __delete__(self, instance):
#         raise AttributeError("Невозможно удалить атрибут")
#
#
# class Foo:
#     name = TypedProperty_v1("name", str)
#     num = TypedProperty_v1("num", int, 42)
#
#
# if __name__ == '__main__':
#     f = Foo()
#     a = f.name          # Неявно вызовет Foo.name.__get__(f,Foo)
#     f.name = "Гвидо"    # Вызовет Foo.name.__set__(f,”Guido”)
#     # del f.name          # Вызовет Foo.name.__delete__(f)
#
#
# class TypedProperty_v2:
#     ''' Дескриптор атрибутов, контролирующий принадлежность указанному типу
#     '''
#     def __init__(self, type_name, default=None):
#         self.name = None
#         self.type = type_name
#         if default:
#             self.default = default
#         else:
#             self.default = type_name()
#
#     def __get__(self, instance, cls):
#         return getattr(instance, self.name, self.default)
#
#     def __set__(self, instance, value):
#         if not isinstance(value, self.type):
#             raise TypeError("Значение должно быть типа %s" % self.type)
#         setattr(instance, self.name, value)
#
#     def __delete__(self, instance):
#         raise AttributeError("Non delete attribute")



class Foo:
    __slots__ = ['foo', 'bar', 'baz']


foo = Foo()
foo.baz = 'spam'