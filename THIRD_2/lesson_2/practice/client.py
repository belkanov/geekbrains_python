import argparse
import json
import logging
import socket
import sys
from threading import Thread
from time import sleep

from common.utils import (
    send_message,
    get_message,
)
from common.variables import (
    ACTION,
    ACTION_MSG,
    DEFAULT_IP,
    DEFAULT_PORT,
    DEFAULT_USERNAME,
    ERROR,
    FROM,
    MESSAGE,
    RESPONSE,

    get_jim_presence,
    get_jim_send_msg,
)

import log_config.client
LOG = logging.getLogger('app.client')


def process_srv_msg(message: dict):
    LOG.debug('process_srv_msg: %s', message)
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            LOG.debug('200: OK')
            return
        LOG.debug(f'400: {message[ERROR]}')
        return
    elif ACTION in message:
        if message.get(ACTION) == ACTION_MSG:
            msg = f'{message.get(FROM)}: {message.get(MESSAGE)}'
            LOG.debug(msg)
            return msg
    else:
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
        help='детальные логи'
    )
    arg_parser.add_argument(
        '-s',
        action='store_true',
        default=False,
        help='запустить клиент в режиме отправки сообщений'
    )
    arg_parser.add_argument(
        '-u',
        metavar='USER_NAME',
        type=str,
        default=DEFAULT_USERNAME,
        help='Отображаемое имя в чате'
    )
    args = arg_parser.parse_args()
    if not (1024 <= args.p <= 65535):
        raise ValueError('Порт должен быть в диапазоне [1024, ..., 65535]')
    return args


def processing_input(server_socket, client_name):
    """
    По умолчанию - сообщение отправляется всем.
    Для указания конкретного получателя:
      - если пользователь - пишем его через @. Пример:
        @user1 сообщение получит только user1
      - если комната - пишем через #. Пример:
        #room1 сообщение получат все участники комнаты room1

    Управляющие команды начинаются с \\ (одиночный бэкслэш). Пример:
      - \\q - выключить клиент
      - \\j [#room_name] - подключиться к комнате #room_name
      - \\l [#room_name] - выйти из комнаты #room_name
    """

    while True:
        msg_to_srv = ''
        while msg_to_srv.strip() == '':
            msg_to_srv = input()

        if msg_to_srv.startswith('\\q'):
            break
        elif msg_to_srv.startswith('\\j'):
            LOG.info('Извините. Функционал еще не поддерживается =(')
        elif msg_to_srv.startswith('\\l'):
            LOG.info('Извините. Функционал еще не поддерживается =(')
        elif msg_to_srv.startswith('@'):
            LOG.info('Извините. Функционал еще не поддерживается =(')
        elif msg_to_srv.startswith('#'):
            LOG.info('Извините. Функционал еще не поддерживается =(')
        else:
            LOG.debug('send msg to #all: %s', msg_to_srv)
            send_message(server_socket, get_jim_send_msg(msg_to_srv, client_name, None))


def processing_output(server_socket, client_name):
    while True:
        try:
            srv_msg = process_srv_msg(get_message(server_socket))
            if srv_msg:
                print(srv_msg)
        except (ValueError, json.JSONDecodeError):
            LOG.error('Не удалось обработать ответ сервера')
        except SystemExit:
            print('---- EXIT ---')


def main():
    client_args = parse_client_args()
    if client_args.v != 0:
        LOG.setLevel(logging.DEBUG)

    LOG.debug('create socket')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv_socket:
        LOG.debug('connect to %(a)s:%(p)s', vars(client_args))
        srv_socket.connect((client_args.a, client_args.p))

        # presence надо отправить в любом случае - слушаем мы или отправляем
        LOG.debug('create presence')
        presence = get_jim_presence(client_args.u)
        LOG.debug('send presence: %s', presence)
        send_message(srv_socket, presence)
        srv_msg = process_srv_msg(get_message(srv_socket))
        LOG.info(srv_msg)

        LOG.debug('Create input_thread')
        input_thread = Thread(target=processing_input, args=(srv_socket, client_args.u))
        input_thread.daemon = True
        input_thread.start()
        LOG.debug('input_thread started')

        LOG.debug('Create output_thread')
        output_thread = Thread(target=processing_output, args=(srv_socket, client_args.u))
        output_thread.daemon = True
        output_thread.start()
        LOG.debug('output_thread started')

        while True:
            sleep(1)
            if input_thread.is_alive() and output_thread.is_alive():
                continue
            break


if __name__ == '__main__':
    LOG.info('----- start app')
    main()
    LOG.info('----- end app')
