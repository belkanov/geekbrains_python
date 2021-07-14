'''
Реализовать класс «Дата», функция-конструктор которого должна принимать дату в виде строки формата «день-месяц-год».
В рамках класса реализовать два метода.
Первый — с декоратором @classmethod. Он должен извлекать число, месяц, год и преобразовывать их тип к типу «Число».
Второй — с декоратором @staticmethod, должен проводить валидацию числа, месяца и года (например, месяц — от 1 до 12). Проверить работу полученной структуры на реальных данных.
'''
import datetime


class Date:
    @classmethod
    def get_int_date(cls, date_str):
        split_str = date_str.split('-')
        if len(split_str) != 3:
            raise ValueError(f'"{date_str}" не соответствует формату «день-месяц-год»')
        try:
            day, month, year = (int(i) for i in split_str)
        except:  # при любой ошибке мы не получим желаемого, поэтому без уточнений.
            raise ValueError('Значения даты не являются целыми числами.')
        else:
            return day, month, year


    @staticmethod
    def date_validate(date_str):
        day, month, year = Date.get_int_date(date_str)
        # можно конечно сразу отдать datetime, но скорее всего ждут не этого, поэтому добавлю немного ручной проверки
        if not 1 <= day <= 31:
            raise ValueError(f'Значение дня "{day}" не является допустимым (1, 2, ..., 31)')
        if not 1 <= month <= 12:
            raise ValueError(f'Значение месяца "{month}" не является допустимым (1, 2, ..., 12)')
        if not 1 <= year:
            raise ValueError(f'Значение года "{year}" не является допустимым (1, 2, ...)')
        try:
            # проверку валидности самой даты отдам datetime, потому что не хочу писать свой громадный велосипед
            dt = datetime.datetime(day=day, month=month, year=year)
        except ValueError as e:
            raise ValueError(f'"{date_str}" - недопустимые значения даты.')
        else:
            # раз уж мы проверили дату на корректность значений, то почему бы это не использовать..
            return dt

    def __init__(self, date_str):
        dt = Date.date_validate(date_str)
        self.day, self.month, self.year = dt.day, dt.month, dt.year


# print(Date('28.02.2021').day)
# print(Date('д-м-г').day)
print(Date('28-2-2021').month)
print(Date('29-02-2021').month)
