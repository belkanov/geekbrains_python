import json
import logging
import socket
import select
from copy import deepcopy

from common.variables import (
    ACCOUNT_NAME,
    ACTION,
    ACTION_PRESENCE,
    ACTION_MSG,
    DEFAULT_PORT,
    MAX_CONNECTIONS,
    TIME,
    USER,
    TO,
    FROM,

    get_jim_response_error,
    get_jim_response,
    ENCODING,
    MESSAGE,
)
from common.utils import (
    get_message,
    send_message,
)
import argparse
from metaclasses import ServerMaker
from descriptors import Port

import log_config.server
LOG = logging.getLogger('app.server')


def parse_srv_args():
    LOG.debug('start parse arguments')
    arg_parser = argparse.ArgumentParser(
        description='Simple server for GeekBrains\' course "Клиент-серверные приложения на Python"'
    )
    arg_parser.add_argument(
        '-a',
        metavar='IPv4',
        type=str,
        default='',
        help=f'IP-адрес для прослушивания (по умолчанию слушает все доступные адреса)'
    )
    arg_parser.add_argument(
        '-p',
        metavar='PORT',
        type=int,
        default=DEFAULT_PORT,
        help=f'TCP-порт для работы (по умолчанию: {DEFAULT_PORT}, должен быть 1024 <= PORT <= 65535)'
    )
    arg_parser.add_argument(
        '-v',
        action='count',
        default=0,
        help=f'детальные логи'
    )
    args = arg_parser.parse_args()

    if args.v != 0:
        LOG.setLevel(logging.DEBUG)

    return args


class Server(metaclass=ServerMaker):
    port = Port()

    def __init__(self, args):
        self.addr = args.a
        self.port = args.p

    def process_request(self, request):
        LOG.debug('process_client_msg: %s', request)

        response = get_jim_response_error(400, 'Bad request')
        msg = None

        if not (ACTION in request and
                TIME in request
        ):
            pass
        elif request[ACTION] == ACTION_PRESENCE:
            if (USER in request and
                    request[USER][ACCOUNT_NAME] == 'Guest'
            ):
                response = get_jim_response(200)
        elif request[ACTION] == ACTION_MSG:
            if (TO in request and
                    FROM in request and
                    ENCODING in request and
                    MESSAGE in request
            ):
                response = get_jim_response(200)
                msg = request

        return response, msg

    def read_requests(self, r_clients, all_clients):
        requests = {}
        for client_socket in r_clients:
            try:
                data = get_message(client_socket)
                requests[client_socket] = data
            except Exception as e:
                print(f'Клиент {client_socket.fileno()} {client_socket.getpeername()} отключился')
                all_clients.remove(client_socket)

        return requests

    def write_requests(self, requests, w_clients, all_clients, messages_list):
        for client_socket in requests:
            request_data = requests[client_socket]
            response, msg = self.process_request(request_data)
            if msg:
                messages_list.append(msg)

            if client_socket in w_clients:
                try:
                    send_message(client_socket, response)
                except Exception as e:
                    print(f'Клиент {client_socket.fileno()} {client_socket.getpeername()} отключился')
                    client_socket.close()
                    all_clients.remove(client_socket)

    def write_messages(self, msg_list, w_clients, all_clients):
        msg_list_copy = deepcopy(msg_list)
        for msg in msg_list_copy:
            for client_socket in w_clients:
                try:
                    send_message(client_socket, msg)
                except Exception as e:
                    print(f'Клиент {client_socket.fileno()} {client_socket.getpeername()} отключился')
                    client_socket.close()
                    all_clients.remove(client_socket)
            msg_list.remove(msg)

    def main_loop(self, ):
        LOG.debug('create socket')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as transport:
            transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            LOG.debug('bind socket to %(a)s:%(p)s', self.addr, self.port)
            transport.bind((self.addr, self.port))

            LOG.debug('start listening')
            transport.listen(MAX_CONNECTIONS)
            transport.settimeout(0.2)

            clients = []
            msg_list = []

            while True:
                try:
                    client, client_addr = transport.accept()
                except OSError as e:
                    pass  # timeout
                else:
                    LOG.info(f'Получен запрос на соединение от {client_addr}')
                    clients.append(client)
                finally:
                    if not clients:
                        continue

                    r = []
                    w = []
                    try:
                        r, w, _ = select.select(clients, clients, [], 0)
                    except Exception as e:
                        print(f'Кто-то отключился\n{e}')

                    if not r:
                        continue
                    requests = self.read_requests(r, clients)
                    self.write_requests(requests, w, clients, msg_list)
                    self.write_messages(msg_list, w, clients)


def main():
    args = parse_srv_args()
    server = Server(args)
    server.main_loop()


if __name__ == '__main__':
    LOG.info('----- start app')
    main()
    LOG.info('----- end app')
