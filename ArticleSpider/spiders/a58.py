# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class A58Spider(CrawlSpider):
    name = '58'
    allowed_domains = ['sz.58.com']
    start_urls = ['http://sz.58.com/']

    rules = (
        Rule(LinkExtractor(allow="zufang/.*"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
