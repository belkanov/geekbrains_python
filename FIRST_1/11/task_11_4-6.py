'''
4.  Начать работу над проектом «Склад оргтехники».
    Создать класс, описывающий склад.
    А также класс «Оргтехника», который будет базовым для классов-наследников.
    Эти классы — конкретные типы оргтехники (принтер, сканер, ксерокс).
    В базовом классе определить параметры, общие для приведённых типов.
    В классах-наследниках реализовать параметры, уникальные для каждого типа оргтехники.

5.  Продолжить работу над предыдущим заданием.
    Разработать методы, которые отвечают за приём оргтехники на склад и передачу в определённое подразделение компании.
    Для хранения данных о наименовании и количестве единиц оргтехники, а также других данных, можно использовать любую подходящую структуру (например, словарь).

6.  Продолжить работу над предыдущим заданием.
    Реализовать механизм валидации вводимых пользователем данных.
    Например, для указания количества принтеров, отправленных на склад, нельзя использовать строковый тип данных.
    Подсказка: постарайтесь реализовать в проекте «Склад оргтехники» максимум возможностей, изученных на уроках по ООП.
'''
from datetime import datetime, timedelta
from uuid import uuid4
from abc import ABC, abstractmethod
from random import choices
from collections import defaultdict
import re


class OfficeEquipment(ABC):
    _equipment_type = ''
    _sn_gen = None
    RE_SN_PATTERN = re.compile(r'\d+')

    def __init__(self, name, sn=None):
        self.name = name
        self.__uuid = str(uuid4())  # нам от уида кроме значения больше ничего и не надо
        self.__serial_number = sn if sn else next(self._sn_gen)
        self.__place_history = []

    @staticmethod
    def _sn_generator(i=0):
        while True:
            i += 1
            yield i

    @classmethod
    def validate_sn(cls, sn):
        if re.sub(cls.RE_SN_PATTERN, '', sn):
            raise ValueError(f'Серийный номер должен быть положительным целым числом (1, 2, ...) S/N: {sn}')

    @classmethod
    def get_eq_type(cls):
        return cls._equipment_type

    @abstractmethod
    def do_work(self):
        pass

    def add_place_history(self, place, date=None):
        date = date if date else datetime.now()
        self.__place_history.append({'place': place, 'date': date})

    @property
    def uuid(self):
        return self.__uuid

    @property
    def sn(self):
        return str(self.__serial_number)

    @property
    def all_place_history(self):
        return self.__place_history

    # это больше для разового вывода
    @property
    def info(self):
        return f'TYPE: {self.get_eq_type()}' \
               f'\nNAME: {self.name}' \
               f'\nS/N: {self.sn}' \
               f'\nUUID: {self.uuid}' \
               f'\nPLACE INFO (last 5): {self.all_place_history[-5:]}'  # можно еще форматированный вывод даты сделать, но я чет не стал..

    # это для отображения в циклах
    def __str__(self):
        return self.info.replace('\n', '; ')

    # это для отображения в списках
    def __repr__(self):
        return str(self)


class Printer(OfficeEquipment):
    _equipment_type = 'Printer'
    _sn_gen = OfficeEquipment._sn_generator()

    def do_work(self):
        print(f'Printer "{self.name}" - printing')


class Scanner(OfficeEquipment):
    _equipment_type = 'Scanner'
    _sn_gen = OfficeEquipment._sn_generator()

    def do_work(self):
        print(f'Scanner "{self.name}" - scanning')


class Copier(OfficeEquipment):
    _equipment_type = 'Copier'
    _sn_gen = OfficeEquipment._sn_generator()

    def do_work(self):
        print(f'Copier "{self.name}" - copying')


class Warehouse:
    def __init__(self, name):
        self.__name = name
        self.__equip_list = []

    @property
    def name(self):
        return self.__name

    def add_equipment(self, *equipment_objs, date=None):
        for x in equipment_objs:
            x.add_place_history(f'{self.name}', date)
            self.__equip_list.append(x)

    def move_equipment_obj(self, equipment_idx, destination_place, date=None):
        destination_place.add_equipment(self.__equip_list[equipment_idx])
        self.__equip_list.pop(equipment_idx)

    def move_equipment_by_uuid(self, uuid, destination_place):
        # чисто теоретически здесь и ниже (движ по SN) мы можем столкнутся с ситуацией, когда эл-ов будет более одного (особенно в случае с SN)
        # но дополнять код на всякие такие проверки не хочу, уровень проекта не тот =)
        # поэтому договоримся, что в рамках данного ДЗ у нас не может быть дублей и в итоге хватит 1го найденного значения
        srch_rslt = next((i for i, x in enumerate(self.__equip_list) if x.uuid == uuid), None)
        if srch_rslt is None:
            print(f'Не найден объект с uuid = {uuid}')
            return 0
        self.move_equipment_obj(srch_rslt, destination_place)

    def move_equipment_by_sn(self, equip_type, sn, destination_place):
        # валидацию в рамках п.6 добавил только тут ввиду простоты SN
        try:
            OfficeEquipment.validate_sn(sn)
        except ValueError as e:
            print(e)
        else:
            srch_rslt = next((i for i, x in enumerate(self.__equip_list) if x.get_eq_type() == equip_type and x.sn == sn), None)
            if srch_rslt is None:
                print(f'Не найден {equip_type} с S/N = {sn}')
                return 0
            self.move_equipment_obj(srch_rslt, destination_place)

    def get_equipments_iter(self):
        for x in self.__equip_list:
            yield x

    def print_equipments(self):
        print(f'{self.name}:')
        for x in self.__equip_list:
            print(x)

    def get_equipments_count(self):
        counters = defaultdict(int)
        for x in self.__equip_list:
            counters[x.get_eq_type()] += 1
        return dict(counters)

    def print_equipments_count(self):
        print(f'{self.name}:')
        print(self.get_equipments_count())


# ручной ввод не стал делать - писать меню и проверять долго.
warehouse_main = Warehouse('Main warehouse')
warehouse_1 = Warehouse('Division 1')
warehouse_2 = Warehouse('Division 2')

char_list = [chr(x) for x in range(ord('a'), ord('z') + 1)]
printers = [Printer(f'printer_{"".join(choices(char_list, k=3))}') for _ in range(5)]
scanners = [Scanner(f'scanner_{"".join(choices(char_list, k=3))}') for _ in range(5)]

start_date = datetime.now() - timedelta(days=7)
warehouse_main.add_equipment(*printers, date=start_date)
warehouse_main.move_equipment_by_uuid(uuid=printers[2].uuid, destination_place=warehouse_1)
warehouse_1.move_equipment_by_uuid(uuid=printers[2].uuid, destination_place=warehouse_2)
warehouse_main.move_equipment_by_sn(Printer.get_eq_type(), 'Серийник:123', warehouse_1)
warehouse_main.move_equipment_by_sn(Printer.get_eq_type(), '-123', warehouse_1)
warehouse_main.move_equipment_by_sn(Printer.get_eq_type(), printers[3].sn, warehouse_1)
print('---')

warehouse_1.print_equipments()
print('---')
warehouse_2.print_equipments()
print('---')
warehouse_main.print_equipments()
print('---')

for x in warehouse_2.get_equipments_iter():
    x.do_work()
print('---')

warehouse_main.add_equipment(*scanners)
warehouse_main.print_equipments_count()
