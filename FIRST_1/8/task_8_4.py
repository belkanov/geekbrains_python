"""
Написать декоратор с аргументом-функцией (callback), позволяющий валидировать входные значения функции и выбрасывать исключение ValueError, если что-то не так, например:
def val_checker...
    ...


@val_checker(lambda x: x > 0)
def calc_cube(x):
   return x ** 3


    a = calc_cube(5)
    125

    a = calc_cube(-5)
    Traceback (most recent call last):
      ...
        raise ValueError(msg)
    ValueError: wrong val -5


Примечание: сможете ли вы замаскировать работу декоратора?

"""
from functools import wraps
import inspect


def true_checker(lst):
    for e in lst:
        if not e:
            return False
    return True


def val_checker(f_check):
    f_name = val_checker.__name__

    def _val_checker(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if true_checker(map(f_check, args)):
                return func(*args, **kwargs)
            raise ValueError(f'{args} не все элементы подходят условию {inspect.getsourcelines(f_check)[0][0].strip().replace(f"@{f_name}", "")}')  # хотя тут и func подходит, они одинаковые.. хз почему, не ковырял

        return wrapper

    return _val_checker


@val_checker(lambda x: x > 0)
def f_1(*n):
    print(*n)


x = f_1(2, -5, 4)
