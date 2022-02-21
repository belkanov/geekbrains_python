from time import time

# Project default params
DEFAULT_PORT = 7777
DEFAULT_IP = '127.0.0.1'
MAX_CONNECTIONS = 5
MAX_PACKAGE_LENGTH = 1024
ENCODING = 'utf-8'

# JIM, basic keys
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'

# JIM, misc keys
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
RESPONSE_DEFAULT_IP = 'response_default_ip'


# JIM, msg templates
def get_base_msg():
    return {
        ACTION: '',
        TIME: time()
    }


def get_base_response():
    return {
        RESPONSE: ''
    }
