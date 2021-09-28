"""
Подсчитать, сколько было выделено памяти под переменные в ранее разработанных программах в рамках первых трех уроков.
Проанализировать результат и определить программы с наиболее эффективным использованием памяти.

Примечание: Для анализа возьмите любые 1-3 ваших программы или несколько вариантов кода для одной и той же задачи.
Результаты анализа вставьте в виде комментариев к коду. Также укажите в комментариях версию Python и разрядность вашей ОС.
"""
from sys import getsizeof
from memory_profiler import profile


def add_size(d: dict, v, v_name):
    d[v_name] = max(d.get(v_name, 0), getsizeof(v))


@profile(precision=12)
def f1(mtrx):
    sizes = dict()

    mins = mtrx[0].copy()
    for i in range(1, len(mtrx)):
        add_size(sizes, i, 'i')
        for j in range(len(mins)):
            add_size(sizes, j, 'j')
            if mtrx[i][j] < mins[j]:
                mins[j] = mtrx[i][j]
    add_size(sizes, mins, 'mins')
    add_size(sizes, mtrx, 'mtrx')

    max_elem = mins[0]
    for i in range(1, len(mins)):
        add_size(sizes, i, 'i')
        if mins[i] > max_elem:
            max_elem = mins[i]
    add_size(sizes, max_elem, 'max_elem')

    print(f'{mins} - минимальные значения; среди них максимальный элемент: {max_elem}')
    print(f'{sizes = }, total size = {sum(sizes.values())}')

    print()


@profile(precision=12)
def f2(mtrx):
    sizes = dict()

    max_elem = max(map(min, zip(*mtrx)))  # краткий вариант
    add_size(sizes, max_elem, 'max_elem')

    print(f'максимальный элемент: {max_elem}')
    print(f'{sizes = }, total size = {sum(sizes.values())}')

    print()


@profile(precision=12)
def f3(mtrx):
    sizes = dict()

    # max_elem = max(map(min, zip(*mtrx))) # разобью эту штуку на части
    a = [*zip(*mtrx)]
    add_size(sizes, a, 'a')
    b = [*map(min, a)]
    add_size(sizes, b, 'b')
    max_elem = max(b)
    add_size(sizes, max_elem, 'max_elem')

    print(f'максимальный элемент: {max_elem}')
    print(f'{sizes = }, total size = {sum(sizes.values())}')

    print()


@profile(precision=12)
def main():
    print('ДЗ 3. #9. Найти максимальный элемент среди минимальных элементов столбцов матрицы.')
    mtrx = [[*map(int, row)] for row in map(str.split, '9 9 3 9\n8 4 3 5\n7 4 1 7\n6 5 2 6'.split('\n'))]
    print(f'Для матрицы:')
    [*map(print, mtrx)]
    print('\n--- f1')
    f1(mtrx)
    print('--- f2')
    f2(mtrx)
    print('--- f3')
    f3(mtrx)


if __name__ == '__main__':
    main()


"""
Делал по всякому: 
 - запускал только одну функцию/все разом
 - из терминала/PyCharm

итог в принципе одинаковый:  
    что-то отличное от нуля было на первой строке добавления в словарь
    22  40.269531250000 MiB   0.003906250000 MiB           3           add_size(sizes, i, 'i')

когда запускал все функции, такое было только раз на f1.
если запускать по отдельности (другие вызовы в комменты) - то этот же размер в вызываемой функции

Единственное отличие было в общем увеличении памяти с 40 до 55 МиБ когда запускал из пишарма.
Подозреваю, что связано со всякими плюшками, которые делает ИДЕ для удобства работы/отладки.

---

Вывод при запуске всех 3х из терминала: 

PS E:\Sources\Python\PyCharmProject\geekbrains_python\FIRST_4\6> python .\lesson_6.py
ДЗ 3. #9. Найти максимальный элемент среди минимальных элементов столбцов матрицы.
Для матрицы:
[9, 9, 3, 9]
[8, 4, 3, 5]
[7, 4, 1, 7]
[6, 5, 2, 6]

--- f1
[6, 4, 1, 5] - минимальные значения; среди них максимальный элемент: 6
sizes = {'i': 28, 'j': 28, 'mins': 88, 'mtrx': 88, 'max_elem': 28}, total size = 260

Filename: .\lesson_6.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    16  40.265625000000 MiB  40.265625000000 MiB           1   @profile(precision=12)
    17                                         def f1(mtrx):
    18  40.265625000000 MiB   0.000000000000 MiB           1       sizes = dict()
    19
    20  40.265625000000 MiB   0.000000000000 MiB           1       mins = mtrx[0].copy()
    21  40.269531250000 MiB   0.000000000000 MiB           4       for i in range(1, len(mtrx)):
    22  40.269531250000 MiB   0.003906250000 MiB           3           add_size(sizes, i, 'i')
    23  40.269531250000 MiB   0.000000000000 MiB          15           for j in range(len(mins)):
    24  40.269531250000 MiB   0.000000000000 MiB          12               add_size(sizes, j, 'j')
    25  40.269531250000 MiB   0.000000000000 MiB          12               if mtrx[i][j] < mins[j]:
    26  40.269531250000 MiB   0.000000000000 MiB           6                   mins[j] = mtrx[i][j]
    27  40.269531250000 MiB   0.000000000000 MiB           1       add_size(sizes, mins, 'mins')
    28  40.269531250000 MiB   0.000000000000 MiB           1       add_size(sizes, mtrx, 'mtrx')
    29
    30  40.269531250000 MiB   0.000000000000 MiB           1       max_elem = mins[0]
    31  40.269531250000 MiB   0.000000000000 MiB           4       for i in range(1, len(mins)):
    32  40.269531250000 MiB   0.000000000000 MiB           3           add_size(sizes, i, 'i')
    33  40.269531250000 MiB   0.000000000000 MiB           3           if mins[i] > max_elem:
    34                                                     max_elem = mins[i]
    35  40.269531250000 MiB   0.000000000000 MiB           1       add_size(sizes, max_elem, 'max_elem')
    36
    37  40.269531250000 MiB   0.000000000000 MiB           1       print(f'{mins} - минимальные значения; среди них максимальный элемент: {max_elem}')
    38  40.269531250000 MiB   0.000000000000 MiB           1       print(f'{sizes = }, total size = {sum(sizes.values())}')
    39
    40  40.269531250000 MiB   0.000000000000 MiB           1       print()


--- f2
максимальный элемент: 6
sizes = {'max_elem': 28}, total size = 28

Filename: .\lesson_6.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    43  40.269531250000 MiB  40.269531250000 MiB           1   @profile(precision=12)
    44                                         def f2(mtrx):
    45  40.269531250000 MiB   0.000000000000 MiB           1       sizes = dict()
    46
    47  40.269531250000 MiB   0.000000000000 MiB           1       max_elem = max(map(min, zip(*mtrx)))  # краткий вариант
    48  40.269531250000 MiB   0.000000000000 MiB           1       add_size(sizes, max_elem, 'max_elem')
    49
    50  40.269531250000 MiB   0.000000000000 MiB           1       print(f'максимальный элемент: {max_elem}')
    51  40.269531250000 MiB   0.000000000000 MiB           1       print(f'{sizes = }, total size = {sum(sizes.values())}')
    52
    53  40.269531250000 MiB   0.000000000000 MiB           1       print()


--- f3
максимальный элемент: 6
sizes = {'a': 112, 'b': 112, 'max_elem': 28}, total size = 252

Filename: .\lesson_6.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    56  40.269531250000 MiB  40.269531250000 MiB           1   @profile(precision=12)
    57                                         def f3(mtrx):
    58  40.269531250000 MiB   0.000000000000 MiB           1       sizes = dict()
    59
    60                                             # max_elem = max(map(min, zip(*mtrx))) # разобью эту штуку на части
    61  40.269531250000 MiB   0.000000000000 MiB           1       a = [*zip(*mtrx)]
    62  40.269531250000 MiB   0.000000000000 MiB           1       add_size(sizes, a, 'a')
    63  40.269531250000 MiB   0.000000000000 MiB           1       b = [*map(min, a)]
    64  40.269531250000 MiB   0.000000000000 MiB           1       add_size(sizes, b, 'b')
    65  40.269531250000 MiB   0.000000000000 MiB           1       max_elem = max(b)
    66  40.269531250000 MiB   0.000000000000 MiB           1       add_size(sizes, max_elem, 'max_elem')
    67
    68  40.269531250000 MiB   0.000000000000 MiB           1       print(f'максимальный элемент: {max_elem}')
    69  40.269531250000 MiB   0.000000000000 MiB           1       print(f'{sizes = }, total size = {sum(sizes.values())}')
    70
    71  40.269531250000 MiB   0.000000000000 MiB           1       print()


Filename: .\lesson_6.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
    74  40.253906250000 MiB  40.253906250000 MiB           1   @profile(precision=12)
    75                                         def main():
    76  40.261718750000 MiB   0.007812500000 MiB           1       print('ДЗ 3. #9. Найти максимальный элемент среди минимальных элементов столбцов матрицы.')
    77  40.261718750000 MiB   0.000000000000 MiB           7       mtrx = [[*map(int, row)] for row in map(str.split, '9 9 3 9\n8 4 3 5\n7 4 1 7\n6 5 2 6'.split('\n'))]
    78  40.261718750000 MiB   0.000000000000 MiB           1       print(f'Для матрицы:')
    79  40.261718750000 MiB   0.000000000000 MiB           1       [*map(print, mtrx)]
    80  40.261718750000 MiB   0.000000000000 MiB           1       print('\n--- f1')
    81  40.269531250000 MiB   0.007812500000 MiB           1       f1(mtrx)
    82  40.269531250000 MiB   0.000000000000 MiB           1       print('--- f2')
    83  40.269531250000 MiB   0.000000000000 MiB           1       f2(mtrx)
    84  40.269531250000 MiB   0.000000000000 MiB           1       print('--- f3')
    85  40.269531250000 MiB   0.000000000000 MiB           1       f3(mtrx)


PS E:\Sources\Python\PyCharmProject\geekbrains_python\FIRST_4\6>
"""