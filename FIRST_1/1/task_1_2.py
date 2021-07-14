"""
Создать список, состоящий из кубов нечётных чисел от 1 до 1000:
    a. Вычислить сумму тех чисел из этого списка, сумма цифр которых делится нацело на 7.
       Например, число «19 ^ 3 = 6859» будем включать в сумму, так как 6 + 8 + 5 + 9 = 28 – делится нацело на 7.
       Внимание: использовать только арифметические операции!

    b. К каждому элементу списка добавить 17 и заново вычислить сумму тех чисел из этого списка, сумма цифр которых делится нацело на 7.

    c. * Решить задачу под пунктом b, не создавая новый список.
"""

# c. список только один
arr = [x**3 for x in range(1001) if x % 2 != 0]

total_a = 0
total_b = 0

for value in arr:
    tmp_val = value
    # вот отсюда и до 28 я бы заменил на функцию, но мы их еще не проходили.
    numbers_sum = 0
    # while я бы заменил на for c in str(value), но раз только арифметика..
    while tmp_val > 0:
        last_number = tmp_val % 10
        numbers_sum += last_number
        tmp_val = (tmp_val - last_number) // 10  # // тут только потому, что он возвращает int
    if numbers_sum % 7 == 0:
        total_a += value

    tmp_val = value + 17
    numbers_sum = 0
    while tmp_val > 0:
        last_number = tmp_val % 10
        numbers_sum += last_number
        tmp_val = (tmp_val - last_number) // 10
    if numbers_sum % 7 == 0:
        total_b += value + 17

print(total_a)  # 17_485_588_610
print(total_b)  # 15_392_909_930
