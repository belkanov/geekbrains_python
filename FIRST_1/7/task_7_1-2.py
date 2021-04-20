"""
1.  Написать скрипт, создающий стартер (заготовку) для проекта со следующей структурой папок:
    |--my_project
       |--settings
       |--mainapp
       |--adminapp
       |--authapp

    Примечание: подумайте о ситуации, когда некоторые папки уже есть на диске (как быть?);
    как лучше хранить конфигурацию этого стартера, чтобы в будущем можно было менять имена папок под конкретный проект;
    можно ли будет при этом расширять конфигурацию и хранить данные о вложенных папках и файлах (добавлять детали)?

2.  *(вместо 1) Написать скрипт, создающий из config.yaml стартер для проекта со следующей структурой:
    |--my_project
       |--settings
       |  |--__init__.py
       |  |--dev.py
       |  |--prod.py
       |--mainapp
       |  |--__init__.py
       |  |--models.py
       |  |--views.py
       |  |--templates
       |     |--mainapp
       |        |--base.html
       |        |--index.html
       |--authapp
       |  |--__init__.py
       |  |--models.py
       |  |--views.py
       |  |--templates
       |     |--authapp
       |        |--base.html
       |        |--index.html

    Примечание: структуру файла config.yaml придумайте сами, его можно создать в любом текстовом редакторе «руками» (не программно);
    предусмотреть возможные исключительные ситуации, библиотеки использовать нельзя.
"""
import os

# расширять конфигурацию и хранить данные о вложенных папках и файлах (добавлять детали) можно заменив строки на словари:
# {'name': value_1,
#  'type': value_2,
#  'mode': value_3,
#  ...
#  }
# остальные папки тут сделаны просто для демонстрации, основная структура из задания создается.
dirs_struct = ('base_dir:',
               ('my_project:',
                       ('settings:',
                        'mainapp:',
                        'adminapp:',
                        'authapp:'
                        ),
                   'tst_1:',
                       ('tst_1_1:',
                        'tst_1_2:',
                        'tst_1_3:',
                            ('tst_1_3_1:',
                                 ('tst_1_3_1_1', ),  # это будет файл
                             'tst_1_3_2:'
                             ),
                        'tst_1_4:'
                    )
                   )
               )


# fso = file system object
def fso_name_from_tuple_gen(dir_list, root=''):
    for dir_name in dir_list:
        if isinstance(dir_name, tuple):
            yield from fso_name_from_tuple_gen(dir_name, cur_root)
        else:
            cur_root = os.path.join(root, dir_name) if root else dir_name
            yield cur_root


def fso_name_from_file_gen(file):
    with open(file, 'r') as f:
        for line in f:
            line = line.strip(os.linesep).replace('- ', '')
            if ':' in line:
                cur_sub_lvl = line.split(' ').count('') // 2
                base_dir = '' if cur_sub_lvl == 0 else os.path.join(*base_dir.split(os.path.sep)[:cur_sub_lvl])
                base_dir = os.path.join(base_dir, line.strip())
                yield base_dir
            else:
                yield os.path.join(base_dir, line.strip())


def make_fso(dir_name):
    # my_project:\mainapp:\templates:\mainapp:
    # my_project:\mainapp:\templates:\mainapp:\base.html
    try:
        if ':' in os.path.basename(dir_name):  # двоеточие = папка. позволяет создавать файлы без расширения
            os.mkdir(dir_name.replace(':', ''))
        else:
            open(dir_name.replace(':', ''), 'x').close()
    except FileExistsError as e:
        # тут можно делать и что-то другое: удалять папку и делать ее заново (очистка содержимого), стирать файл, ...
        # можно пользователя каждый раз спрашивать, можно только перед выполнением один раз спросить, ...
        # вариантов много =)
        print(f'"{e.filename}" уже существует')


def task_1(dirs):
    for fso_name in fso_name_from_tuple_gen(dirs):
        make_fso(fso_name)


def task_2(file_name):
    for fso_name in fso_name_from_file_gen(file_name):
        make_fso(fso_name)


if __name__ == '__main__':
    task_1(dirs_struct)
    task_2('config.yaml')
