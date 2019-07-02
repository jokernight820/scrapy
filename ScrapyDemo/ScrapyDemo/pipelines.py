# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql as sql
import pymysql.cursors
import scrapy

config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '12345678',
    'db': 'scrapy',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}





class ScrapyDemoPipeline(object):

    def __init__(self):
        # 连接数据库
        self.db = sql.connect(**config)
        self.cursor = self.db.cursor()

    def process_item(self, item, spider):
        # 先保存作者信息
        sql = 'INSERT INTO author (name, birthdate, address, bio) VALUES (%s, %s, %s, %s)'
        self.cursor.execute(sql, (item['author']['name'], item['author']['birthday'], item['author']['address'], item['author']['description']))
        # 获取作者id
        author_id = self.cursor.lastrowid

        # 保存引述信息
        sql = 'INSERT INTO quotes (text, author,tags ) VALUES (%s, %s, %s)'
        self.cursor.execute(sql, (item['text'], ','.join(item['tags']), author_id))
        self.db.commit()

    # 即将结束爬虫
    def close_spider(self, spider):
        self.db.close()
        self.cursor.close()
        print('close db')