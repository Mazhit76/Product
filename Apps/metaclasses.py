import dis

from tabulate import tabulate


class ServerMaker(type):
    """
    clsname: экземпля класа Server
    bases: кортеж базовых классов
    clsdict: словарь атрибутов и методов экземпляра метакласа
    return: None

    """
    def __init__(self, clsname, bases, clsdict):
        # Lists is methods, which use in functions class
        methods = []
        # Attribute, use in function classes
        attrs = []
        # looping through the keys
        for func in clsdict:
            try:
                # return an iterator oder tht instructions in the provided function, method,
                # line code or object off code
                ret = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for i in ret:
                    print(i)
                    # opname- name for operation
                    if i.opname == 'LOAD_GLOBAL':
                        # fill the list with methods used in class functions
                        if i.argval not in methods:
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        # fill the list with attributes used in class functions
                        if i.argval not in attrs:
                            attrs.append(i.argval)
        print(methods)
    #     if an invalid connect method is detected throw an exception
        if 'connect' in methods:
            raise TypeError('Use of connect method is invalid on server class')
        if not ('SOCK_STREAM' in attrs) and ('AF_INET' in attrs):
            raise TypeError('Incorrect socket initialization')
    #     Be sure to call ancestor constructor
        super().__init__(clsname,bases,clsdict)




class ClientMaker(type):
    def __init__(self, clsname, bases, clsdict):

        methods = []
        # Attribute, use in function classes
        attrs = []
        for func in clsdict:
            try:
                # return an iterator oder tht instructions in the provided function, method,
                # line code or object off code
                ret = dis.get_instructions(clsdict[func])
            except TypeError:
                pass
            else:
                for i in ret:
                    print(i)
                    # opname- name for operation
                    if i.opname == 'LOAD_GLOBAL':
                        # fill the list with methods used in class functions
                        if i.argval not in methods:
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_ATTR':
                        # fill the list with attributes used in class functions
                        if i.argval not in attrs:
                            attrs.append(i.argval)
        print(methods)
#       If the use an invalid accept, list, socket method throw an exception
        for command in ('accept', 'listen', 'socket'):
            if command in methods:
                raise TypeError('The use of a forbidden method was detected in the class')
        #     Calling get_message or send_message from utils is considered correct socket usage
        if 'create_message' in clsdict and 'message_from_server' in clsdict:
            pass
        else:
            raise TypeError('There are no calls to functions that work with sockets')
        super().__init__(clsname, bases, clsdict)

