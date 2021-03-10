"""
3.  Написать функцию thesaurus(), принимающую в качестве аргументов имена сотрудников и возвращающую словарь, в котором ключи — первые буквы имен, а значения — списки, содержащие имена, начинающиеся с соответствующей буквы. Например:
     thesaurus("Иван", "Мария", "Петр", "Илья")
    {
        "И": ["Иван", "Илья"],
        "М": ["Мария"], "П": ["Петр"]
    }

    Подумайте: полезен ли будет вам оператор распаковки?
    Как поступить, если потребуется сортировка по ключам?
    Можно ли использовать словарь в этом случае?

4.  *(вместо задачи 3) Написать функцию thesaurus_adv(), принимающую в качестве аргументов строки в формате «Имя Фамилия» и возвращающую словарь, в котором ключи — первые буквы фамилий, а значения — словари, реализованные по схеме предыдущего задания и содержащие записи, в которых фамилия начинается с соответствующей буквы. Например:
     thesaurus_adv("Иван Сергеев", "Инна Серова", "Петр Алексеев", "Илья Иванов", "Анна Савельева")
    {
        "А": {
            "П": ["Петр Алексеев"]
        },
        "С": {
            "И": ["Иван Сергеев", "Инна Серова"],
            "А": ["Анна Савельева"]
        }
    }

    Как поступить, если потребуется сортировка по ключам?
"""


def thesaurus(*args):
    rslt = {}
    for elem in args:
        first_alpha = elem[:1]
        if first_alpha in rslt:
            rslt[first_alpha].append(elem)
        else:
            rslt[first_alpha] = [elem]
    return rslt


def thesaurus_adv(*args):
    rslt = {}
    for elem in args:
        name, surname = elem.split()
        name_first_alpha = name[:1]
        surname_first_alpha = surname[:1]
        if surname_first_alpha in rslt:
            if name_first_alpha in rslt[surname_first_alpha]:
                rslt[surname_first_alpha][name_first_alpha].append(elem)
            else:
                rslt[surname_first_alpha][name_first_alpha] = [elem]
        else:
            rslt[surname_first_alpha] = {name_first_alpha: [elem]}
    return rslt


thsrs = thesaurus("Мария", "Петр", "Илья", "Иван")
# для начала покажем, что словарь не сортирован (хотя про них нельзя так сказать)
print(*thsrs.items())  # распаковка, чтобы не было dict_items()
# "отсортированный"
thsrs = dict(sorted(thsrs.items()))
print(*thsrs.items())

print('---')
thsrs = thesaurus_adv("Иван Сергеев", "Инна Серова", "Петр Алексеев", "Илья Иванов", "Анна Савельева")
print(*thsrs.items())
# по мне такая запись смотрится куда проще (а по дзену значит лучше), чем та, что ниже, хотя одной строкой веселее)
for k in thsrs:
    thsrs[k] = dict(sorted(thsrs[k].items()))
thsrs = dict(sorted(thsrs.items()))
# thsrs = dict(tuple(map(lambda x: (x[0], dict(sorted(x[1].items()))), sorted(thsrs.items()))))
print(*thsrs.items())
