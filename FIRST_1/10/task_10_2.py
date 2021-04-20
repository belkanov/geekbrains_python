'''
Реализовать проект расчёта суммарного расхода ткани на производство одежды.
Основная сущность (класс) этого проекта — одежда, которая может иметь определённое название.
К типам одежды в этом проекте относятся пальто и костюм.
У этих типов одежды существуют параметры: размер (для пальто) и рост (для костюма).
Это могут быть обычные числа: V и H соответственно.

Для определения расхода ткани по каждому типу одежды использовать формулы: для пальто (V/6.5 + 0.5), для костюма (2*H + 0.3).
Проверить работу этих методов на реальных данных.

Выполнить общий подсчёт расхода ткани.
Проверить на практике полученные на этом уроке знания.
Реализовать абстрактные классы для основных классов проекта и проверить работу декоратора @property.
'''

from abc import ABC, abstractmethod
import random


class Cloth(ABC):
    title = 'Одежда'

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def tissue_consumption(self):
        pass


class Coat(Cloth):
    title = 'Пальто'

    def __init__(self, size, name=None):
        super().__init__(name)
        self.size = size

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, new_size):
        if new_size < 10:
            self.__size = 10
        elif new_size > 100:
            self.__size = 100
        else:
            self.__size = new_size

    def tissue_consumption(self):
        return self.size / 6.5 + 0.5


class Suit(Cloth):
    title = 'Костюм'

    def __init__(self, height, name=None):
        super().__init__(name)
        self.height = height

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, new_height):
        if new_height < 50:
            self.__height = 50
        elif new_height > 200:
            self.__height = 200
        else:
            self.__height = new_height

    def tissue_consumption(self):
        return 2 * self.height + 0.3


coats = [Coat(random.randint(10, 100)) for _ in range(10)]
suits = [Suit(random.randint(50, 200)) for _ in range(10)]

print('Итого ткани: {:.2f}'.format(sum(map(Coat.tissue_consumption, coats)) + sum(map(Suit.tissue_consumption, suits))))
