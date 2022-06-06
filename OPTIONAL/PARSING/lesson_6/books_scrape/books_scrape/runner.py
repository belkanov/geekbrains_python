"""
I вариант
1) Доработать паука в имеющемся проекте, чтобы он формировал item по структуре:
*Наименование вакансии
*Зарплата от
*Зарплата до
*Ссылку на саму вакансию
И складывал все записи в БД(любую)

2) Создать в имеющемся проекте второго паука по сбору вакансий с сайта superjob. Паук должен формировать item'ы по аналогичной структуре и складывать данные также в БД

II вариант
1) Создать пауков по сбору данных о книгах с сайтов labirint.ru и/или book24.ru
2) Каждый паук должен собирать:
* Ссылку на книгу
* Наименование книги
* Автор(ы)
* Основную цену
* Цену со скидкой
* Рейтинг книги
3) Собранная информация должна складываться в базу данных
"""

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from books_scrape.spiders.labirint import LabirintSpider

if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    # CrawlerRunner рассчитан на встройку в приложение, которое уже написано
    # на Twisted. Поэтому рекомендуется даже для одного паука не забывать про
    # работу с реактором (reactor.stop())
    # Более простой вариант - через CrawlerProcess
    # https://doc.scrapy.org/en/latest/topics/practices.html
    runner = CrawlerRunner(settings)

    deferred = runner.crawl(LabirintSpider)
    deferred.addBoth(lambda _: reactor.stop())

    reactor.run()  # the script will block here until the crawling is finished
