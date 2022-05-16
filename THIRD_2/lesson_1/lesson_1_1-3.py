"""
1. Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
   Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или ip-адресом.
   В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего сообщения
   («Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью функции ip_address().

2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
   Меняться должен только последний октет каждого адреса.
   По результатам проверки должно выводиться соответствующее сообщение.

3. Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
   Но в данном случае результат должен быть итоговым по всем ip-адресам, представленным в табличном
   формате (использовать модуль tabulate). Таблица должна состоять из двух колонок и выглядеть примерно так:

Reachable   Unreachable
10.0.0.1    10.0.0.3
10.0.0.2    10.0.0.4
"""

import subprocess
from ipaddress import (
    ip_address,
    ip_network,
)
from tabulate import tabulate

"""
Учитывая, что я не разбирал вариант строки для *NIX - я не рассчитываю,
что код будут выполнять на этих системах.

Поэтому без всяких chardet, строго cp866.
Другие кодировки отметаю, т.к. считаю, 
что будут запускать на русскоязычных системах - на глобальный рынок выходить пока не планирую =)
"""


def host_ping(host_list, print_rslt=False):
    reachable_ip = []
    unreachable_ip = []
    for host_str in host_list:
        try:
            host = ip_address(host_str)
        except ValueError:
            host = host_str
        ping_str = f'ping -n 1 -w 500 {host}'
        ping_process = subprocess.Popen(ping_str.split(),
                                        shell=True,
                                        stdout=subprocess.PIPE)
        ping_stdout_str = ping_process.stdout.read().decode('cp866')
        # при вариантах:
        #  - Destination host unreachable
        #  - Request timed out
        # строчки "Average = XXXms" (среднее время доступности) не возникает
        #
        # код ответа у меня всегда == 0, так что толку от него нет
        # поэтому без wait()
        if 'Average =' in ping_stdout_str:
            reachable_ip.append(host)
            if print_rslt: print(f'{host} «Узел доступен»')
        else:
            unreachable_ip.append(host)
            if print_rslt: print(f'{host} «Узел недоступен»')

    return reachable_ip, unreachable_ip


def host_range_ping(network_ip, print_rslt=False):
    network = ip_network(network_ip)
    return host_ping(network.hosts(), print_rslt)


def host_range_ping_tab(network_ip):
    reachable_ips, unreachable_ips = host_range_ping(network_ip)
    data = {
        'Reachable': reachable_ips,
        'Unreachable': unreachable_ips
        }
    print(tabulate(data, headers='keys'))


print('----- host_ping')
host_ping(['192.168.0.1', '127.0.0.1', '8.8.8.8', '10.0.0.1', 'ya.ru', 'google.com'], print_rslt=True)
print('----- host_range_ping')
host_range_ping('192.168.0.0/30', print_rslt=True)
print('----- host_range_ping_tab')
host_range_ping_tab('192.168.0.0/30')
