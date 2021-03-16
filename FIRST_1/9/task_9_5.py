'''
Реализовать класс Stationery (канцелярская принадлежность):
определить в нём атрибут title (название) и метод draw (отрисовка). Метод выводит сообщение «Запуск отрисовки»;
создать три дочерних класса Pen (ручка), Pencil (карандаш), Handle (маркер);
в каждом классе реализовать переопределение метода draw. Для каждого класса метод должен выводить уникальное сообщение;
создать экземпляры классов и проверить, что выведет описанный метод для каждого экземпляра.

'''


class Stationery:
    title = 'канцелярская принадлежность'

    def draw(self):
        print('Запуск отрисовки')


class Pen(Stationery):

    def __init__(self):
        self.title = 'Ручка'

    def draw(self):
        super().draw()
        print(f'{self.title} рисует')


class Pencil(Stationery):

    def __init__(self):
        self.title = 'Карандаш'

    def draw(self):
        super().draw()
        print(f'{self.title} рисует')


class Handle(Stationery):

    def __init__(self):
        self.title = 'Маркер'

    def draw(self):
        super().draw()
        print(f'{self.title} рисует')


s = Stationery()
s.draw()
print(s.title)

pen = Pen()
pen.draw()

pencil = Pencil()
pencil.draw()

h = Handle()
h.draw()
