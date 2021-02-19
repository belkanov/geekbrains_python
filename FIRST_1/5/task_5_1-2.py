"""
1.  Написать генератор нечётных чисел от 1 до n (включительно), используя ключевое слово yield

2.  *(вместо 1) Решить задачу генерации нечётных чисел от 1 до n (включительно), не используя ключевое слово yield.
"""


def odd_nums(n):
    for i in range(1, n + 1, 2):
        yield i


for x in odd_nums(15):
    print(f'for - {x}')

gen_a = odd_nums(15)
gen_b = odd_nums(15)

print(f'next(gen_a) = {next(gen_a)}')
print(f'next(gen_a) = {next(gen_a)}')
print(f'next(gen_a) = {next(gen_a)}')
print(f'next(gen_b) = {next(gen_b)}')


# task 2
def odd_nums_not_yield(n):
    return [i for i in range(1, n + 1, 2)]


print(f'task_2 = {odd_nums_not_yield(15)}')
