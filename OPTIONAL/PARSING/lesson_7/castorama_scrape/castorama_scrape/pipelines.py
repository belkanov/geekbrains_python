# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class CastoramaScrapePipeline:
    def __init__(self):
        client = MongoClient(host='localhost',
                             port=27017,
                             username='username',
                             password='password')
        self.mongobase = client.castoramacrape
        super().__init__()

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item


class CastoramaPhotosScrapePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [result[1] for result in results if result[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        default_file_path = super().file_path(request, response, info, item=item)
        new_file_path = default_file_path.split('/')  # возможно тут стоит использовать os.sep
        # https://www.castorama.ru/molotok-slesarnyj-stanley-500-g
        new_file_path.insert(1, item['url'].split('/')[-1])
        new_file_path = '/'.join(new_file_path)
        return new_file_path



