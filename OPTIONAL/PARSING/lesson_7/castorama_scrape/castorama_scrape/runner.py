"""
1) Взять любую категорию товаров на сайте https://www.castorama.ru/. Собрать следующие данные:
● название;
● все фото;
● ссылка;
● цена.

Реализуйте очистку и преобразование данных с помощью ItemLoader. Цены должны быть в виде числового значения.

Дополнительно:
2)Написать универсальный обработчик характеристик товаров, который будет формировать данные вне зависимости от их типа и количества.

3)Реализовать хранение скачиваемых файлов в отдельных папках, каждая из которых должна соответствовать собираемому товару
"""

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from castorama_scrape.spiders.castorama import CastoramaSpider

if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    # CrawlerRunner рассчитан на встройку в приложение, которое уже написано
    # на Twisted. Поэтому рекомендуется даже для одного паука не забывать про
    # работу с реактором (reactor.stop())
    # Более простой вариант - через CrawlerProcess
    # https://doc.scrapy.org/en/latest/topics/practices.html
    runner = CrawlerRunner(settings)

    deferred = runner.crawl(CastoramaSpider)
    deferred.addBoth(lambda _: reactor.stop())

    reactor.run()  # the script will block here until the crawling is finished
