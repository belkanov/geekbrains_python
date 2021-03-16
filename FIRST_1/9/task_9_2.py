'''
Реализовать класс Road (дорога).
определить атрибуты: length (длина), width (ширина);
значения атрибутов должны передаваться при создании экземпляра класса;
атрибуты сделать защищёнными;
определить метод расчёта массы асфальта, необходимого для покрытия всей дороги;
использовать формулу: длина*ширина*масса асфальта для покрытия одного кв. метра дороги асфальтом, толщиной в 1 см*число см толщины полотна;
проверить работу метода.

Например: 20 м*5000 м*25 кг*5 см = 12500 т.

'''


class Road:
    __mass = 25  # кг асфальта для покрытия 1 кв.м, толщиной 1 см

    def __init__(self, length, width):
        self._length = length
        self._width = width

    def get_mass(self, height=1):
        mass = self._width * self._length * height * Road.__mass
        mass_name = 'кг'
        if mass >= 1000:
            mass_name = 'т'
            mass = (mass / 1000)
        mass = mass
        return f'{mass:,} {mass_name}'


r = Road(5000, 20)
print(r.get_mass(1))
print(r.get_mass(5))
r = Road(10, 2)
print(r.get_mass(1))
print(r.get_mass(5))
