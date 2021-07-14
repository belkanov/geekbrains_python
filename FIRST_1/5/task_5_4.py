"""
Представлен список чисел. Необходимо вывести те его элементы, значения которых больше предыдущего, например:
src = [300, 2, 12, 44, 1, 1, 4, 10, 7, 1, 78, 123, 55]
result = [12, 44, 4, 10, 78, 123]


Подсказка: использовать возможности python, изученные на уроке. Подумайте, как можно сделать оптимизацию кода по памяти, по скорости.

"""
from timeit import Timer

src = [300, 2, 12, 44, 1, 1, 4, 10, 7, 1, 78, 123, 55]
check_rslt = [12, 44, 4, 10, 78, 123]


def gen_1(s):
    i = 0
    while True:
        i += 1
        if i >= len(s):
            break
        if s[i - 1] < s[i]:
            yield s[i]


def gen_2(s):
    for i in range(1, len(s)):
        if s[i - 1] < s[i]:
            yield s[i]


def gen_3(s):
    # чаще всего самый бодрый вариант. так же топ по памяти ввиду того, что это генератор
    # с ним на равне comp_2 и ret_1. Они иногда были быстрее:
    # gen_3: 0.18943300000000007
    # comp_2: 0.17081250000000003
    # ret_1: 0.16769089999999975
    prev = None
    for i in s:
        if (prev or i) < i:
            prev = i
            yield i
        prev = i


def gen_4(s):
    for x, y in zip(s, s[1:]):
        if x < y:
            yield y


def comp_1(s):
    return [x for i, x in enumerate(s) if s[i - 1] < s[i] if i > 0]


def comp_2(s):
    return [y for x, y in zip(s, s[1:]) if x < y]


def ret_1(s):
    rslt = []
    prev = None
    for i in s:
        if (prev or i) < i:
            prev = i
            rslt.append(i)
        prev = i
    return rslt


if __name__ == '__main__':

    print(check_rslt == list(gen_1(src)) == list(gen_2(src)) == list(gen_3(src)) == list(gen_4(src)) == comp_1(src) == comp_2(src) == ret_1(src))

    timeit_count = 100_000
    for v in range(1, 5):
        time = Timer("list(func(src))", f"from __main__ import src, gen_{v} as func").timeit(timeit_count)
        print(f"gen_{v}: {time}")

    for v in range(1, 3):
        time = Timer("func(src)", f"from __main__ import src, comp_{v} as func").timeit(timeit_count)
        print(f"comp_{v}: {time}")

    for v in range(1, 2):
        time = Timer("func(src)", f"from __main__ import src, ret_{v} as func").timeit(timeit_count)
        print(f"ret_{v}: {time}")
