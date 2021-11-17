import logging
import sys


import traceback
import inspect


class Log:
    """Класс-декоратор"""

    def __init__(self):
        # See name apps, where the appeal to us
        if sys.argv[0].find('client') == -1:
            self.LOG = logging.getLogger('server')
        else:
            self.LOG = logging.getLogger('client')

    def __call__(self, func_to_log):
        def decorated(*args, **kwargs):
            """Обертка"""
            res = func_to_log(*args, **kwargs)
            self.LOG.debug(f'Был вызов f(x): {func_to_log.__name__} с параметрами: {args}{kwargs}'
                           f'из модуля: {func_to_log.__module__}, функции {traceback.format_stack()[0].strip().split()[-1]}.'
                           f'вызов из функции: {inspect.stack()[1][3]}')
            return res

        return decorated
