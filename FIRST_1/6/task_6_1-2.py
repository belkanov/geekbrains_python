"""
1.  Не используя библиотеки для парсинга, распарсить (получить определённые данные) файл логов web-сервера nginx_logs.txt
    (https://github.com/elastic/examples/raw/master/Common%20Data%20Formats/nginx_logs/nginx_logs) — получить 
    список кортежей вида: (<remote_addr>, <request_type>, <requested_resource>). Например:
    [
        ...
        ('141.138.90.60', 'GET', '/downloads/product_2'),
        ('141.138.90.60', 'GET', '/downloads/product_2'),
        ('173.255.199.22', 'GET', '/downloads/product_2'),
        ...
    ]
    
    Примечание: код должен работать даже с файлами, размер которых превышает объем ОЗУ компьютера.
2.  *(вместо 1) Найти IP адрес спамера и количество отправленных им запросов по данным файла логов из предыдущего задания.
    Примечания: спамер — это клиент, отправивший больше всех запросов; код должен работать даже с файлами, размер которых превышает объем ОЗУ компьютера.
"""
from requests import get


# качать файл не просили, но я решил добавить
def save_log(url, file_name):
    """ сохраняет контент url в file_name. Пишет байты. Читает по 10мб

    """
    response = get(url, stream=True)
    if response.status_code == 200:
        with open(file_name, 'bw') as f:
            # для текста это рекомендуемый (разрабами request) способ. Есть еще Response.raw - это прям когда байты 1в1
            # но вообще, насколько я понял, для потоковой скачки (если точнее сохранения на диск) лучше пользовать модуль IO
            for chunk in response.iter_content(chunk_size=10 * 1024 * 1024):  # думаю 10мб найдется у всех =) всякие ардуино не в счет
                f.write(chunk)


def parse_log(file_name, req_counters):
    """возвращает список кортежей вида: (<remote_addr>, <request_type>, <requested_resource>). Например:
        [
            ...

            ('141.138.90.60', 'GET', '/downloads/product_2'),

            ('141.138.90.60', 'GET', '/downloads/product_2'),

            ('173.255.199.22', 'GET', '/downloads/product_2'),

            ...
        ]

    и словарь с подсчетом вызовов от каждого IP:
        {
            ...

            '1.2.3.4': 9000

            ...
        }
    """
    parsed_data = []
    with open(file_name) as f:
        for line in f:
            # 80.70.214.71 - - [17/May/2015:09:05:20 +0000] "HEAD /downloads/product_1 HTTP/1.1" 200 0 "-" "Wget/1.13.4 (linux-gnu)"
            first_quote = line.find('"') + 1
            parsed_data.append((line[:line.find(' ')], *line[first_quote:line.find('"', first_quote)].split()[:2]))  # ip, req_type, req_resource
            req_counters.setdefault(parsed_data[-1][0], 0)
            req_counters[parsed_data[-1][0]] += 1
    return parsed_data


if __name__ == '__main__':
    log_name = 'nginx_logs.txt'
    request_counters = dict()
    # по хорошему надо конечно проверять наличие файла и если его нет - скачать, можно еще смотреть на дату модификации и сохранять каждые 15 минут например
    # да и еще кучу вариантов придумать..
    # но файловую систему мы еще не проходили - поэтому так.
    # можно еще как параметр запуска в терминале вынести, но чет не стал..
    # False тут стоит намеренно, чтобы постоянно не скачивать файл.
    if False:
        save_log('https://github.com/elastic/examples/raw/master/Common%20Data%20Formats/nginx_logs/nginx_logs', log_name)

    # принт отключил намеренно. кортеж получаем, вывод необязателен
    # print(parse_log(log_name, request_counters))
    parse_log(log_name, request_counters)

    # такое сработает, если максимальное значение только одно
    max_req_key = max(request_counters, key=request_counters.get)
    print(f'{max_req_key}: {request_counters[max_req_key]}')

    # более универсальный вариант
    max_req_value = max(request_counters.values())
    print([f'{k}: {v}' for k, v in request_counters.items() if v == max_req_value])
