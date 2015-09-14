__author__ = 'sdg'

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor
import os
from lk.items import LkItem
pages = []
class LKSpider(CrawlSpider):
    name = "lk"
    allowed_domains = ['www.lkong.net']
    start_urls = ['http://www.lkong.net/forum-60-1.html']

    rules = (
        Rule(LinkExtractor(allow = ('/forum-60-\d{1,4}\.html', )), callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        #url = thread
        #for thread in response.xpath('//th[@class="new"]/a/@href').extract():
            #yield scrapy.Request(url, callback=self.parse_thread)
        if response.url not in pages:
            pages.append(response.url)
            with open('page', 'a+') as f:
                f.write(response.url + '\n')

    def parse_thread(self, response):
        item = LkItem()
        item['home'] = response.url
        item['title'] = response.xpath('//h1[@class="ts"]/a[1]/text()').extract()
        item['link'] = response.xpath('//h1[@class="ts"]/a[2]/@href').extract()
        item['content'] = response.xpath('//div[@id="postlist"]/div[1]/descendant::td[@class="t_f"]').extract()[0].encode('utf8')
        return item

'''
    start_urls = ['http://www.lkong.net/forum-60-1.html']

    def parse(self, response):
        #LKItem['title'] = response.xpath('//th[@class="new"]/a[1]/text()')
        for thread in response.xpath('//th[@class="new"]/a/@href').extract():
            url = thread
            yield scrapy.Request(url, callback=self.parse_thread)

    def parse_thread(self, response):
        item = LkItem()
        item['title'] = response.xpath('//h1[@class="ts"]/a[1]/text()').extract()
        item['link'] = response.xpath('//h1[@class="ts"]/a[2]/@href').extract()
        item['content'] = response.xpath('//td[@class="t_f"]/text()').extract()
        return item

'''
