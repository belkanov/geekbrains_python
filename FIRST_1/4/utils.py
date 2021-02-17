from datetime import datetime
# для финансов Decimal считаю необходимым, ввиду накоплений ошибок при расчетах из-за внутреннего представления float
from decimal import Decimal

from requests import get


def get_url_content(url):
    response = get(url)
    if response.status_code == 200:
        return response.content.decode(encoding=response.encoding)


def currency_rates(cntnt, *currency_names):
    """Return [{'srv_date':datetime, 'rate':float}, ...]
    """

    rslt = []
    first_bracket_idx = cntnt.find('Date="') + 6
    # можем опираться на стабильные 10 символов в дате.
    # т.е. я не ожидаю 3 марта получить как 3.3.2021
    # сужу по текущему формату февраля (02)
    srv_date = datetime.strptime(cntnt[first_bracket_idx:first_bracket_idx + 10], '%d.%m.%Y')
    for currency_name in currency_names:
        rate = None
        if currency_name:
            currency_idx = cntnt.find(f'<CharCode>{currency_name.upper()}')
            if currency_idx != -1:
                currency_rate_idx_start = cntnt.find('<Value>', currency_idx) + 7
                currency_rate_idx_end = cntnt.find('</Value>', currency_idx)
                rate = Decimal(cntnt[currency_rate_idx_start:currency_rate_idx_end].replace(',', '.'))
        # словарь сделал для красивой распаковки в строке.
        # иначе оставил бы простой кортеж
        rslt.append({'srv_date': srv_date, 'rate': rate})
    return rslt


# сделал отдельное форматирование на случай если нам вдруг захочется поменять формат вывода (я его менял раз 5 =))
def currency_rate_print_format_str(currency_name, currency_rate_dict):
    print('{srv_date:%d.%m.%Y} {0} = {rate}'.format(currency_name.upper() if currency_name else None, **currency_rate_dict))


def print_currencies(*currency_names):
    """ Return currency rates like
    18.02.2021 eur = 89.0809
    18.02.2021 GBP = 102.4401
    """
    # это добавлено для вызова из других мест (считаем, что там не в курсе откуда брать инфу)
    cntnt = get_url_content('http://www.cbr.ru/scripts/XML_daily.asp')
    # хитрый вариант =)
    # [*map(currency_rate_print_format_str, currency_names, currency_rates(cntnt, *currency_names)]
    for i in zip(currency_names, currency_rates(cntnt, *currency_names)):
        currency_rate_print_format_str(*i)
