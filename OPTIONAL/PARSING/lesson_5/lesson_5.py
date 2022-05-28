"""
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и
реализовать функцию, которая будет добавлять только новые вакансии в вашу базу.

2. Написать функцию, которая производит поиск и выводит на экран вакансии с
заработной платой больше введённой суммы (необходимо анализировать оба поля зарплаты).
Для тех, кто выполнил задание с Росконтролем - напишите запрос для поиска продуктов
с рейтингом не ниже введенного или качеством не ниже введенного
(то есть цифра вводится одна, а запрос проверяет оба поля)
"""
import logging
from hashlib import sha3_256
from pprint import pprint
from time import sleep
from typing import Optional
from lxml import html

import requests
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError
from bson.objectid import ObjectId

from constants import *

logging.basicConfig(format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('job_scraper')
logger.setLevel(logging.INFO)

# если включить - можно увидеть редиректы
# requests_log = logging.getLogger("urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True


def get_response(url, headers=HEADERS, params=None):
    timeouts = (5, 5)  # conn, read

    for i in range(5):
        response = requests.get(url,
                                headers=headers,
                                params=params,
                                timeout=timeouts)
        if response.ok:
            logger.debug('response - OK')
            break
        else:
            logger.debug('response - NOT OK (%s)', response.status_code)
            sleep_time = i + 1
            logger.warning(f'Не смог получить ответ для %s. Подождем %d сек.',
                           response.url,
                           sleep_time)
            sleep(sleep_time)
    else:
        raise SystemExit(1, f'Так и не смог получить ответ для {response.url}')

    return response


def save_to_file(data, file_name):
    with open(file_name, 'w', encoding='utf8') as f:
        f.write(data)


def is_link_ok(link):
    # Натыкался на разное, что, по идее, не подходит под стандартные новости.
    # Например
    # https://news.mail.ru/diafilm/12-po-rossii-kazan/
    # слайдшоу по достопримечательностям Казани
    #
    # https://news.mail.ru/stories/4-foto-dnya/
    # там галерея из 35 фото с изначально пустыми ДИВами,
    # Дата самой "новости" всегда 3 ноября 2021 (поэтому ее не беру),
    # актуальные даты есть только у фото, которые заполняются динамически.
    #
    # решил такое пропускать
    if link.split('/')[-2].isdecimal():
        return True
    logger.warning('ПРОПУЩЕНО: скорее всего не обычная новость: %s', link)
    return False


def parse_response(response):
    news_info_list = []
    news_links = []
    dom = html.fromstring(response.text)
    anchor = dom.xpath(XPATH_ANCHOR)[0]

    # сначала картинки (5шт)
    news_links.extend(anchor.xpath('.//a/@href'))
    # потом текст под ними (6шт)
    news_links.extend(anchor.xpath('../following-sibling::ul/li[not(contains(@class, "hidden"))]/a/@href'))

    logger.info('Нашел %d новостей. Обрабатываю...', len(news_links))
    for news_idx, news_link in enumerate(news_links):
        logger.info('Parse news #%d', news_idx+1)
        if not is_link_ok(news_link):
            continue

        news_response = get_response(news_link)
        news_dom = html.fromstring(news_response.text)
        news_anchor = news_dom.xpath('//div[@data-logger-parent="content"]')[0]

        metainfo_anchor = news_anchor.xpath('.//span[@class="note"]')
        news_info = {
            'link': str(news_link),  # приводим к явной строке <_ElementUnicodeResult>
            'pub_date': metainfo_anchor[0].xpath('./span/@datetime')[0],
            'source_name': metainfo_anchor[1].xpath('./a//text()')[0],
            'source_link': metainfo_anchor[1].xpath('./a/@href')[0],  # решил добавить
            'news_title': news_anchor.xpath('.//h1/text()')[0],
        }
        news_info_list.append(news_info)

    return news_info_list


def get_mongo_collection(collection_name: str) -> Optional[Collection]:
    client = MongoClient(host=MONGODB_HOST,
                         port=MONGODB_PORT,
                         username=MONGO_INITDB_ROOT_USERNAME,
                         password=MONGO_INITDB_ROOT_PASSWORD)
    db = client[MONGODB_DB_NAME]

    collection = getattr(db, collection_name, None)
    if collection is None:
        raise ValueError(1, f"Коллекция {collection_name} не найдена")

    return collection


def save_to_mongo(data):
    mailru_news_collection = get_mongo_collection(MONGO_COLLECTION)
    for row in data:
        try:
            # если вдруг будет http вместо https или поменяется поддомен, то
            # получим другой хэш (даже без него все равно уникальность сломается).
            # Хочется чуть больше стабильности =)
            # 'https://news.mail.ru/society/51496205/' =>
            # 'society51496205'
            news_unique_str = ''.join(row['link'].split('/')[3:5])
            news_hash = sha3_256(news_unique_str.encode('utf-8')).hexdigest()
            mailru_news_collection.insert_one({'_id': news_hash, **row})
        except DuplicateKeyError as e:
            logger.debug('Для ID=%s уже есть запись. Пропускаем', vacancy_id)  # noqa
            pass


def main():
    url = MAIN_URL
    logger.info('Parse %s', url)
    response = get_response(url)
    if not response:
        logger.error('NO response from %s', url)
        raise SystemExit(1)

    try:
        news_info_list = parse_response(response)
    except ValueError as e:
        logger.exception(e)
        save_to_file(response.text, 'error_response.html')
        raise SystemExit(1)

    logger.info('Сохраняю их в Mongo')
    save_to_mongo(news_info_list)


if __name__ == '__main__':
    logger.info('--- START')
    main()
    logger.info('--- END')
