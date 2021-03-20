'''
Реализовать класс Matrix (матрица).
Обеспечить перегрузку конструктора класса (метод __init__()), который должен принимать данные (список списков) для формирования матрицы.
Подсказка: матрица — система некоторых математических величин, расположенных в виде прямоугольной схемы.
Примеры матриц: 3 на 2, 3 на 3, 2 на 4.

31 22
37 43
51 86

3 5 32
2 4 6
-1 64 -8

3 5 8 3
8 3 7 1

Следующий шаг — реализовать перегрузку метода __str__() для вывода матрицы в привычном виде.

Далее реализовать перегрузку метода __add__() для  сложения двух объектов класса Matrix (двух матриц). Результатом сложения должна быть новая матрица.
Подсказка: сложение элементов матриц выполнять поэлементно. Первый элемент первой строки первой матрицы складываем с первым элементом первой строки второй матрицы и пр.
'''
from collections import defaultdict


class Matrix:
    def __init__(self, elements):
        if len(elements) < 2:
            raise ValueError('Для формирования матрицы необходимо минимум 2 списка.')
        self.__elements = []
        self.__max_elem_len = defaultdict(int)
        row_len = 0
        for row in elements:
            if row_len and len(row) != row_len:
                raise ValueError('Необходимо равное количество элементов в строках матрицы.')
            self.__elements.append(row)
            row_len = len(row)
            for i, elem in enumerate(row):
                self.__max_elem_len[str(i)] = max(self.__max_elem_len[str(i)], len(str(elem)))

    def __str__(self):
        return '\n'.join([' '.join(map(lambda x: f'{x[1]:>{self.__max_elem_len[str(x[0])]}}', enumerate(i))) for i in self.__elements])

    def __add__(self, other):
        return Matrix([[sum(j) for j in zip(*i)] for i in zip(self.__elements, other.__elements)])


matrix_a = Matrix([[31, 2222], [37, 43], [51, 86]])
print(matrix_a, end='\n\n')
matrix_b = Matrix([[3, 5, 32], [2, 4, 6], [-123, 64, -8]])
print(matrix_b, end='\n\n')
print(matrix_a + matrix_b)
