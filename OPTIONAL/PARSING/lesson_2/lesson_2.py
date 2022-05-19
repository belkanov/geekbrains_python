"""
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность)
с сайтов HH(обязательно) и/или Superjob(по желанию).
Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).

Получившийся список должен содержать в себе минимум:
Наименование вакансии.
Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия.

По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas.

Сохраните в json либо csv.
"""
import re
from time import sleep

import requests
from bs4 import BeautifulSoup as bs
from collections import namedtuple
import logging
import json

RE_SALARY = re.compile(r'(?:\d+\s*){1,}')
RE_CURRENCY = re.compile(r'\D+')
MAIN_URL = 'https://hh.ru'
VACANCY_URL = f'{MAIN_URL}/search/vacancy'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'
}
vacancy_name = 'python'
PARAMS = {
    'text': vacancy_name
}

Salary = namedtuple('Salary', (
    'min',
    'max',
    'currency'
))

logging.basicConfig(format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('job_scraper')
logger.setLevel(logging.INFO)

# если включить - можно увидеть редиректы
# requests_log = logging.getLogger("urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True


def get_response(url, headers, params=None):
    timeouts = (5, 5)  # conn, read
    response = requests.get(url,
                            headers=headers,
                            params=params,
                            timeout=timeouts)
    if response.ok:
        # на случай редиректа hh.ru -> rostov.hh.ru
        splitted_response_url = response.url.split('/')
        new_main_url = f'{splitted_response_url[0]}//{splitted_response_url[2]}'
        return response, new_main_url


def get_int(re_match):
    return int(re_match.group().replace(' ', ''))


def get_salary(tag):
    if tag is None:
        return Salary(None, None, None)

    text = clear_tag_text(tag)
    # получалось неплохо через всякие сплиты/слайсы/джоины,
    # но потом пришли 'бел. руб.' и все сломалось =)
    # поэтому регулярки
    if 'от' in text:
        re_salary = RE_SALARY.search(text)
        salary = get_int(re_salary)
        re_currency = RE_CURRENCY.search(text, re_salary.end())
        return Salary(salary, None, re_currency.group())
    elif 'до' in text:
        re_salary = RE_SALARY.search(text)
        salary = get_int(re_salary)
        re_currency = RE_CURRENCY.search(text, re_salary.end())
        return Salary(None, salary, re_currency.group())
    else:
        re_min_salary = RE_SALARY.search(text)
        min_salary = get_int(re_min_salary)
        re_max_salary = RE_SALARY.search(text, re_min_salary.end())
        max_salary = get_int(re_max_salary)
        re_currency = RE_CURRENCY.search(text, re_max_salary.end())
        return Salary(min_salary, max_salary, re_currency.group())


def clear_tag_text(tag):
    text = tag.getText()
    text = text.replace('\n', '')
    # внезапно вылезло много пробелов
    splitted = [word for word in text.split() if word]
    text = ' '.join(splitted)
    return text


def parse_vacancy_link(tag):
    link = tag.get('href')
    return f'{MAIN_URL}{link}'


def save_to_file(data, file_name):
    with open(file_name, 'w', encoding='utf8') as f:
        f.write(data)


def parse_response(response, main_url):
    vacancies_info = []

    soup = bs(response.text, 'html.parser')
    anchor = soup.find('div', {'class': 'vacancy-serp-content'})

    vacancy_results = anchor.find('div', {'data-qa': 'vacancy-serp__results'})
    vacancies = vacancy_results.find_all('div', {'class': 'vacancy-serp-item'})
    logger.info('Нашел %d вакансий. Обрабатываю...', len(vacancies))
    for vacancy in vacancies:
        title_tag = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
        salary_tag = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})

        vacancy_info = {
            'name': clear_tag_text(title_tag),
            'salary': get_salary(salary_tag),
            'link': title_tag.get('href'),
            'site': main_url,
        }
        vacancies_info.append(vacancy_info)

    return vacancies_info, anchor


def main():
    all_vacancies = []

    page_cnt = 1
    url = VACANCY_URL
    headers = HEADERS
    params = PARAMS
    while True:
        logger.info('Parse page #%d', page_cnt)
        response, main_url = get_response(url, headers=headers, params=params)
        if not response:
            logger.error('NO response from %s', url)
            raise SystemExit(1)

        try:
            vacancies_info, anchor = parse_response(response, main_url)
        except ValueError as e:
            logger.exception(e)
            save_to_file(response.text, 'error_response.html')
            raise SystemExit(1)

        all_vacancies.extend(vacancies_info)

        logger.info('Ищу следующую страницу...')
        next_link = anchor.find('a', {'data-qa': 'pager-next'})
        if next_link:
            logger.info('Нашел.')
            url = f'{main_url}{next_link.get("href")}'
            params = None
            page_cnt += 1
            sleep(1)  # не будем спамить запросами
        else:
            logger.info('Видимо это последняя =) Всего обработано %d страниц',
                        page_cnt)
            break

    with open('vacancies.json', 'w', encoding='utf-8') as f:
        json.dump(all_vacancies, f, ensure_ascii=False)


if __name__ == '__main__':
    logger.info('--- START')
    main()
    logger.info('--- END')
