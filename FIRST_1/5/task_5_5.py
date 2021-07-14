"""
Представлен список чисел. Определить элементы списка, не имеющие повторений. Сформировать из этих элементов список с сохранением порядка их следования в исходном списке, например:
src = [2, 2, 2, 7, 23, 1, 44, 44, 3, 2, 10, 7, 4, 11]
result = [23, 1, 3, 10, 4, 11]

"""

src = [2, 2, 2, 7, 23, 1, 44, 44, 3, 2, 10, 7, 4, 11]

unique_num = set()
unique_num_tmp = set()
for el in src:
    if el not in unique_num_tmp:
        unique_num.add(el)
    else:
        unique_num.discard(el)
    unique_num_tmp.add(el)

print([x for x in src if x in unique_num])
