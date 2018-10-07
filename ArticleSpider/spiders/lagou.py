# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ArticleSpider.items import LagouItemLoader, LagouJobItem
from ArticleSpider.utils.common import get_md5
from datetime import datetime


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/']

    headers = {
        "HOST": "www.lagou.com",
        "Referer": "http://www.lagou.com/",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
    }

    rules = (
        #
        Rule(LinkExtractor(allow=("zhaopin/.*",)), process_request='request_tagPage', follow=True),
        Rule(LinkExtractor(allow=("gognsi/j\d+.html/",)), process_request='request_tagPage', follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), process_request='request_tagPage', callback='parse_item',
             follow=True),
    )

    def request_tagPage(self, request):
        newRequest = request.replace(headers=self.headers)
        newRequest.meta.update(cookiejar=1)
        return newRequest

    def parse_item(self, response):
        item_loader = LagouItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_css("title", ".job-name::attr(title)")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_css("salary", ".job_request .salary::text")
        item_loader.add_xpath("job_city", "//*[@class='job_request']/p/span[2]/text()")
        item_loader.add_xpath("work_years", "//*[@class='job_request']/p/span[3]/text()")
        item_loader.add_xpath("degree_need", "//*[@class='job_request']/p/span[4]/text()")
        item_loader.add_xpath("job_type", "//*[@class='job_request']/p/span[5]/text()")
        item_loader.add_css("tags", ".position-label  .labels::text")
        item_loader.add_css("publish_time", ".publish_time::text")
        item_loader.add_css("job_advantage", ".job-advantage p::text")
        item_loader.add_css("job_desc", ".job_bt div p::text")
        item_loader.add_css("job_addr", ".work_addr")
        item_loader.add_css("company_name", "#job_company dt a img::attr(alt)")
        item_loader.add_css("company_url", "#job_company dt a::attr(href)")
        item_loader.add_value("crawl_time", datetime.now())
        job_item = item_loader.load_item()
        return job_item
