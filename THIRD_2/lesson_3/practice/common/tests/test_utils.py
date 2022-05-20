import json
import socket
import sys
from pathlib import Path
# from unittest import (
#     TestCase,
#     main,
# )
import unittest

sys.path.append(str(Path('..').resolve()))

from common.variables import (
    DEFAULT_IP,
    DEFAULT_PORT,
    MAX_CONNECTIONS,
    ENCODING,
)
from common.utils import (
    get_message,
    send_message,
)


class TestClient(unittest.TestCase):
    def setUp(self):
        self.srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srv_socket.bind((DEFAULT_IP, DEFAULT_PORT))
        self.srv_socket.listen(MAX_CONNECTIONS)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((DEFAULT_IP, DEFAULT_PORT))

        self.client_to_srv, client_addr = self.srv_socket.accept()

    def tearDown(self):
        self.client_to_srv.close()
        self.client_socket.close()
        self.srv_socket.close()

    def test_get_message_ok(self):
        msg = {'tst_key': 'tst_value ₽'}
        json_msg = json.dumps(msg)
        outcoming_encoded_msg = json_msg.encode(ENCODING)
        self.client_socket.send(outcoming_encoded_msg)
        incoming_msg = get_message(self.client_to_srv)

        self.assertEqual(incoming_msg, msg)

    def test_get_message_not_dict(self):
        msg = [{'tst_key': 'tst_value ₽'}]
        json_msg = json.dumps(msg)
        outcoming_encoded_msg = json_msg.encode(ENCODING)
        self.client_socket.send(outcoming_encoded_msg)

        self.assertRaises(ValueError, get_message, self.client_to_srv)

    def test_get_message_not_bytes(self):
        # Учитывая, что self.client_socket.send() будет ругаться, если ему отдать не байты -
        # нет идей как проверить get_message на получение чего-то не байтового.
        # Возможно через сторонний софт или что-то более низкого уровня на питоне - копать не стал
        pass

    def test_send_message_ok(self):
        msg = {'tst_key': 'tst_value ₽'}
        send_message(self.client_socket, msg)
        # будем считать, что если тесты выше пройдены - то get_message работает нормально
        incoming_msg = get_message(self.client_to_srv)

        self.assertEqual(incoming_msg, msg)

    def test_send_message_not_json_serializable(self):
        msg = {1, 2, 3}

        self.assertRaises(TypeError, send_message, self.client_socket, msg)


if __name__ == '__main__':
    unittest.main()
