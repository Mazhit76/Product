import logging

LOG = logging.getLogger('server')


class Port:
    # __slots__ = 'name'
    # def __init__(self, name_):
    #     self.name = name_


    def __set__(self, instance, value):
        """
        :param instance: Server.object
        :param value: port address: must value 1023:655636
        :return: None
        """
        if not 1023 < value < 65536:
            LOG.critical(f' Запуск сервера с портом: {value}, вне диапазона 1024:655635 недопустим!!!')
            exit(1)
        instance.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        """
        :param owner: class Server
        :param name: port
        :return: None
        """
        self.name = name


