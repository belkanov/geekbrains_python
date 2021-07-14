"""
Создать структуру файлов и папок, как написано в задании 2 (при помощи скрипта или «руками» в проводнике).
Написать скрипт, который собирает все шаблоны в одну папку templates, например:
|--my_project
   ...
   |--templates
   |   |--mainapp
   |   |  |--base.html
   |   |  |--index.html
   |   |--authapp
   |      |--base.html
   |      |--index.html


Примечание: исходные файлы необходимо оставить;
обратите внимание, что html-файлы расположены в родительских папках (они играют роль пространств имён);
предусмотреть возможные исключительные ситуации;
это реальная задача, которая решена, например, во фреймворке django.
"""

import os
from shutil import copy2

tmplt_dir = os.path.join('my_project', 'templates')
try:
    os.mkdir(tmplt_dir)
except FileExistsError as e:
    pass

for r, d, f in os.walk('my_project'):
    if 'templates' in r and tmplt_dir not in r:  # второе условие - чтобы не копирвать папку шаблонов саму в себя
        if 'templates' in os.path.basename(r):  # тут мы попали на что-то в духе my_project\authapp\templates
            for dir_name in d:
                os.makedirs(os.path.join(tmplt_dir, dir_name), exist_ok=True)  # makedirs из-за exist_ok, чтобы не писать try
        else:  # а тут мы уже где-то глубже. например my_project\authapp\templates\authapp
            for file_name in f:
                if file_name.endswith('.html'):
                    src_dir = r.split('templates')[1].lstrip(os.path.sep)
                    # мне это задание видится больше как бэкап шаблонов, поэтому считаю copy2 уместным
                    # так у нас в бэкапе будет актуальный файл с корректными датами
                    copy2(os.path.join(r, file_name), os.path.join(tmplt_dir, src_dir))
