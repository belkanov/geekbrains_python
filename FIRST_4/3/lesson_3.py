from random import randint


def inpt(text, inpt_str, row_cnt=1):
    """
    на случай если появится желание проверить и вводить даные руками
    сделайте is_input_enable = True

    в остальных случаях будем работать с заготовленной строкой inpt_str

    просто для удобства)
    """

    is_input_enable = False
    
    rslt = []
    inpt_str = inpt_str.split('\n')
    for i in range(row_cnt):
        if is_input_enable:
            rslt.append(input(text).split())
        else:
            rslt.append(inpt_str[i].split())
    if row_cnt == 1:
        rslt = rslt[0]
    return rslt


def part_1(s):
    print('# 1. В диапазоне натуральных чисел от 2 до 99 определить, сколько из них кратны каждому из чисел в диапазоне от 2 до 9.')
    
    rslt = dict.fromkeys(range(2, 10), 0)
    for v in range(2, 100):
        for k in rslt:
            if v % k == 0:
                rslt[k] += 1
    
    [*map(lambda k : print(f'числу {k} кратно {rslt[k]} чисел'), rslt)]
    print()
    
    print()


def part_2(s):
    print('# 2. Во втором массиве сохранить индексы четных элементов первого массива. ')
    # Например, если дан массив со значениями 8, 3, 15, 6, 4, 2, то во второй массив надо заполнить 
    # значениями 1, 4, 5, 6 (или 0, 3, 4, 5 - если индексация начинается с нуля), т.к. именно в этих позициях первого массива стоят четные числа.')
    
    arr = [*map(int, inpt('Введите массив значений: ', s))]
    # rslt = [i for i in range(len(arr)) if arr[i] % 2 == 0] # краткий вариант
    rslt = []
    for i in range(len(arr)):
        if arr[i] % 2 == 0:
            rslt.append(i)
    
    print(f'Для массива {arr} индексы четных элементов - {rslt}')

    print()


def part_3(s):
    print('# 3. В массиве случайных целых чисел поменять местами минимальный и максимальный элементы.')
    
    arr = [randint(0, 100) for _ in range(10)]
    min_idx, max_idx = 0, 0
    for i in range(len(arr)):
        if arr[i] < arr[min_idx]:
            min_idx = i
        if arr[i] > arr[max_idx]:
            max_idx = i
            
    print(f'Для массива   {arr} максимальный и минимальный элементы (в скобках индекс): {arr[max_idx]}({max_idx}), {arr[min_idx]}({min_idx})')    
    arr[min_idx], arr[max_idx] = arr[max_idx], arr[min_idx]
    print(f'Новый массив: {arr}')
    
    print()


def part_4(s):
    print('# 4. Определить, какое число в массиве встречается чаще всего.')
    
    arr = [*map(int, inpt('Введите массив значений: ', s))]
    d_cntr = dict.fromkeys(set(arr), 0)
    for v in arr:
        d_cntr[v] += 1
    # max_cnt_k = max(d_cntr, key=d_cntr.get) # краткий вариант
    max_cnt_k, max_cnt_v = None, 0
    for k, v in d_cntr.items():
        if v > max_cnt_v:
            max_cnt_k, max_cnt_v = k, v
    
    print(f'Для массива {arr} счетчики чисел: {d_cntr}. Чаще всего встречается число {max_cnt_k}')
    
    print()


def part_5(s):
    print('# 5. В массиве найти максимальный отрицательный элемент. Вывести на экран его значение и позицию (индекс) в массиве.')
    
    arr = [*map(int, inpt('Введите массив значений: ', s))]
    # думаю, что из part_3() становится ясно, что мне понятен алгоритм нахождения мин/макс и их индексов. 
    # поэтому я решил попробовать записать решение одной строчкой, пускай и с использованием встроенной функции =)
    max_idx = max((i for i in range(len(arr)) if arr[i] < 0), key=lambda idx: arr[idx])
    
    print(f'Для массива {arr} максимальный отрицательный элемент (в скобках индекс): {arr[max_idx]} ({max_idx})')
    
    print()


def part_6(s):
    print('# 6. В одномерном массиве найти сумму элементов, находящихся между минимальным и максимальным элементами. ')
    # Сами минимальный и максимальный элементы в сумму не включать.

    arr = [randint(0, 100) for _ in range(10)]
    min_max_idx = [0, 0]
    for i in range(len(arr)):
        if arr[i] < arr[min_max_idx[0]]:
            min_max_idx[0] = i
        if arr[i] > arr[min_max_idx[1]]:
            min_max_idx[1] = i
    print(f'Для массива {arr} максимальный и минимальный элементы (в скобках индекс): {arr[min_max_idx[1]]}({min_max_idx[1]}), {arr[min_max_idx[0]]}({min_max_idx[0]})')
    # если у нас минимальное в конце - соритруем, чтобы воспользоваться срезом. ну или городим IF, чтобы разобраться какой индекс меньше
    # т.к. в min_max_idx всего два элемента, то я решил, что мы не особо потеряем в скорости из-за сортировки
    min_max_idx.sort()
    # rslt = sum(arr[min_max_idx[0]+1:min_max_idx[1]]) # краткий вариант
    rslt = 0
    for v in arr[min_max_idx[0]+1:min_max_idx[1]]:
        rslt += v
    print(f'Сумма чисел между этими элементами: {rslt}')
    print()


def part_7(s):
    print('# 7. В одномерном массиве целых чисел определить два наименьших элемента.')
    # Они могут быть как равны между собой (оба являться минимальными), так и различаться. 
    
    arr = [randint(0, 100) for _ in range(10)]
    # разные примеры...
    # arr = [90, 12, 79, 51, 37, 31, 99, 24, 98, 21]  # [0], min1, ...., min2, ... # сломается, если будут неверные начальные индексы min1_idx, min2_idx
    # arr = [11, 77, 18, 13, 34, 96, 78, 89, 65, 93]  # min1, ..., min2, ... # сломается, если не проверять индекс текущего и первого минимального (i != min1_idx)
    # arr = [3, 9, 4, 1]  # min2, ..., min1  # надо передать второму минимальному 0-ой индекс и только под конец
    # arr = [3, 9, 4, 2, 1]  # минимальные появятся с самом конце, в обратном порядке (..., min2, min1)
    # arr = [3, 9, 1, 4, 1]  # min1 = min2
    # arr = [6, 21, 69, 7, 67, 41, 37, 76, 35, 6]  # min1 = min2, с краю каждый
    # arr = [39, 14, 70, 100, 97, 62, 40, 28, 28, 80]  # 2 шт min2, при этом индекс не меняется с 7 на 8; это не ошибка конечно, но бывает важно найти первое совпадение
    min1_idx, min2_idx = 0, 1
    for i in range(len(arr)):
        if arr[i] < arr[min1_idx]:
            min2_idx = min1_idx
            min1_idx = i
        if arr[min1_idx]<=arr[i]<arr[min2_idx] and i != min1_idx:
            min2_idx = i
    print(f'Для массива {arr} наименьшие элементы (в скобках индекс): {arr[min1_idx]}({min1_idx}), {arr[min2_idx]}({min2_idx})')
    print(f'Отсортированный: {sorted(arr)}')  # для удобства проверки рандомных значений решил добавить

    print()


def part_8(s):
    print('# 8. Матрица 5x4 заполняется вводом с клавиатуры кроме последних элементов строк.')
    # Программа должна вычислять сумму введенных элементов каждой строки и записывать ее в последнюю ячейку строки. 
    # В конце следует вывести полученную матрицу.')
    
    mtrx = [[*map(int, row)] for row in inpt('Введите матрицу 5x3 (последний столбец будет рассчитан): ', s, 5)]
    # [row.append(sum(row)) for row in mtrx]  # краткий вариант 
    for row in mtrx:
        s = 0
        for v in row:
            s += v
        row.append(s) 
    
    [*map(print, mtrx)]

    print()


def part_9(s):
    print('# 9. Найти максимальный элемент среди минимальных элементов столбцов матрицы.')

    mtrx = [[*map(int, row)] for row in inpt('Введите матрицу 4xN: ', s, 4)]
    # max_elem = max(map(min, zip(*mtrx))) # краткий вариант 
    mins = mtrx[0].copy()
    for i in range(1, len(mtrx)):
        for j in range(len(mins)):
            if mtrx[i][j] < mins[j]:
                mins[j] = mtrx[i][j]
    max_elem = mins[0]
    for i in range(1, len(mins)):
        if mins[i] > max_elem:
            max_elem = mins[i]
    
    print(f'Для матрицы:')
    [*map(print, mtrx)]
    print(f'\n{mins} - минимальные значения; среди них максимальный элемент: {max_elem}')
    
    print()


def main():
    part_1('')
    part_2('8 3 15 6 4 2')
    part_3('')
    part_4('3 1 2 1 2 1')
    part_5('-2 0 5 -1 4')
    part_6('')
    part_7('')
    part_8('1 1 1\n2 2 2\n3 3 3\n4 4 4\n5 5 5')
    part_9('9 9 3 9\n8 4 3 5\n7 4 1 7\n6 5 2 6')
    
if __name__ == '__main__':
    main()