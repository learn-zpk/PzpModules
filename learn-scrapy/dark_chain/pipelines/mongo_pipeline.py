import pymongo

from ..items import DarkChainDomainNameItem


class ItemWritePipeline(object):
    """
    项目管道：用于清理、验证、持久化等操作
    """
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'books')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db.drop_collection("dark_domainname")

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        # if isinstance(item, DarkChainUrlItem):
        #     self.db["dark_url"].insert(dict(item))

        if isinstance(item, DarkChainDomainNameItem):
            if not item['domainname'] or '.' not in item['domainname']:
                return
            if not self.db['dark_domainname'].find_one({"domainname": item['domainname'], 'typo': item['typo']}):
                self.db['dark_domainname'].insert_one(
                    ({'domainname': item['domainname'], 'typo': item['typo'], 'num': 0, 'origin_urls': []}))

            self.db['dark_domainname'].find_and_modify(
                {"domainname": item['domainname'], 'typo': item['typo']},
                {'$inc': {'num': 1}, "$push": {"origin_urls": item['origin_url']}}
            )
        return item
