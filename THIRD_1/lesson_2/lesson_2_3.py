"""
3. Задание на закрепление знаний по модулю yaml.

Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата.

Для этого:
Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список,
второму — целое число,
третьему — вложенный словарь,
где значение каждого ключа — это целое число с юникод-символом,
отсутствующим в кодировке ASCII (например, €);

Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml.
При этом обеспечить стилизацию файла с помощью параметра default_flow_style,
а также установить возможность работы с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
"""
from pathlib import Path

import yaml

DATA_FOR_WRITE = {
    'first': [10, 20, 30],
    'second': 40,
    'third': {
        (1, 11): '1 €',
        (2, 22): '2 €',
        (3, 33): '3 €',
    }
}

OUTPUT_FILE = Path('lesson_2_3.yaml')


def save_data(data):
    # считаю, что добавлять данные не надо, поэтому перезатрём
    with OUTPUT_FILE.open('w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)


def check_data(data):
    with OUTPUT_FILE.open('r', encoding='utf-8') as f:
        # о рисках лоадера знаю, файл свой - поэтому так
        data_in_file = yaml.load(f, Loader=yaml.FullLoader)

    if data_in_file == data:
        print('Данные совпадают')
    else:
        print('Данные НЕ совпадают')


if __name__ == '__main__':
    save_data(DATA_FOR_WRITE)
    check_data(DATA_FOR_WRITE)
