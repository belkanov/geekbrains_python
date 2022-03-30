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

import server
from common.variables import (
    ACCOUNT_NAME,
    ACTION,
    PRESENCE,
    RESPONSE,
    USER,
    ERROR,
    DEFAULT_PORT,
    TIME,
)


class TestClient(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @staticmethod
    def get_base_msg_for_process_client_msg():
        return {
            RESPONSE: 0
        }

    def test_process_client_msg_200(self):
        test_msg = TestClient.get_base_msg_for_process_client_msg()
        test_msg[RESPONSE] = 200
        client_msg = {
            ACTION: PRESENCE,
            # на значение времени сервер не смотрит, смотрит только ключ,
            # поэтому такое значение пока норм.
            TIME: None,
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        }

        self.assertEqual(server.process_client_msg(client_msg), test_msg)

    # Сервер проверяет 5 условий сразу, вариантов можно сделать много.
    # Я решил ограничиться одним.
    def test_process_client_msg_not_200(self):
        test_msg = TestClient.get_base_msg_for_process_client_msg()
        test_msg[RESPONSE] = 400
        test_msg[ERROR] = 'Bad request'
        client_msg = {
            ACTION: PRESENCE,
            # TIME: None,
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        }

        self.assertEqual(server.process_client_msg(client_msg), test_msg)

    @patch.object(sys, 'argv', [''])
    def test_parse_client_args_default_addr(self):
        test_args = server.parse_srv_args()

        self.assertEqual(test_args.a, '')

    @patch.object(sys, 'argv', [''])
    def test_parse_client_args_default_port(self):
        test_args = server.parse_srv_args()

        self.assertEqual(test_args.p, DEFAULT_PORT)

    @patch.object(sys, 'argv', ['', '-a', '28.28.28.28'])
    def test_parse_client_args_custom_addr(self):
        test_args = server.parse_srv_args()

        self.assertEqual(test_args.a, '28.28.28.28')

    @patch.object(sys, 'argv', ['', '-p', '7000'])
    def test_parse_client_args_custom_port(self):
        test_args = server.parse_srv_args()

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
                server.parse_srv_args()

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
                server.parse_srv_args()

        e_context = e.exception.__context__  # <argparse.ArgumentError>
        conditions = [e_context.argument_name == '-p',
                      e_context.message == 'expected one argument',
                      ]

        self.assertTrue(all(conditions))


if __name__ == '__main__':
    main()
