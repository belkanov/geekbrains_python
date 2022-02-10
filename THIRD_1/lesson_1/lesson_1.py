import platform
import subprocess
from pathlib import Path

import chardet


def print_info_str(*args):
    print('\n\n')
    print('*' * 20, *args, '*' * 20)


def func_1():
    """
    1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате
    и проверить тип и содержание соответствующих переменных.
    Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode
    и также проверить тип и содержимое переменных.
    """
    print_info_str('# 1')

    word_1_str = 'разработка'
    word_2_str = 'сокет'
    word_3_str = 'декоратор'
    word_1_utf = '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430'
    word_2_utf = '\u0441\u043e\u043a\u0435\u0442'
    word_3_utf = '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440'

    print(f'{isinstance(word_1_str, str)=}')
    print(f'{isinstance(word_2_str, str)=}')
    print(f'{isinstance(word_3_str, str)=}')
    print(f'{isinstance(word_1_utf, str)=}')
    print(f'{isinstance(word_2_utf, str)=}')
    print(f'{isinstance(word_3_utf, str)=}')

    print(f'{(word_1_str == "разработка")=}')
    print(f'{(word_2_str == "сокет")=}')
    print(f'{(word_3_str == "декоратор")=}')
    print(f'{(word_1_utf == "разработка")=}')
    print(f'{(word_2_utf == "сокет")=}')
    print(f'{(word_3_utf == "декоратор")=}')


def func_2(*args):
    """
    2. Каждое из слов «class», «function», «method» записать в байтовом типе без
    преобразования в последовательность кодов (не используя методы encode и decode)
    и определить тип, содержимое и длину соответствующих переменных.
    """
    print_info_str('# 2')

    for val in args:
        if val.isascii():
            tmp = eval(f'b"{val}"')
            print(tmp, type(tmp), len(tmp))
        else:
            print(f'Не получилось записать в байтовом типе "{val}"')


def func_3(*args):
    """
    3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно
    записать в байтовом типе.

    Важно: решение должно быть универсальным, т.е. не зависеть от того,
    какие конкретно слова мы исследуем.
    """
    print_info_str('# 3')

    for val in args:
        for c in val:
            if ord(c) > 127:
                print(f'"{val}" нельзя записать в байтовом виде')
                break
        else:
            print(f'"{val}" можно записать в байтовом виде')


def func_4(*args):
    """
    4. Преобразовать слова «разработка», «администрирование», «protocol», «standard»
    из строкового представления в байтовое и выполнить обратное преобразование
    (используя методы encode и decode).
    """
    print_info_str('# 4')

    for val in args:
        print(f'{val}:')
        tmp_byte = val.encode('utf-8')
        print(f'str -> byte: {tmp_byte!r}')
        print(f'byte -> str: {tmp_byte.decode("utf-8")!r}\n')


def func_5(*args):
    """
    5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты
    из байтовового в строковый тип на кириллице.
    """
    print_info_str('# 5')

    ping_param = '-n' if platform.system().lower() == 'windows' else '-c'

    for arg in args:
        subp_args = ['ping', ping_param, '2', arg]
        subp_result = subprocess.Popen(subp_args, stdout=subprocess.PIPE)
        for line in subp_result.stdout:
            chardet_result = chardet.detect(line)
            line = line.decode(chardet_result['encoding']).encode('utf-8')
            print(line.decode('utf-8'), end='')


def func_6(*args):
    """
    6. Создать текстовый файл test_file.txt, заполнить его тремя строками:
    «сетевое программирование», «сокет», «декоратор».
    Далее забыть о том, что мы сами только что создали этот файл и исходить из того,
    что перед нами файл в неизвестной кодировке.

    Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того, в какой кодировке он был создан.
    """
    print_info_str('# 6')

    file = Path('test_file.txt')

    with file.open(mode='w', encoding='utf-8') as f:
        f.writelines(f'{v}\n' for v in args)

    with file.open(mode='rb') as f:
        chardet_result = chardet.detect(f.read())

    with file.open(mode='r', encoding=chardet_result['encoding']) as f:
        print(f'Данные в "{file}":')
        for line in f:
            print(line, end='')


if __name__ == '__main__':
    func_1()
    func_2('class', 'function', 'method', 'код')
    func_3('attribute', 'класс', 'функция', 'type')
    func_4('разработка', 'администрирование', 'protocol', 'standard')
    func_5('yandex.ru', 'youtube.com')
    func_6('сетевое программирование', 'сокет', 'декоратор')
