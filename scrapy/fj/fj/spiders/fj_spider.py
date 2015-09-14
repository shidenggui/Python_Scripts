__author__ = 'sdg'

import urllib
import urllib2
import os
import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spider import CrawlSpider,Rule
from fj.items import FjItem

class Fj_Spider(CrawlSpider):
    name = 'fj'
    allow_domains = ['ipaddr']
    start_urls = ['index.php']
    rules = (
        Rule(LinkExtractor(allow=('aid=\d+',)), callback='parse_thread', follow=True),
    )

    def start_requests(self):
        yield scrapy.FormRequest('login.php',
                                  formdata={
                                     'fmdo':'login',
                                      'dopost':'login',
                                      'gourl':'',
                                      'userid':'username',
                                      'pwd':'password',
                                      'vdcode':'',
                                      'keeptime':'2592000'
                                  },
                                  callback=self.after_login
                              )

    def after_login(self, response):
        for url in start_urls:
            yield self.make_requests_from_url(url)


    def parse_thread(self, response):
        item = FjItem()
        item['link'] = response.url
        item['title'] = response.xpath('//div[@class="title"]/text()').extract()
        item['content'] = response.xpath('//div[@class="content"]/text()').extract()
        item['fj'] = response.xpath('//div[@class="intro"]/a/@href').extract()
        fjnames = response.xpath('//div[@class="intro"]/a/text()').extract()
        for fjurl,name in item['fj'][:-1], fjnames:
            urllib.urlretrieve(fjurl, name)
        return item

