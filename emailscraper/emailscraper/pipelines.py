# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import csv

class EmailscraperPipeline(object):
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        output_file = open('output.csv', 'w')
        writer = csv.writer(output_file)
        writer.writerow(["url","email","phone"])
        output_file.close()

        email_file = open('emails.csv', 'w')
        email_file.close()

    def spider_closed(self, spider):
        pass

    def process_item(self, item, spider):
        return item
