"""
1.  Написать функцию email_parse(<email_address>), которая при помощи регулярного выражения извлекает
    имя пользователя и почтовый домен из email адреса и возвращает их в виде словаря.
    Если адрес не валиден, выбросить исключение ValueError. Пример:

     email_parse('someone@geekbrains.ru')
    {'username': 'someone', 'domain': 'geekbrains.ru'}

     email_parse('someone@geekbrainsru')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      ...
        raise ValueError(msg)
    ValueError: wrong email: someone@geekbrainsru


    Примечание: подумайте о возможных ошибках в адресе и постарайтесь учесть их в регулярном выражении;
    имеет ли смысл в данном случае использовать функцию re.compile()?

2.  *(вместо 1) Написать регулярное выражение для парсинга файла логов web-сервера из ДЗ 6 урока nginx_logs.txt
    (https://github.com/elastic/examples/raw/master/Common%20Data%20Formats/nginx_logs/nginx_logs)
    для получения информации вида: (<remote_addr>, <request_datetime>, <request_type>, <requested_resource>, <response_code>, <response_size>), например:

    raw = '188.138.60.101 - - [17/May/2015:08:05:49 +0000] "GET /downloads/product_2 HTTP/1.1" 304 0 "-" "Debian APT-HTTP/1.3 (0.9.7.9)"'
    parsed_raw = ('188.138.60.101', '17/May/2015:08:05:49 +0000', 'GET', '/downloads/product_2', '304', '0')


    Примечание: вы ограничились одной строкой или проверили на всех записях лога в файле? Были ли особенные строки? Можно ли для них уточнить регулярное выражение?
"""
import re

valid_email = ['123abc@mail1.com', '123_abc@mail.2com', '123-abc@mail3.3com', '1.2.3.a.b.c@4mail4.4com4', '1-2-3-a-b-c@ma5il.com', '1_2-3.abc@6m6a6i6l6.6c6o6m6', '             1_2-3.abc@mail.com']
not_valid_email = ['123abc@mailcom', '123abc.@mail.com', '.123abc@mail.com', '123a..bc@mail.com', '123abc-@mail.com', '-123abc@mail.com', '123--abc@mail.com', '123 abc@mail.com', '123abc @mail.com']

"""
основа:
буквы цифры . _ - (без пробелов, без повторений подряд, не начало, не конец)

кириллицу (и прочий юникод) считаю уместной
ввиду работающих сайтов по типу "стопкоронавирус.рф" (https://xn--80aesfpebagmfblc0a.xn--p1ai/)
"""
RE_TASK_1 = re.compile(r'(?P<username>^\w+([._-]\w+)*)@(?P<domain>\w+\.\w+)')
# т.к. это логи сервера, то нам не надо проверять валидность адресов, просто их достаем
RE_TASK_2 = re.compile(r'^([0-9a-f.:]+) - - \[(.*)\] \"(\w+) (.*?)\" (\d+) (\d+) ', flags=re.IGNORECASE)


def email_parse(email):
    # python 3.8+
    if s := RE_TASK_1.search(email.strip()):  # посчитал стрип уместным, т.к. в итоге можно возвращать очищенный email или из словаря составлять дальше в коде
        return s.groupdict()
    raise ValueError(f'{email} - not valid email')


def log_line_parse(log_str):
    if s := RE_TASK_2.search(log_str):
        return s.groups()
    raise ValueError(f'--- NOT VALID --- {log_str}')  # для выделения


def task_1():
    for elem in valid_email + not_valid_email:
        try:
            print(elem, email_parse(elem))
        except ValueError as e:
            print(e)


def task_2():
    with open('nginx_logs.txt', encoding='utf8') as f:
        for line in f:
            try:
                print(log_line_parse(line))
            except ValueError as e:
                print(e)


if __name__ == '__main__':
    task_1()
    task_2()
