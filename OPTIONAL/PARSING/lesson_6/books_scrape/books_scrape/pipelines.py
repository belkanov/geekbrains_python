# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from books_scrape.items import BooksScrapeItem


class BooksScrapePipeline:
    def __init__(self):
        # без всяких .env и докеров в этот раз.
        client = MongoClient('localhost', 27017)
        self.mongobase = client.bookscrape

    def process_item(self, item: BooksScrapeItem, spider):
        item['name'] = item['name'].replace('\n', ' ').strip()
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item
