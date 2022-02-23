import argparse
import json
import logging
import socket

from common.variables import (
    get_base_msg,
    USER,
    ACCOUNT_NAME,
    RESPONSE,
    ERROR,
    DEFAULT_IP,
    DEFAULT_PORT,
    ACTION,
    PRESENCE,
)
from common.utils import (
    send_message,
    get_message,
)

import log_config.client
LOG = logging.getLogger('app.client')


def create_presence(acc_name='Guest'):
    LOG.debug('create presence message')
    presence_msg = get_base_msg()
    presence_msg[ACTION] = PRESENCE
    presence_msg[USER] = {
        ACCOUNT_NAME: acc_name
    }
    return presence_msg


def process_srv_msg(message: dict):
    LOG.debug('process_srv_msg: %s', message)
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200: OK'
        return f'400: {message[ERROR]}'
    raise ValueError


def parse_client_args():
    LOG.debug('start parse arguments')
    arg_parser = argparse.ArgumentParser(
        description='Simple client for GeekBrains\' course "Клиент-серверные приложения на Python"'
    )
    arg_parser.add_argument(
        '-a',
        metavar='IPv4',
        type=str,
        default=DEFAULT_IP,
        help=f'IP-адрес для покдлючения (по умолчанию {DEFAULT_IP})'
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
    client_args = parse_client_args()
    if client_args.v == 0:
        LOG.setLevel(logging.INFO)

    LOG.debug('create socket')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as transport:
        LOG.debug('connect to %(a)s:%(p)s', vars(client_args))
        transport.connect((client_args.a, client_args.p))

        LOG.debug('create_presence()')
        msg_to_srv = create_presence()
        LOG.debug('send msg: %s', msg_to_srv)
        send_message(transport, msg_to_srv)

        try:
            LOG.debug('process_srv_msg()')
            srv_answer = process_srv_msg(get_message(transport))
            LOG.info(srv_answer)
        except (ValueError, json.JSONDecodeError):
            LOG.error('Не удалось обработать ответ сервера')


if __name__ == '__main__':
    LOG.info('----- start app')
    main()
    LOG.info('----- end app')
