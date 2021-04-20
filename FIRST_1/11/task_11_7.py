'''
Реализовать проект «Операции с комплексными числами».
Создать класс «Комплексное число».
Реализовать перегрузку методов сложения и умножения комплексных чисел.
Проверить работу проекта.
Для этого создать экземпляры класса (комплексные числа), выполнить сложение и умножение созданных экземпляров. Проверить корректность полученного результата.
'''
import re


class ComplexNum:
    RE_NUM_PATTERN = re.compile(r'(\d+)\s*\+\s*(\d+)+i')

    def __init__(self, num_str: str):
        self.a = None
        self.b = None
        srch = re.search(self.RE_NUM_PATTERN, num_str)
        if srch:
            self.a = int(srch.groups()[0])
            self.b = int(srch.groups()[1])
        # split_str = num_str.split('+')
        # a = split_str[0]

    def __str__(self):
        if self.a and self.b:
            return f'{self.a}+{self.b}i'
        else:
            return 'None'

    def __add__(self, other):
        return ComplexNum(f'{self.a + other.a}+{self.b + other.b}i')

    def __mul__(self, other):
        return ComplexNum(f'{self.a * other.a - self.b * other.b}+{self.a * other.b + self.b * other.a}i')


x = ComplexNum('3+2i')
y = ComplexNum('3+2')
z = ComplexNum('4+5i')
print(x, y, z)

assert str(x + z) == '7+7i'
assert str(x * z) == '2+23i'
