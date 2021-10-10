from collections import namedtuple, deque
from itertools import zip_longest, product
from functools import reduce


def part_1():
    print('# 1. Пользователь вводит данные о количестве предприятий, их наименования и прибыль за 4 квартала (т.е. 4 отдельных числа) для каждого предприятия..')
    #    Программа должна определить среднюю прибыль (за год для всех предприятий) и вывести наименования предприятий,
    #    чья прибыль выше среднего и отдельно вывести наименования предприятий, чья прибыль ниже среднего.

    QuartalFinData = namedtuple('QuartalFinData', 'first_q second_q third_q fourth_q')
    companies = dict()
    # для проверки
    companies['a'] = QuartalFinData(first_q=1, second_q=1, third_q=1, fourth_q=1)
    companies['b'] = QuartalFinData(first_q=2, second_q=2, third_q=2, fourth_q=2)
    companies['c'] = QuartalFinData(first_q=1, second_q=2, third_q=3, fourth_q=4)
    companies['d'] = QuartalFinData(first_q=4, second_q=3, third_q=2, fourth_q=2)
    # for i in range(int(input('Введите количество компаний:'))):
    #     k, *v = input(f'Введите название и данные по кварталам для компании №{i+1}: ').split()
    #     companies[k] = QuartalFinData(first_q=int(v[0]), second_q=int(v[1]), third_q=int(v[2]), fourth_q=int(v[3]))
    avg = sum(sum(v) for v in companies.values()) / len(companies)
    top_companies = []
    low_companies = []
    for k, v in companies.items():
        if (s := sum(v)) >= avg:
            top_companies.append((k, s))
        else:
            low_companies.append((k, s))
    top_companies.sort(key=lambda x: x[1], reverse=True)
    low_companies.sort(key=lambda x: x[1], reverse=True)
    print('--- TOP ---')
    for v in top_companies:
        print(f'{v[0]}: {v[1]}')
    print(f'--- AVG: {avg} ---')
    for v in low_companies:
        print(f'{v[0]}: {v[1]}')


def part_2():
    print('\n# 2. Написать программу сложения и умножения двух шестнадцатеричных чисел. При этом каждое число представляется как массив,')
    #    элементы которого это цифры числа. Например, пользователь ввёл A2 и C4F. Сохранить их как [‘A’, ‘2’] и [‘C’, ‘4’, ‘F’] соответственно.
    #    Сумма чисел из примера: [‘C’, ‘F’, ‘1’], произведение - [‘7’, ‘C’, ‘9’, ‘F’, ‘E’].
    hex_dict = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
    # можно конечно и руками, но чет было лень..
    dec_dict = {v: k for k, v in hex_dict.items()}

    def add(a, b):
        rslt = [*zip_longest(a[::-1], b[::-1], fillvalue='0')]  # формируем списки для сложений
        r = 0  # "1 в уме" =)
        for i in range(len(rslt)):
            t = (hex_dict[rslt[i][0]] + hex_dict[rslt[i][1]]) + r  # скалдываем числа + разряд
            rslt[i] = t % 16  # записываем остаток от деления
            r = 0 if t <= 15 else t // 16  # сохарняем разряд
        if r:
            rslt.append(r)  # если вдруг остался разряд - надо его сохранить

        rslt = [dec_dict[v] for v in rslt]  # dec -> hex
        return rslt[::-1]

    def mul(a, b):
        def chunks(lst, n):
            for i in range(0, len(lst), n):
                yield deque(lst[i:i + n])

        rslt = [*product(b[::-1], a[::-1])]  # созадем пары для операции умножения
        rslt = [*chunks(rslt, len(rslt) // len(b))]  # разбиваем их по разрядности
        for j in range(len(b)):
            r = 0
            for i in range(len(rslt[j])):
                t = (hex_dict[rslt[j][i][0]] * hex_dict[rslt[j][i][1]]) + r
                rslt[j][i] = t % 16
                r = 0 if t <= 15 else t // 16
            if r:  # сохарнем разряд
                rslt[j].append(r)
            for _ in range(j):  # повышаем число на порядок
                rslt[j].appendleft(0)

        rslt = [[dec_dict[v] for v in reversed(l)] for l in rslt]  # dec -> hex
        return [*reduce(add, rslt)]  # суммируем

    # n_1 = list('A2')
    # n_1 = list('B5D')
    # n_1 = list('F')
    n_1 = list('ED45')
    #
    # n_2 = list('C4F')
    # n_2 = list('A0AB')
    # n_2 = list('F')
    n_2 = list('C41E2')
    #
    # n_1, n_2 = map(list, input('Введите 2 числа: ').upper().split())
    print(f'{n_1} + {n_2} = {add(n_1, n_2)}')
    print(f'{n_1} * {n_2} = {mul(n_1, n_2)}')


def main():
    part_1()
    part_2()


if __name__ == '__main__':
    main()
