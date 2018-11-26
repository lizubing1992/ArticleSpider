# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import json
from ArticleSpider.items import SohuItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5
from datetime import datetime


class SohuSpider(scrapy.Spider):
    name = 'sohu'
    start_urls = ['https://search.sohu.com/outer/search/news']
    data = {
        'keyword': '思维',
        'size': '10',
        'SUV': '1809052201174155',
        'terminalType': 'pc',
        'source': 'article',
        'queryType': 'edit'
    }

    def start_requests(self):
        print('请求中……')
        for i in range(1, 100):
            self.data['from'] = str(i * 10)
            yield scrapy.http.FormRequest(
                self.start_urls[0],
                headers={'content-type': 'application/x-www-form-urlencoded'},
                formdata=self.data)

    def parse(self, response):
        python_content = json.loads(response.body)
        print(python_content)
        count = len(python_content['data']['news'])  # 获取用户评论数（这里只是当前页的）
        for i in range(count):
            url = python_content['data']['news'][i]['url']
            print(url)
            yield Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        sohuItem = SohuItem()
        item_loader = ArticleItemLoader(item=sohuItem, response=response)
        item_loader.add_css("title", ".text-title h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_value("article_type", self.get_article_type())
        item_loader.add_css("author_name", ".user-info h4 a::text")
        item_loader.add_css("publish_time", ".article-info span::text")
        item_loader.add_css("content", "article")
        item_loader.add_value("crawl_time", datetime.now())
        sohuItem = item_loader.load_item()
        yield sohuItem

    def get_article_type(self):
        return "thinker"
