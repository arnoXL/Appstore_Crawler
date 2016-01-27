# -*- coding: utf-8 -*-

# This file defined the scraped items
#

import scrapy

class AppstoreItem(scrapy.Item):
    # the app's name
    title = scrapy.Field()

    # the app's url
    url = scrapy.Field()

    # app ID
    appid = scrapy.Field()

    # introduction of the app
    intro = scrapy.Field()

    # recommended apps for the app
    recommended = scrapy.Field()

    # thumbnail url of the app
    thumb = scrapy.Field()