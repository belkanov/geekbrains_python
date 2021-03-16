'''
Реализуйте базовый класс Car:
у класса должны быть следующие атрибуты: speed, color, name, is_police (булево).
А также методы: go, stop, turn(direction), которые должны сообщать, что машина поехала, остановилась, повернула (куда);
опишите несколько дочерних классов: TownCar, SportCar, WorkCar, PoliceCar;
добавьте в базовый класс метод show_speed, который должен показывать текущую скорость автомобиля;
для классов TownCar и WorkCar переопределите метод show_speed. При значении скорости свыше 60 (TownCar) и 40 (WorkCar) должно выводиться сообщение о превышении скорости.

Создайте экземпляры классов, передайте значения атрибутов.
Выполните доступ к атрибутам, выведите результат.
Вызовите методы и покажите результат.

'''


class Car:
    def __init__(self, speed, color, name, is_police=False):
        self.speed = speed
        self.color = color
        self.name = name
        self.is_police = is_police

    def go(self):
        print('Машина поехала')

    def stop(self):
        print('Машина остановилась')

    def turn(self, direction):
        if direction.lower() == 'l':
            print('Машина повернула налево')
        elif direction.lower() == 'r':
            print('Машина повернула направо')
        else:
            print('Недопустимое значение направления поворота')

    def show_speed(self):
        print(f'Скорость машины = {self.speed}')


class TownCar(Car):
    def __init__(self, speed, color, name):
        super().__init__(speed, color, name)

    def show_speed(self):
        super().show_speed()
        if self.speed > 60:
            print('Машина едет с превышением допустимой скорости (60)')


class SportCar(Car):
    def __init__(self, speed, color, name):
        super().__init__(speed, color, name)


class WorkCar(Car):
    def __init__(self, speed, color, name):
        super().__init__(speed, color, name)

    def show_speed(self):
        super().show_speed()
        if self.speed > 40:
            print('Машина едет с превышением допустимой скорости (40)')


class PoliceCar(Car):
    def __init__(self, speed, color, name):
        super().__init__(speed, color, name, is_police=True)


tc = TownCar(70, 'a', 'name_tc_1')
print(tc.name)
tc.go()
tc.stop()
tc.turn('O')
tc.turn('L')
tc.show_speed()

print()
pc = PoliceCar(120, 'b', 'name_pc_1')
print(pc.name)
print(pc.is_police)
