'''
Осуществить программу работы с органическими клетками, состоящими из ячеек.
Необходимо создать класс «Клетка».
В его конструкторе инициализировать параметр, соответствующий количеству ячеек клетки (целое число).
В классе должны быть реализованы методы перегрузки арифметических операторов: сложение (__add__()), вычитание (__sub__()), умножение (__mul__()), деление (__floordiv____truediv__()).
Эти методы должны применяться только к клеткам и выполнять увеличение, уменьшение, умножение и округление до целого числа деления клеток соответственно.

Сложение. Объединение двух клеток. При этом число ячеек общей клетки должно равняться сумме ячеек исходных двух клеток.

Вычитание. Участвуют две клетки. Операцию необходимо выполнять, только если разность количества ячеек двух клеток больше нуля, иначе выводить соответствующее сообщение.

Умножение. Создаётся общая клетка из двух. Число ячеек общей клетки — произведение количества ячеек этих двух клеток.

Деление. Создаётся общая клетка из двух. Число ячеек общей клетки определяется как целочисленное деление количества ячеек этих двух клеток.

В классе необходимо реализовать метод make_order(), принимающий экземпляр класса и количество ячеек в ряду.
Этот метод позволяет организовать ячейки по рядам.
Метод должен возвращать строку вида *****\n*****\n*****..., где количество ячеек между \n равно переданному аргументу.
Если ячеек на формирование ряда не хватает, то в последний ряд записываются все оставшиеся.
Например, количество ячеек клетки равняется 12, а количество ячеек в ряду — 5. В этом случае метод make_order() вернёт строку: *****\n*****\n**.
Или количество ячеек клетки — 15, а количество ячеек в ряду равняется 5. Тогда метод make_order() вернёт строку: *****\n*****\n*****.
'''
import re


class Cell:
    is_abs_operations = False

    def __check_instance(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f'Операция допустима только для объектов одного класса ({self.__class__}).')

    def __init__(self, cell_num):
        if not isinstance(cell_num, int) or cell_num < 1:
            raise ValueError('Количество ячеек должно быть натуральным числом (1, 2, 3, ...)')
        self.cell_num = cell_num

    def __add__(self, other):  # +
        self.__check_instance(other)
        return Cell(self.cell_num + other.cell_num)

    def __sub__(self, other):  # -
        self.__check_instance(other)
        if not Cell.is_abs_operations and self.cell_num < other.cell_num:
            raise ValueError('Разность ячеек будет отрицательной. Поменяйте местами операнды.')
        else:
            return Cell(abs(self.cell_num - other.cell_num))

    def __mul__(self, other):  # *
        self.__check_instance(other)
        return Cell(self.cell_num * other.cell_num)

    def __floordiv__(self, other):  # //
        self.__check_instance(other)
        return Cell(self.cell_num // other.cell_num)

    def __truediv__(self, other):  # /
        self.__check_instance(other)
        return Cell(int(self.cell_num / other.cell_num))  # int(7/4) == 1

    def make_order(self, row_len):
        cell_str = '*' * self.cell_num
        splitter = '*' * row_len
        end_pattern = r'\*' * row_len

        # можно и без регулярки. захотел одной строкой
        return print(re.sub(rf'\n{end_pattern}$', '', '\n'.join(map(lambda x: x if x else splitter, cell_str.split(splitter)))))


print('----- 1 -----')
Cell(12).make_order(5)
print('----- 2 -----')
(Cell(5) + Cell(6)).make_order(3)
# (Cell(5) + 5).make_order(2)  # raise из __check_instance
print('----- 3 -----')
Cell.is_abs_operations = True
(Cell(5) - Cell(6)).make_order(2)
# (Cell(5) - Cell(5)).make_order(20)  # raise из __init__
print('----- 4 -----')
(Cell(5) * Cell(5)).make_order(5)
print('----- 5 -----')
(Cell(100) // Cell(5)).make_order(20)
print('----- 6 -----')
Cell.is_abs_operations = False
(Cell(5) - Cell(6)).make_order(2)
