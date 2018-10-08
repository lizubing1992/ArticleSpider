# -*- coding: utf-8 -*-

import codecs
import json

import MySQLdb
import MySQLdb.cursors
from scrapy.exporters import JsonItemExporter
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    # 提取settings中的配置数据
    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        # twist 异步mysql
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)

    # 处理异步数据插入异常
    def handle_error(self, failure):
        print(failure)

    def do_insert(self, cursor, item):
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)
        # 执行插入逻辑
        # insert_sql = """
        #            insert into article(title, url, url_object_id, create_date, fav_nums, front_image_url, front_image_path, praise_nums, comment_nums,tags,content)
        #            VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        #        """
        # cursor.execute(insert_sql, (
        #     item["title"], item["url"], item["url_object_id"], item["create_date"], item["fav_nums"],
        #     item["front_image_url"], item["front_image_path"], item["praise_nums"], item["comment_nums"], item["tags"],
        #     item["content"]))


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'article_spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into article(title, url, url_object_id, create_date, fav_nums, front_image_url, front_image_path, praise_nums, comment_nums,tags,content)
            VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (
            item["title"], item["url"], item["url_object_id"], item["create_date"], item["fav_nums"],
            item["front_image_url"], item["front_image_path"], item["praise_nums"], item["comment_nums"], item["tags"],
            item["content"]))
        self.conn.commit()


class JsonExporterPipeline(object):
    # 调用scrapy提供的json export 导出json
    def __init__(self):
        self.file = open('articleexporter.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class JsonWithEncodingPipeline(object):
    # 使用json 导出
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


# 图片下载的pipeline
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        # 图片下载完成把 图片路劲path写回item中
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path

        return item
