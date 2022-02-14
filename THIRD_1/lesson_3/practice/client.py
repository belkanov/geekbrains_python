import argparse
import json
import socket

from common.variables import (
    get_base_msg,
    USER,
    ACCOUNT_NAME,
    RESPONSE,
    ERROR,
    DEFAULT_PORT,
    ACTION,
    PRESENCE,
)
from common.utils import (
    send_message,
    get_message,
)


def create_presence(acc_name='Guest'):
    presence_msg = get_base_msg()
    presence_msg[ACTION] = PRESENCE
    presence_msg[USER] = {
        ACCOUNT_NAME: acc_name
    }
    return presence_msg


def process_srv_msg(message: dict):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200: OK'
        return f'400: {message[ERROR]}'
    raise ValueError


def parse_client_args():
    arg_parser = argparse.ArgumentParser(
        description='Simple client for GeekBrains\' course "Клиент-серверные приложения на Python"'
    )
    arg_parser.add_argument(
        '-a',
        metavar='IPv4',
        type=str,
        default='127.0.0.1',
        help=f'IP-адрес для покдлючения (по умолчанию 127.0.0.1)'
    )
    arg_parser.add_argument(
        '-p',
        metavar='PORT',
        type=int,
        default=DEFAULT_PORT,
        help=f'TCP-порт для работы (по умолчанию: {DEFAULT_PORT}, должен быть 1024 <= PORT <= 65535)'
    )
    args = arg_parser.parse_args()
    if not (1024 <= args.p <= 65535):
        raise ValueError('Порт должен быть в диапазоне [1024, ..., 65535]')
    return args


def main():
    client_args = parse_client_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as transport:
        transport.connect((client_args.a, client_args.p))

        msg_to_srv = create_presence()
        send_message(transport, msg_to_srv)

        try:
            srv_answer = process_srv_msg(get_message(transport))
            print(srv_answer)
        except (ValueError, json.JSONDecodeError):
            print('Не удалось обработать ответ сервера')


if __name__ == '__main__':
    main()
