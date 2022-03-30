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

import log_config.server
LOG = logging.getLogger('app.server')


def process_request(request):
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
    if not (1024 <= args.p <= 65535):
        raise ValueError('Порт должен быть в диапазоне [1024, ..., 65535]')

    return args


def read_requests(r_clients, all_clients):
    requests = {}
    for client_socket in r_clients:
        try:
            data = get_message(client_socket)
            requests[client_socket] = data
        except Exception as e:
            print(f'Клиент {client_socket.fileno()} {client_socket.getpeername()} отключился')
            all_clients.remove(client_socket)

    return requests


def write_requests(requests, w_clients, all_clients, messages_list):
    for client_socket in requests:
        request_data = requests[client_socket]
        response, msg = process_request(request_data)
        if msg:
            messages_list.append(msg)

        if client_socket in w_clients:
            try:
                send_message(client_socket, response)
            except Exception as e:
                print(f'Клиент {client_socket.fileno()} {client_socket.getpeername()} отключился')
                client_socket.close()
                all_clients.remove(client_socket)


def write_messages(msg_list, w_clients, all_clients):
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


def main():
    srv_args = parse_srv_args()
    if srv_args.v != 0:
        LOG.setLevel(logging.DEBUG)

    LOG.debug('create socket')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as transport:
        transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        LOG.debug('bind socket to %(a)s:%(p)s', vars(srv_args))
        transport.bind((srv_args.a, srv_args.p))

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
                requests = read_requests(r, clients)
                write_requests(requests, w, clients, msg_list)
                write_messages(msg_list, w, clients)


if __name__ == '__main__':
    LOG.info('----- start app')
    main()
    LOG.info('----- end app')
