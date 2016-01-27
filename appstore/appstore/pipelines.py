# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AppstorePipeline(object):
    def __init__(self):
        self.file = open('appstore.dat', 'wb')

    def process_item(self, item, spider):
        # the app info will be output into "appstore.dat" file
        val = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(item['appid'],
                item['url'], item['title'], item['intro'],
                item['thumb'], item['recommended'])
        self.file.write(val)
        return item
