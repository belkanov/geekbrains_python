import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from castorama_scrape.items import CastoramaScrapeItem
from itemloaders.processors import TakeFirst

class CastoramaSpider(scrapy.Spider):
    name = 'castorama'
    allowed_domains = ['castorama.ru']
    # https://www.castorama.ru/catalogsearch/result/?q=молоток&sc=wallpaper
    start_urls = ['https://www.castorama.ru/catalogsearch/result/?q=%D0%BC%D0%BE%D0%BB%D0%BE%D1%82%D0%BE%D0%BA&sc=wallpaper']

    def parse(self, response: HtmlResponse):
        next_page_href = response.css('div.toolbar-bottom a.next::attr(href)')
        if next_page_href:
            yield response.follow(next_page_href.get(), callback=self.parse)

        for link in response.css('ul.products-grid li a.product-card__name::attr(href)'):
            yield scrapy.Request(link.get(), callback=self.parse_page)

    def parse_page(self, response: HtmlResponse):
        item_loader = ItemLoader(item=CastoramaScrapeItem(), response=response)

        product_loader = item_loader.nested_css('div.col-main')
        product_loader.add_css('name', 'h1::text')
        product_id = product_loader.get_css('div.js-product-data::attr(data-product-id)', TakeFirst())
        product_loader.add_xpath('price', f'//*[@id="product-price-{product_id}"]//text()')
        item_loader.add_value('url', response.url)
        # мне крайне "повезло" и я нарвался на инцидент в PyPi =)
        # https://status.python.org/incidents/lgpr13fy71bk
        # не ставился Pillow (при установке ругался на большое кол-во редиректов)
        # в итоге сдача задержалась..
        product_loader.add_css('photos', 'div.product-media__top img.top-slide__img::attr(data-src)')

        # этот вариант у меня нормально не заработал,
        # часто были дубли и пропадала часть инфы
        # проверял вот тут - https://extendsclass.com/xpath-tester.html
        # там все успешно:
        # копировал div#specifications и смотрел работу (//dt/span[1] | //dd)/text()
        # Все мысли сводятся к многопоточности и race condition.
        # Возможно сам процесс дебага на это повлиял, но в остальных переменных все норм.
        # Может обработчик xpath в сложных примерах работает немного иначе,
        # чем в браузерах - я хз =)
        # specifications_loader = item_loader.nested_css('#specifications > dl')
        # specifications_loader.add_xpath('specifications', '(//dt/span[1] | //dd)/text()')

        keys = response.xpath('//*[@id="specifications"]/dl/dt/span[1]/text()').getall()
        keys = [k.replace('\n', '').strip() for k in keys]
        values = response.xpath('//*[@id="specifications"]/dl/dd/text()').getall()
        values = [v.replace('\n', '').strip() for v in values]
        item_loader.add_value('specifications', {k: v for k, v in zip(keys, values)})

        yield item_loader.load_item()

