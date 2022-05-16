from subprocess import (
    Popen,
    CREATE_NEW_CONSOLE,
)
from time import sleep
from sys import executable

"""
Без изысков. 
Считаю, что если конфиг отличается от предложенного - 
то проще запускать через консоль.

Лаунчер для простоты тестов. 
"""

PROCESSES = []

print('Выберите действие:\n'
      '[1]* - запустить 1 сервер и 2 клиента\n'
      '[2]  - выключить все и выйти\n')
while True:
    mode = input('> ')
    if mode == '1':
        PROCESSES.append(Popen(['start', executable, 'server.py'], shell=True, creationflags=CREATE_NEW_CONSOLE))
        sleep(0.5)
        PROCESSES.append(Popen(['start', executable, *'client.py -u Test_1'.split()], shell=True, creationflags=CREATE_NEW_CONSOLE))
        PROCESSES.append(Popen(['start', executable, *'client.py -u Test_2'.split()], shell=True, creationflags=CREATE_NEW_CONSOLE))
    elif mode == '2':
        while PROCESSES:
            VICTIM = PROCESSES.pop()
            VICTIM.kill()
            VICTIM.terminate()
        break
    else:
        print(PROCESSES)
        print('Действие не распознано. Введите 1 или 2.')
