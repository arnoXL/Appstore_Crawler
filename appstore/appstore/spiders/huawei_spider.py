# -*- coding: utf-8 -*-

# This file is used for crawl app info from Huawei Market website.
# It use splash service and scrapyjs to render javascript on the web.
# The splash service IP is assumed as http://192.168.99.100:8050,
# you can change it to your splash service in settings.py file.
# This file just crawl first 5 pages of two list on homepage and all
# the searches, you can just uncomment and comment some codes to get all 
# apps info. The details can be found in comments below, around
# line 26 and line 87.

import scrapy
import re

from scrapy.selector import Selector
from appstore.items import AppstoreItem

class HuaweiSpider(scrapy.Spider):
    # spider name
    name = 'huawei'
    allowed_domains = ["huawei.com"]

    # these urls will be used as a start point to crawl info
    start_urls = [
        # All lists on home page, for here just crawl two of them.
        # If you want to find all lists' apps info, just uncomment
        # these urls.
        "http://appstore.huawei.com/more/all",
        "http://appstore.huawei.com/more/recommend",
        # "http://appstore.huawei.com/more/soft",
        # "http://appstore.huawei.com/more/game",
        # "http://appstore.huawei.com/more/newPo",
        # "http://appstore.huawei.com/more/newUp",
        # 
        # searches
        "http://appstore.huawei.com/search/game",
        "http://appstore.huawei.com/search/software"
    ]

    # to start the crawl process
    def start_requests(self):
        for url in self.start_urls:
            # Use splash to render javascript.
            # The result will be returned in a render.html.
            # Use self.parse function to find information which is useful
            # to us.
            yield scrapy.Request(url, self.parse, meta={
            'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 0.5}
                }
            })


    # used to extract app info
    def parse(self, response):
        page = Selector(response)
        # get all apps url in this page
        hrefs = page.xpath('.//h4[@class="title"]/a/@href')

        for href in hrefs:
            url = href.extract()
            # go to each app's page to get the info with self.parse_item func
            request =  scrapy.Request(url, callback=self.parse_item, meta={
            'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': 0.5}
                }
            })

            # pass the app's url to self.parse_item function
            request.meta['url'] = url
            yield request

        for i in range(1, 10):
            # get next page's url
            nextpath = ('//div[@class="page-ctrl ctrl-app"]/a[' 
                        + str(i) + ']/text()')

            # find the page number of the "next page"
            # (Chinese words "下一页" means "next page")
            if page.xpath(nextpath).extract_first().encode('utf-8') == "下一页":
                nextpage = page.xpath('//div[@class="page-ctrl ctrl-app"]/a[' 
                                      + str(i) + ']/@href').extract_first()

                # for here jsut crawl first 5 pages of each start url
                # can crawl all pages by deleting these 3 lines code below
                temp = nextpage.split("/")
                if int(temp[-1]) > 5:
                    break

                yield scrapy.Request(nextpage, callback=self.parse, meta={
                'splash': {
                        'endpoint': 'render.html',
                        'args': {'wait': 0.5}
                    }
                })
                break

    def parse_item(self, response):
        page = Selector(response)
        item = AppstoreItem()

        # get app's title
        item['title'] = page.xpath('.//ul[@class="app-info-ul nofloat"]'
         + '/li/p/span[@class="title"]/text()').extract_first().encode('utf-8')

        # get app's url passed by self.parse
        item['url'] = response.meta['url']

        # get appID
        item['appid'] = re.match(r'http://.*/(.*)', item['url']).group(1)

        # get all introduction of the app
        allIntro = ""
        introList = page.xpath('.//div[@id="app_strdesc"]/text()').extract()
        for ele in introList:
            allIntro += ele.encode('utf-8')
        introduct = "introduction: {0}".format(allIntro)
        item['intro'] = introduct

        # get thumbnail url of the app
        thumbn = page.xpath('.//ul[@class="app-info-ul nofloat"]/'
            + 'li[@class="img"]/img[@class="app-ico"]/@src').extract_first()

        item['thumb'] = "thumbnail URL: {0}".format(thumbn)

        # get all recommended apps for the app
        divs = page.xpath('//div[@class="open-info"]')
        recomm = ""
        for div in divs:
            # extract each recommended app's info
            url = div.xpath('./p[@class="name"]/a/@href').extract_first()
            recommended_appid = re.match(r'http://.*/(.*)', url).group(1)
            name = div.xpath('./p[@class="name"]'
                             + '/a/text()').extract_first().encode('utf-8')
            recomm += "recommendation {0}:{1},".format(recommended_appid, name)
        item['recommended'] = recomm

        yield item