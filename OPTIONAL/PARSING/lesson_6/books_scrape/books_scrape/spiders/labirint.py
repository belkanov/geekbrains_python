import scrapy
from scrapy.http import HtmlResponse
from books_scrape.items import BooksScrapeItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    # https://www.labirint.ru/search/программирование/
    start_urls = ['https://www.labirint.ru/search/%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5/']

    def parse(self, response: HtmlResponse):
        next_page_href = response.xpath('//a[@class="pagination-next__text"]/@href').get()
        if next_page_href:
            yield response.follow(next_page_href, callback=self.parse)
        yield from self.parse_books(response)

    def parse_books(self, response: HtmlResponse):
        for book in response.css('div.card-column'):
            anchor = book.xpath('./div')

            url = response.urljoin(anchor.xpath('.//a[@class="cover"]/@href').get())
            name = anchor.xpath('./@data-name').get()
            main_price = anchor.xpath('./@data-price').get()
            sale_price = anchor.xpath('./@data-discount-price').get()
            # Авторов иногда нет, например https://www.labirint.ru/books/10000623/
            # хотя на фотке книги он есть.
            # Так же всегда работаем со списком (даже если автор только один)
            authors = anchor.xpath('./div[@class="product-author"]/a/@title').getall()
            # Решил вместо рейтинга собирать кол-во рецензий. Так решил только потому,
            # что это всё-таки ДЗ, а не ПРОД задание. Сбор рецензий вместо рейтинга
            # позволяет не проваливаться в саму книгу => значительно уменьшается поток
            # запросов. Это скорее из этичных соображений =)
            # Имя переменой немного не соответствует фактическим данным,
            # но будем считать это рейтингом
            rating = None
            rating_anchor = anchor.xpath('.//a[starts-with(@href,"/reviews")]')
            if rating_anchor:
                rating = rating_anchor.xpath('./@data-event-content').get()

            yield BooksScrapeItem(
                url=url,
                name=name,
                main_price=main_price,
                sale_price=sale_price,
                authors=authors,
                rating=rating,
            )
