"""
2. Задание на закрепление знаний по модулю json.

Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными.

Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров —
товар (item), количество (quantity), цена (price), покупатель (buyer), дата (date).

Функция должна предусматривать запись данных в виде словаря в файл orders.json.
При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json()
с передачей в нее значений каждого параметра.
"""

import json
from pathlib import Path

ORDERS_FILE = Path('./data/orders.json')


def write_order_to_json(item, quantity, price, buyer, date):
    with ORDERS_FILE.open('r', encoding='utf-8') as f:
        orderds_in_file = json.loads(f.read())

    orderds_in_file['orders'].append({
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    })

    with ORDERS_FILE.open('w', encoding='utf-8') as f:
        f.write(json.dumps(orderds_in_file, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    write_order_to_json('item_1', 'quantity_1', 'price_1 €', 'buyer_1', 'date_1')
    write_order_to_json('item_2', 'quantity_2', 'price_2 €', 'buyer_2', 'date_2')
    write_order_to_json('item_3', 'quantity_3', 'price_3 €', 'buyer_3', 'date_3')
