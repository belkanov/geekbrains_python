import contextlib
from io import StringIO
import sys
from pathlib import Path
from unittest import (
    TestCase,
    main,
)
from unittest.mock import patch

sys.path.append(str(Path('..').resolve()))

import client
from common.variables import (
    ACCOUNT_NAME,
    ACTION,
    PRESENCE,
    RESPONSE,
    USER,
    ERROR,
    DEFAULT_IP,
    DEFAULT_PORT,
    get_base_msg,
)


class TestClient(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def get_base_msg_for_process_srv_msg():
        return {
            RESPONSE: 0
        }

    def test_create_presence(self):
        test_presence = client.create_presence()

        check_presence = get_base_msg()
        check_presence[ACTION] = PRESENCE
        check_presence[USER] = {
            ACCOUNT_NAME: 'Guest'  # другие имена пока не проверяем
        }

        self.assertEqual(test_presence, check_presence)

    def test_process_srv_msg_200(self):
        test_msg = TestClient.get_base_msg_for_process_srv_msg()
        test_msg[RESPONSE] = 200

        self.assertEqual(client.process_srv_msg(test_msg), '200: OK')

    def test_process_srv_msg_not_200(self):
        test_msg = TestClient.get_base_msg_for_process_srv_msg()
        test_msg[RESPONSE] = 222
        error_txt = 'error text'
        test_msg[ERROR] = error_txt

        self.assertEqual(client.process_srv_msg(test_msg), f'400: {error_txt}')

    def test_process_srv_msg_no_response(self):
        test_msg = {
            'not_response_key': None
        }

        self.assertRaises(ValueError, client.process_srv_msg, test_msg)

    @patch.object(sys, 'argv', [''])
    def test_parse_client_args_default_addr(self):
        test_args = client.parse_client_args()

        self.assertEqual(test_args.a, DEFAULT_IP)

    @patch.object(sys, 'argv', [''])
    def test_parse_client_args_default_port(self):
        test_args = client.parse_client_args()

        self.assertEqual(test_args.p, DEFAULT_PORT)

    @patch.object(sys, 'argv', ['', '-a', '28.28.28.28'])
    def test_parse_client_args_custom_addr(self):
        test_args = client.parse_client_args()

        self.assertEqual(test_args.a, '28.28.28.28')

    @patch.object(sys, 'argv', ['', '-p', '7000'])
    def test_parse_client_args_custom_port(self):
        test_args = client.parse_client_args()

        self.assertEqual(test_args.p, 7000)

    @patch.object(sys, 'argv', ['', '-a'])
    def test_parse_client_args_no_addr(self):
        """
        Шаманство ниже требуется, чтобы отловить именно
        argparse.ArgumentError: argument -a: expected one argument

        unittest затирает стэктрейс и мы видим только конечный эксепшн (SystemExit).
        Багу знают:
        https://bugs.python.org/issue24959
        Есть пул-реквест на фикс, но он пока открыт (на 20.02.2022)
        """

        # ioerr - не обязателен
        # без него лезут описания ошибок из ArgumentError
        ioerr = StringIO()
        with contextlib.redirect_stderr(ioerr):
            with self.assertRaises(SystemExit) as e:
                client.parse_client_args()

        e_context = e.exception.__context__  # <argparse.ArgumentError>
        conditions = [e_context.argument_name == '-a',
                      e_context.message == 'expected one argument',
                      ]

        self.assertTrue(all(conditions))

    @patch.object(sys, 'argv', ['', '-p'])
    def test_parse_client_args_no_port(self):
        ioerr = StringIO()
        with contextlib.redirect_stderr(ioerr):
            with self.assertRaises(SystemExit) as e:
                client.parse_client_args()

        e_context = e.exception.__context__  # <argparse.ArgumentError>
        conditions = [e_context.argument_name == '-p',
                      e_context.message == 'expected one argument',
                      ]

        self.assertTrue(all(conditions))


if __name__ == '__main__':
    main()
