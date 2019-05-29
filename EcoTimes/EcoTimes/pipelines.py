# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import urllib

class EcotimesPipeline(object):
    
    def __init__(self):
      #  self.conn = pymongo.MongoClient(
       #     '192.168.1.28',
        #    27017
        #)
       
        username = "admin"
        password = "athena"
        port = 27017
               
        self.client = pymongo.MongoClient('192.168.1.28', 27017)
        db = self.client['finbotdb']
        db.authenticate('admin', 'athena')
        self.collection = db['weekly_articles']

        

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item
