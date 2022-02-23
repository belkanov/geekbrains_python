import json
import logging
import socket

from common.variables import (
    ACTION,
    PRESENCE,
    TIME,
    USER,
    ACCOUNT_NAME,
    get_base_response,
    RESPONSE,
    ERROR,
    DEFAULT_PORT,
    MAX_CONNECTIONS,
)
from common.utils import (
    get_message,
    send_message,
)
import argparse

import log_config.server
LOG = logging.getLogger('app.server')


def process_client_msg(message):
    LOG.debug('process_client_msg: %s', message)
    response_msg = get_base_response()

    if all((ACTION in message,
            message[ACTION] == PRESENCE,
            TIME in message,
            USER in message,
            message[USER][ACCOUNT_NAME] == 'Guest'
            )):
        response_msg[RESPONSE] = 200
    else:
        response_msg[RESPONSE] = 400
        response_msg[ERROR] = 'Bad request'

    return response_msg


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


def main():
    srv_args = parse_srv_args()
    if srv_args.v == 0:
        LOG.setLevel(logging.INFO)

    LOG.debug('create socket')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as transport:
        transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        LOG.debug('bind socket to %(a)s:%(p)s', vars(srv_args))
        transport.bind((srv_args.a, srv_args.p))

        LOG.debug('start listening')
        transport.listen(MAX_CONNECTIONS)

        while True:
            LOG.debug('waiting for client...')
            client, client_addr = transport.accept()
            with client:
                try:
                    LOG.debug('get msg from %s', client)
                    msg_from_client = get_message(client)
                    LOG.info('msg: %s', msg_from_client)
                    LOG.debug('process_client_msg()')
                    response = process_client_msg(msg_from_client)
                    LOG.debug('send response: %s', response)
                    send_message(client, response)
                except (ValueError, json.JSONDecodeError):
                    LOG.error('Принято некорректное сообщение от клиента.')


if __name__ == '__main__':
    LOG.info('----- start app')
    main()
    LOG.info('----- end app')
