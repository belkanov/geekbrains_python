"""
Написать декоратор для логирования типов позиционных аргументов функции, например:
    def type_logger...
        ...

    @type_logger
    def calc_cube(x):
       return x ** 3

    a = calc_cube(5)
    5: <class 'int'>

Примечание: если аргументов несколько - выводить данные о каждом через запятую;
можете ли вы вывести тип значения функции?
Сможете ли решить задачу для именованных аргументов?
Сможете ли вы замаскировать работу декоратора?
Сможете ли вывести имя функции, например, в виде:
    a = calc_cube(5)
    calc_cube(5: <class 'int'>)
"""
from functools import wraps


def type_logger(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(', '.join(map(lambda x: f'{func.__name__}({x}: {str(type(x))}) -> {str(type(result))}', args)))
        # решил сделать отдельно, а то уже каша выходит
        print(', '.join(map(lambda x: f'{x}: {kwargs.get(x)} {str(type(kwargs.get(x)))}', kwargs)))
        return result

    return wrapper


@type_logger
def some_func(*args, **kwargs):
    pass


a = some_func(3, (2, 2), 'abc', some_func, param_1='a', param_2=[324, ])
