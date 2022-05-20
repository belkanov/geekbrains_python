from time import time

# Project default params
DEFAULT_PORT = 7777
DEFAULT_IP = '127.0.0.1'
MAX_CONNECTIONS = 5
MAX_PACKAGE_LENGTH = 1024
DEFAULT_ENCODING = 'utf-8'
DEFAULT_USERNAME = 'Guest'

# JIM, basic keys
ACTION = 'action'
RESPONSE = 'response'
ERROR = 'error'
ALERT = 'alert'
TIME = 'time'
TYPE = 'type'
USER = 'user'
ACCOUNT_NAME = 'account_name'
RESPONSE_DEFAULT_IP = 'response_default_ip'
TO = 'to'
FROM = 'from'
ENCODING = 'encoding'
ROOM = 'room'
MESSAGE = 'message'

# JIM, actions
ACTION_PRESENCE = 'presence'  # присутствие. Сервисное сообщение для извещения сервера о присутствии клиента online
ACTION_PROBE = 'probe'  # проверка присутствия. Сервисное сообщение от сервера для проверки присутствии клиента online
ACTION_MSG = 'msg'  # простое сообщение пользователю или в чат;
ACTION_JOIN = 'join'  # присоединиться к чату
ACTION_LEAVE = 'leave'  # покинуть чат
ACTION_AUTH = 'authenticate'  # авторизация на сервере
ACTION_QUIT = 'quit'  # отключение от сервера


def get_jim_response(response_code):
    return {
        RESPONSE: response_code
    }


def get_jim_response_alert(response_code, alert_msg):
    return {
        RESPONSE: response_code,
        ALERT: alert_msg
    }


def get_jim_response_error(response_code, error_msg):
    return {
        RESPONSE: response_code,
        ERROR: error_msg
    }


def get_jim_presence(acc_name):
    return {
        ACTION: ACTION_PRESENCE,
        TIME: time(),
        USER: {
            ACCOUNT_NAME: acc_name
        }
    }


def get_jim_send_msg(msg, from_name, to_name):
    return {
        ACTION: ACTION_MSG,
        TIME: time(),
        TO: to_name or '#all',
        FROM: from_name,
        ENCODING: DEFAULT_ENCODING,
        MESSAGE: msg
    }


def get_jim_join_chatroom(chatroom_name):
    return {
        ACTION: ACTION_JOIN,
        TIME: time(),
        ROOM: chatroom_name
    }


def get_jim_leave_chatroom(chatroom_name):
    return {
        ACTION: ACTION_LEAVE,
        TIME: time(),
        ROOM: chatroom_name
    }
