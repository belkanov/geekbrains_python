"""
5.  **(вместо 4) Решить задачу 4 и реализовать интерфейс командной строки, чтобы можно было задать имя обоих исходных файлов и имя выходного файла.
    Проверить работу скрипта.
"""
from sys import exit, argv


def task_5(*args):
    if len(args) != 4:
        print('Необходимо указать 3 параметра: файл пользователей, файл хобби, выходной файл')
        return 1
    with open(args[1], encoding='utf8') as fu, open(args[2], encoding='utf8') as fh, open(args[3], 'w', encoding='utf8') as fd:
        for user_line in fu:
            hobby_line = fh.readline().strip()  # strip для контроля за \n
            fd.write(f'{user_line.strip()}: {hobby_line if hobby_line else None}\n')
        if fh.readline():
            return 1
    return 0


if __name__ == '__main__':
    exit(task_5(*argv))
