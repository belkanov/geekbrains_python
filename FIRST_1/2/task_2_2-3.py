"""
Дан список:
['в', '5', 'часов', '17', 'минут', 'температура', 'воздуха', 'была', '+5', 'градусов']

Необходимо его обработать — обособить каждое целое число (вещественные не трогаем) кавычками
(добавить кавычку до и кавычку после элемента списка, являющегося числом) и дополнить нулём до двух целочисленных разрядов:
['в', '"', '05', '"', 'часов', '"', '17', '"', 'минут', 'температура', 'воздуха', 'была', '"', '+05', '"', 'градусов']

Сформировать из обработанного списка строку:
в "05" часов "17" минут температура воздуха была "+05" градусов

Подумать, какое условие записать, чтобы выявить числа среди элементов списка? Как модифицировать это условие для чисел со знаком?

Примечание: если обособление чисел кавычками не будет получаться - можете вернуться к его реализации позже. Главное: дополнить числа до двух разрядов нулем!
"""

data = ['в', '5', 'часов', '17', 'минут', 'температура', 'воздуха', 'была', '+5', 'градусов']
# тут сразу 3я часть - без новых списков
first_id = id(data)

idx = 0
while idx < len(data):
    if data[idx].lstrip('+-').isdigit():
        # шаманство, т.к. формат -02d не добавляет 0 отрицательным числам, что в принципе логично
        number_sign = data[idx][:1]
        if number_sign not in ('+', '-'):
            number_sign = ''
            number = data[idx]
        else:
            number = data[idx][1:]
        # конец шаманства
        data[idx] = f'{number_sign}{int(number):02d}'
        data.insert(idx, '"')
        data.insert(idx + 2, '"')
        idx += 2
    else:
        idx += 1

second_id = id(data)

print(data)  # вывод обработнного списка
print(f'\nПосле обработки это тот же объект? {first_id == second_id}')

msg = ' '.join(data)
# я бы конечно сделал через регулярки, но мы их вроде как еще не касались.. и импорта тоже не касались
#
# можно это все еще в цикле выше сделать(в списке сразу необходимые отступы делать),
# но по условиям задачи надо список обработать определенным орбразом
#
# конечно вместо джоина выше можно в цикле объединять как надо, но там будет 16 новых строк (новая строка на каждый элемент списка)
# а тут 6 - по одному на каждую кавычку (если не считать срезы для джоинов)
# ну и джоины бодрее
is_first_bracket = True
idx_start_find = 0
while True:
    current_bracket_idx = msg.find('"', idx_start_find)
    if current_bracket_idx == -1:
        break
    if is_first_bracket:
        msg = ''.join((msg[:current_bracket_idx + 1], msg[current_bracket_idx + 2:]))
        is_first_bracket = False
    else:
        msg = ''.join((msg[:current_bracket_idx - 1], msg[current_bracket_idx:]))
        is_first_bracket = True
    idx_start_find = current_bracket_idx + 1
print(f'\n{msg}')
