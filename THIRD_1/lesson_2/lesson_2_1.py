"""
1. Задание на закрепление знаний по модулю CSV.
Написать скрипт, осуществляющий выборку определенных данных из файлов info_1.txt,
info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными,
их открытие и считывание данных. В этой функции из считанных данных необходимо с
помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список.
Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list.
В этой же функции создать главный список для хранения данных отчета — например,
main_data — и поместить в него названия столбцов отчета в виде списка:
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;
Проверить работу программы через вызов функции write_to_csv().
"""
import csv
from pathlib import Path
import chardet
import re

DATA_DIR = Path('./data')


def get_data(*file_names):
    def search_data(idx, search_string):
        re_pattern = fr'({search_string}:)\s+(.*)'
        search_result = re.search(re_pattern, line)
        if search_result:
            searched_data[idx].append(search_result.groups()[1])

    strings_to_search = ('Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы')
    searched_data = [[] for _ in range(len(strings_to_search))]

    for file_name in file_names:
        file = DATA_DIR / file_name
        with file.open('rb') as f:
            chardet_result = chardet.detect(f.read())

        with file.open('r', encoding=chardet_result['encoding']) as f:
            for line in f:
                # написал отдельную проверку на наличие искомой строки в данной строчке файла,
                # т.к. строк может быть много, а регулярка тяжелой
                # в ДАННОМ примере это конечно избыточно..
                if any(check_str in line for check_str in strings_to_search):
                    for i, search_str in enumerate(strings_to_search):
                        search_data(i, search_str)

    main_data = [strings_to_search, ]
    for row in zip(*searched_data):
        main_data.append(row)

    return main_data


def write_to_csv(file_name):
    data_to_write = get_data('info_1.txt', 'info_2.txt', 'info_3.txt')
    with Path(file_name).open('w', encoding='utf-8', newline='') as f:
        f_writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        f_writer.writerows(data_to_write)


if __name__ == '__main__':
    write_to_csv('lesson_2_1.csv')
