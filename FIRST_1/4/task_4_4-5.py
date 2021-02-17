"""
4.  Написать свой модуль utils и перенести в него функцию currency_rates() из предыдущего задания.
    Создать скрипт, в котором импортировать этот модуль и выполнить несколько вызовов функции currency_rates().
    Убедиться, что ничего лишнего не происходит.

5.  *(вместо 4) Доработать скрипт из предыдущего задания: теперь он должен работать и из консоли. Например:

    > python task_4_5.py USD
    75.18, 2020-09-05
"""
import utils
import argparse

# utils.print_currency('usd', 'AUD', 'cad')

if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser(description='Get CURRENCY/RUB rate')
    arg_parser.add_argument('currency', nargs='*', help='Can be "USD EUR ..."')

    args = arg_parser.parse_args()

    if not args.currency:
        args.currency = ('usd', 'eur', 'cny')
    utils.print_currencies(*args.currency)
