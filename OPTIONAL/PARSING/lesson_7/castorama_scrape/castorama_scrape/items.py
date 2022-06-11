# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def clear_text(value):
    return value.replace('\n', '').strip()


def remove_inner_spaces(value):
    return value.replace(' ', '')


def make_int(value):
    result = value
    try:
        result = int(value)
    except:
        pass
    return result


class CastoramaScrapeItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(
        input_processor=MapCompose(clear_text, remove_inner_spaces, make_int),
        output_processor=TakeFirst()
    )
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    # это пригодилось, если бы работал specifications_loader
    # specifications = scrapy.Field(input_processor=MapCompose(clear_text))
    specifications = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field()  # for MongoDB

