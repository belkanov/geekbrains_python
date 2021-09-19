"""
Проанализировать скорость и сложность одного любого алгоритма, разработанных в рамках практического задания первых трех уроков.
"""
from random import randint
import cProfile
from timeit import Timer


# ДЗ 3, п.4 Определить, какое число в массиве встречается чаще всего.

def f1():
    # если я правильно понял - сложность у обеих реализаций О(n)
    # один раз проходимся по всем элементам словаря и находим максимальный по значению
    return max(d_cntr, key=d_cntr.get)


def f2():
    max_cnt_k, max_cnt_v = None, 0
    for k, v in d_cntr.items():
        if v > max_cnt_v:
            max_cnt_k, max_cnt_v = k, v
    return max_cnt_k


def main():
    f1()
    f2()


def main2():
    for _ in range(20_000):
        f1()
        f2()


if __name__ == '__main__':
    arr = [randint(0, 5000) for _ in range(100_000)]
    d_cntr = dict.fromkeys(set(arr), 0)
    for v in arr:
        d_cntr[v] += 1
    # cProfile.run('main()')  # в плане сравнений реализаций оказался бесполезным (у обеих функций время по нулям)

    # несмотря на одинаковую сложность за счет разной реализации получили разницу в 2 раза
    # f1: 4.1257295
    # f2: 8.1112554
    for v in range(1, 3):
        time = Timer("func()", f"from __main__ import f{v} as func").timeit(20_000)
        print(f"f{v}: {time}")

    # после решил еще переделать cProfile, чтобы тоже было видно
    # cumtime
    #   4.204 lesson_4_1.py:11(f1)
    #   7.858 lesson_4_1.py:17(f2)
    cProfile.run('main2()')
