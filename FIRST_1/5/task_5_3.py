"""
Необходимо реализовать генератор, возвращающий кортежи вида (<tutor>, <klass>), например:
('Иван', '9А')
('Анастасия', '7В')
...

Количество генерируемых кортежей не должно быть больше длины списка tutors. Если в списке klasses меньше элементов, чем в списке tutors, необходимо вывести последние кортежи в виде: (<tutor>, None), например:
('Станислав', None)

Доказать, что вы создали именно генератор. Проверить его работу вплоть до истощения. Подумать, в каких ситуациях генератор даст эффект.

"""
import itertools

tutors = [
    'Иван', 'Анастасия', 'Петр', 'Сергей',
    'Дмитрий', 'Борис', 'Елена', 'Евгений',
    'Станислав'
]
klasses = [
    '9А', '7В', '9Б', '9В',
    '8Б', '10А', '10Б', '9А'
]


def gen():
    for e in itertools.zip_longest(tutors, klasses, fillvalue=None):
        yield e


data_gen = gen()
for i in data_gen:
    print(i)

for i in data_gen:
    print('тут наши полномочия - все..')