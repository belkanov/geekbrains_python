"""
4.  Написать скрипт, который выводит статистику для заданной папки в виде словаря,
    в котором ключи — верхняя граница размера файла (пусть будет кратна 10), а значения — общее количество файлов (в том числе и в подпапках),
    размер которых не превышает этой границы, но больше предыдущей (начинаем с 0), например:
        {
          100: 15,
          1000: 3,
          10000: 7,
          100000: 2
        }

    Тут 15 файлов размером не более 100 байт; 3 файла больше 100 и не больше 1000 байт...

    Подсказка: размер файла можно получить из атрибута .st_size объекта os.stat.

5.  *(вместо 4) Написать скрипт, который выводит статистику для заданной папки в виде словаря,
    в котором ключи те же, а значения — кортежи вида (<files_quantity>, [<files_extensions_list>]), например:
        {
          100: (15, ['txt']),
          1000: (3, ['py', 'txt']),
          10000: (7, ['html', 'css']),
          100000: (2, ['png', 'jpg'])
        }

    Сохраните результаты в файл <folder_name>_summary.json в той же папке, где запустили скрипт.
"""

import os
from collections import defaultdict
from json import dump

file_size_cnt = defaultdict(lambda: [0, set()])
file_size_cnt_dict = dict()


def get_size_for_dict(n):
    if not n:
        return 0
    cnt = 1
    while True:
        dict_size = 10 ** cnt
        if n < dict_size:
            return dict_size
        else:
            cnt += 1


for r, d, f in os.walk(os.getcwd()):
    with os.scandir(r) as sd:
        for element in sd:
            if element.is_file():
                size_key = get_size_for_dict(element.stat().st_size)
                file_size_cnt[size_key][0] += 1
                file_size_cnt[size_key][1].add(os.path.splitext(element.name)[1][1:])

for k, v in file_size_cnt.items():
    file_size_cnt_dict[k] = tuple((v[0], list(v[1])))

with open(os.path.join(os.getcwd(), 'task_5_dict.json'), 'w+') as f:
    dump(file_size_cnt_dict, f)
