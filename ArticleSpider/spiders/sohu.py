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
    list = ["思维", "撩妹", "撩汉", "格局", "商业模式", "谈判技巧"]
    list_type = ["thinking", "girl", "boy", "ambition", "businessModels", "negotiatingSkills"]

    def start_requests(self):
        print('请求中……')
        for index in range(len(self.list)):
            for i in range(1, 30):
                self.data["keyword"] = self.list[index]
                self.data['from'] = str(i * 10)
                yield scrapy.http.FormRequest(
                    self.start_urls[0],
                    meta={"article_type": self.list_type[index]},
                    headers={'content-type': 'application/x-www-form-urlencoded'},
                    formdata=self.data)

    def parse(self, response):
        python_content = json.loads(response.body)
        print(python_content)
        article_type = response.meta.get("article_type", "")
        count = len(python_content['data']['news'])  # 获取用户评论数（这里只是当前页的）
        if count != 0:
            for i in range(count):
                url = python_content['data']['news'][i]['url']
                image_news = python_content['data']['news'][i]['imageNews']
                if image_news:
                    front_image_url = python_content['data']['news'][i]['images']
                    image_url_list = front_image_url.split(',')
                    if len(image_url_list) > 0:
                        image_url = image_url_list[0].replace("[", "").replace("]", "").replace("\"", "")
                    else:
                        image_url = front_image_url
                else:
                    image_url = "images"
                print(url)
                yield Request(url=url, meta={"front_image_url": image_url, "article_type": article_type},
                              callback=self.parse_detail)

    def parse_detail(self, response):
        sohuItem = SohuItem()
        front_image_url = response.meta.get("front_image_url", "")
        article_type = response.meta.get("article_type", "")
        item_loader = ArticleItemLoader(item=sohuItem, response=response)
        item_loader.add_css("title", ".text-title h1::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("front_image_url", front_image_url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_value("article_type", article_type)
        item_loader.add_css("author_name", ".user-info h4 a::text")
        item_loader.add_css("publish_time", ".article-info span::text")
        item_loader.add_css("content", "article")
        item_loader.add_value("crawl_time", datetime.now())
        sohuItem = item_loader.load_item()
        yield sohuItem
