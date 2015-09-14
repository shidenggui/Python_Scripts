#coding:utf-8
__author__ = 'sdg'

import scrapy
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor

start_url = ['http://www.lkong.net/forum-14-1.html']
class LkLoginSpider(CrawlSpider):
    name = "lkl"
    allowed_domains = ['www.lkong.net']
    #start_urls = ['http://www.lkong.net/member.php?mod=logging&action=login']
    #start_urls = ['http://www.lkong.net/forum-14-1.html']

    rules = (
        Rule(LinkExtractor(allow=('/thread.+\.html', )), callback='parse_thread'),
    )

    def start_requests(self):
        return [scrapy.FormRequest('http://www.lkong.net/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=L7On7&inajax=1',
                                   formdata={'username':'username',
                                             'password':'password',
                                             'answer':'email',
                                             'formhash':'forumhash',
                                             'referer':'/forum.php',
                                             'questionid':'0',
                                             'loginsubmit':'True',
                                             'cookietime':'2592000'},
                                   callback=self.after_login)]


    def after_login(self, response):
        #print response.body.decode('utf8')
        for url in start_url:
            yield self.make_requests_from_url(url)

    def parse_thread(self, response):
        print response.body.decode('utf8')
        print response.url
        #print response.body.decode('utf8')

    #def make_requests_from_url(self, url):
        #return [scrapy.Request(url)]
    #def make_requests_from_url(self, url):

