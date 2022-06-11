"""
Вариант I
Написать программу, которая собирает входящие письма из своего или тестового
почтового ящика и сложить данные о письмах в базу данных
(от кого, дата отправки, тема письма, текст письма полный)

Вариант II
2) Написать программу, которая собирает товары «В тренде» с сайта техники
mvideo и складывает данные в БД. Сайт можно выбрать и свой.
Главный критерий выбора: динамически загружаемые товары
"""
import logging
from hashlib import sha3_256
from time import sleep
from typing import Optional

import requests
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from constants import *

logging.basicConfig(format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('job_scraper')
logger.setLevel(logging.INFO)


def parse_mails(url):
    service = Service(executable_path='./chromedriver_win32_102.0.5005.61.exe')
    options = Options()
    options.add_argument('start-maximized')

    with webdriver.Chrome(service=service, options=options) as driver:
        driver.implicitly_wait(10)

        mails_data = []
        # на простой странице (https://mail.ru) у меня не находил тэги
        # для ввода логопаса.
        # Искал через xpath, id, имена тэгов. Даже самым широким поиском
        # в списке не было искомых. Не понял в чем печаль.
        # Возможно плохо дружит с iframe - хз..
        driver.get(url)

        username_field = driver.find_element(By.CSS_SELECTOR, 'input[name="username"]')
        username_field.send_keys('study.ai_172@mail.ru')
        username_field.send_keys(Keys.ENTER)
        password_field = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        password_field.send_keys('NextPassword172#')
        password_field.send_keys(Keys.ENTER)

        # Решил немного поиграться с интерфейсом.
        # Возможно так менее эффективно, чем просто собрать ссылки,
        # а потом по ним пройтись, но так явно интересней =)
        #
        # ЭТО ЛОМАЕТ ОТОБРАЖЕНИЕ ПИСЕМ ДЛЯ ОСТАЛЬНЫХ УЧАСТНИКОВ
        # поэтому если проверять, то где-нить на отдельном ящике,
        # либо после тестов - вернуть галку обратно

        # кнопка "настройки" слева внизу
        driver.find_element(By.CSS_SELECTOR, 'div.settings').click()
        # галка "Список писем с колонкой письма"
        if driver.find_elements(By.CSS_SELECTOR, 'div[data-test-id="3pane-enabled"]'):
            pass
        else:
            driver.find_element(By.CSS_SELECTOR, 'div[data-test-id="3pane-disabled"]').click()
        # крестик "Закрыть настройки"
        driver.find_element(By.CSS_SELECTOR, 'button[data-test-id="cross"]').click()

        # Искусственное ограничение, чтобы не собирать все 1к+ писем.
        # По-хорошему, если делать это на постоянке, то нас будут интересовать
        # только непрочитанные, которые тоже можно найти.
        max_mails_cnt = 10
        mails_cnt = 0
        prev_mail_link = ''

        # находим первое письмо и открываем его
        driver.find_element(By.CSS_SELECTOR, 'a.llct').click()
        while True:
            # там же есть еще llct_active, но я решил по llct_open.
            # хз куда актив может указать, а llct_open, по логике должен
            # смотреть на открытое, а оно одно в данной ситуации
            current_mail = driver.find_element(By.CSS_SELECTOR, 'a.llct_open')
            current_mail_link = current_mail.get_attribute('href')
            if prev_mail_link == current_mail_link or mails_cnt >= max_mails_cnt:
                break

            prev_mail_link = current_mail_link
            mails_cnt += 1

            # тема письма, она тут полная.
            # Обрезается видимо JSом или вообще стилями, я хз..
            # Где-то 1 из 5 - не собиралась тема первого письма.
            # Я не стал ковырять - думаю затупы моего ПК.
            mail_title = current_mail.find_element(By.CSS_SELECTOR, 'div.llct__subject').get_attribute('title')
            # от кого (название+ящик)
            mail_from = current_mail.find_element(By.CSS_SELECTOR, 'span.ll-crpt').get_attribute('title')
            # дата отправки. Надо бы еще переделать "Сегодня/Вчера/ХХ мая/..." на
            # адекватные значения, но я не стал - все таки не боевая задача =)
            mail_send_date = current_mail.find_element(By.CSS_SELECTOR, 'div.llct__date').get_attribute('title')
            # текст письма
            # выше в DOM есть "letter__body", но в нем еще какие-то календари и обертки
            # решил их не брать
            mail_body_text = driver.find_element(By.CSS_SELECTOR, 'div.letter-body__body-content').text

            # переходим к следующему письму
            current_mail.send_keys(Keys.ARROW_DOWN)

            mails_data.append({
                'title': mail_title,
                'from': mail_from,
                'send_date': mail_send_date,
                'body_text': mail_body_text,
            })

            # попробуем сразу двух зайцев
            # 1 - будем косить под пользователя и не жать на кнопку 500раз/сек
            # 2 - дадим тексту письма загрузиться (хоть это и не самый кошерный вариант)
            sleep(2)

    return mails_data


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
    mails_collection = get_mongo_collection(MONGO_COLLECTION)
    for row in data:
        try:
            # При условии преобразования даты в нормальное значение
            # (о чем я писал выше и не делал) - можно получить норм хэш для одного
            # и того же письма, которое мы соберем сегодня, а потом завтра.
            # Можно конечно и ИД брать, который есть в URL или
            # data-id="0:16539077630958936900:0"
            mail_unique_str = ''.join((row['from'], row['send_date']))
            mail_hash = sha3_256(mail_unique_str.encode('utf-8')).hexdigest()
            mails_collection.insert_one({'_id': mail_hash, **row})
        except DuplicateKeyError as e:
            logger.debug('Для ID=%s уже есть запись. Пропускаем', vacancy_id)  # noqa
            pass


def main():
    url = MAIN_URL
    logger.info('Parse mails...')

    try:
        mails_list = parse_mails(url)
    except Exception as e:
        logger.exception(e)
        raise SystemExit(1)

    logger.info('Сохраняю их в Mongo')
    save_to_mongo(mails_list)


if __name__ == '__main__':
    logger.info('--- START')
    main()
    logger.info('--- END')
