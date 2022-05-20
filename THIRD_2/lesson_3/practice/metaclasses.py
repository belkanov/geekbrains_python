import dis
from socket import socket


def get_methods_and_attrs(clsdict):
    methods = []
    attrs = []

    for func in clsdict:
        try:
            ret = dis.get_instructions(clsdict[func])
        except TypeError:
            pass
        else:
            for i in ret:
                if i.opname == 'LOAD_GLOBAL':
                    if i.argval not in methods:
                        methods.append(i.argval)
                elif i.opname == 'LOAD_ATTR':
                    if i.argval not in attrs:
                        attrs.append(i.argval)

    return methods, attrs


class ServerMaker(type):
    def __init__(self, clsname, bases, clsdict):
        methods, attrs = get_methods_and_attrs(clsdict)

        if 'connect' in methods:
            raise TypeError('Использование метода connect недопустимо в серверном классе')
        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Некорректная инициализация сокета.')
        super().__init__(clsname, bases, clsdict)


class ClientMaker(type):
    def __init__(self, clsname, bases, clsdict):
        methods, _ = get_methods_and_attrs(clsdict)

        for value in clsdict.values():
            if isinstance(value, socket):
                raise ValueError('Нельзя создавать сокеты на уровне класса')
        for command in ('accept', 'listen'):
            if command in methods:
                raise TypeError('В классе обнаружено использование запрещённого метода')
        if 'get_message' in methods or 'send_message' in methods:
            pass
        else:
            raise TypeError('Отсутствуют вызовы функций, работающих с сокетами.')
        super().__init__(clsname, bases, clsdict)
