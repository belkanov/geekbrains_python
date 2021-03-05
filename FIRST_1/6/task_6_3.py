"""
3.  Есть два файла: в одном хранятся ФИО пользователей сайта, а в другом  — данные об их хобби.
    Известно, что при хранении данных используется принцип: одна строка — один пользователь, разделитель между значениями — запятая.
    Написать код, загружающий данные из обоих файлов и формирующий из них словарь: ключи — ФИО, значения — данные о хобби.
    Сохранить словарь в файл. Проверить сохранённые данные.
    Если в файле, хранящем данные о хобби, меньше записей, чем в файле с ФИО, задаём в словаре значение None.
    Если наоборот — выходим из скрипта с кодом «1».
    При решении задачи считать, что объём данных в файлах во много раз меньше объема ОЗУ.

    Фрагмент файла с данными о пользователях (users.csv):
    Иванов,Иван,Иванович
    Петров,Петр,Петрович

    Фрагмент файла с данными о хобби  (hobby.csv):
    скалолазание,охота
    горные лыжи
"""
from itertools import zip_longest
from json import dump, load
from sys import exit


def task_3():
    with open('users.csv', encoding='utf8') as fu, open('hobby.csv', encoding='utf8') as fh, open('dict.json', 'w', encoding='utf8') as fd:
        user_lines, hobby_lines = fu.readlines(), fh.readlines()
        if len(hobby_lines) > len(user_lines):
            # вместо импорта я бы сделал raise SystemExit, но раз мы исключения еще не трогали..
            return 1
        user_hobby_dict = {' '.join(k.strip().split(',')): v.strip().split(',') if v else None for k, v in zip_longest(user_lines, hobby_lines)}
        dump(user_hobby_dict, fd, ensure_ascii=False)
    # проверяем корректность
    with open('dict.json', encoding='utf8') as fd:
        check_dict = load(fd)
        print(check_dict)
    return 0


if __name__ == '__main__':
    exit(task_3())
