import scrapy


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['http://labirint.ru/']

    def parse(self, response):
        pass
