'''
Создать собственный класс-исключение, обрабатывающий ситуацию деления на ноль.
Проверить его работу на данных, вводимых пользователем.
При вводе нуля в качестве делителя программа должна корректно обработать эту ситуацию и не завершиться с ошибкой.
'''


class MyZeroDivisionError(Exception):
    def __init__(self, txt=None):
        self.txt = txt if txt else 'Деление на ноль'


class Test:
    def __init__(self, n):
        self.n = int(n)

    def __truediv__(self, other):
        other_n = other.n if isinstance(other, self.__class__) else int(other)
        if other_n == 0:
            raise MyZeroDivisionError
        return self.n / other_n

    def __floordiv__(self, other):
        other_n = other.n if isinstance(other, self.__class__) else int(other)
        if other_n == 0:
            raise MyZeroDivisionError
        return self.n // other_n


def input_loop():
    a = int(input('Введите A:'))
    if a == 1:
        return 1
    a_obj = Test(a)
    b = int(input('Введите B:'))
    b_obj = Test(b)
    try:
        print(a_obj / b)
        print(a_obj // b)
        print(a_obj / b_obj)
        print(a_obj // b_obj)
    except MyZeroDivisionError as e:
        print('Поймал...')
        print(e.txt)
    else:
        return 0


while True:
    if input_loop():
        print('Пока =)')
        break
