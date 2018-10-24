# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ArticleSpider.items import GrfyItemLoader, GrfyItem
from ArticleSpider.utils.common import get_md5
from datetime import datetime


class GrfySpider(CrawlSpider):
    name = 'grfy'
    allowed_domains = ['sh.grfy.net']
    start_urls = ['http://sh.grfy.net/']

    headers = {
        "HOST": "sh.grfy.net",
        "Referer": "http://sh.grfy.net/",
        'User-Agent': "MMozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0"
    }

    rules = (
        Rule(LinkExtractor(allow="rent/d-.*"), process_request='request_tagPage', callback='parse_item', follow=True),
    )

    def request_tagPage(self, request):
        newRequest = request.replace(headers=self.headers)
        newRequest.meta.update(cookiejar=1)
        return newRequest

    def parse_item(self, response):
        item_loader = GrfyItemLoader(item=GrfyItem(), response=response)
        item_loader.add_xpath("city", "//*[@class='cr_left']/dl[4]/dd/text()")
        item_loader.add_xpath("village_name", "//*[@class='cr_left']/dl[3]/dd/text()")
        item_loader.add_xpath("room_num", "//*[@class='cr_left']/dl[4]/dd/text()")

        landlord_phone = response.css(".redtelphone::text").TakeFirst()
        if len(landlord_phone):
            landlord_phone = ["暂无数据"]
        item_loader.add_value("landlord_phone", landlord_phone)
        item_loader.add_xpath("landlord_name", "//*[@class='cr_left']/dl[7]/dd/text()")
        item_loader.add_xpath("bedroom_num", "//*[@class='cr_left']/dl[2]/dd/text()")
        item_loader.add_xpath("living_room_num", "//*[@class='cr_left']/dl[2]/dd/text()")
        item_loader.add_xpath("toilet_num", "//*[@class='cr_left']/dl[2]/dd/text()")
        item_loader.add_xpath("room_area", "//*[@class='cr_left']/dl[2]/dd/text()")
        item_loader.add_css("mark", ".infoitem .des")
        item_loader.add_value("create_date", datetime.now())
        grfy_item = item_loader.load_item()
        return grfy_item
