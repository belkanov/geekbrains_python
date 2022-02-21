import json
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


def process_client_msg(message):
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
    args = arg_parser.parse_args()
    if not (1024 <= args.p <= 65535):
        raise ValueError('Порт должен быть в диапазоне [1024, ..., 65535]')

    return args


def main():
    srv_args = parse_srv_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as transport:
        transport.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        transport.bind((srv_args.a, srv_args.p))

        transport.listen(MAX_CONNECTIONS)

        while True:
            client, client_addr = transport.accept()
            with client:
                try:
                    msg_from_client = get_message(client)
                    print(msg_from_client)
                    response = process_client_msg(msg_from_client)
                    send_message(client, response)
                except (ValueError, json.JSONDecodeError):
                    print('Принято некорректное сообщение от клиента.')


if __name__ == '__main__':
    main()
