# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class JianshuitPipeline(object):
    def __init__(self):
        conn = pymysql.connect(host='localhost', user='root', passwd='', db='mydb', port=3306, charset='utf8')
        cursor = conn.cursor()
        self.post = cursor

    def process_item(self, item, spider):
        cursor = self.post
        cursor.execute("use mydb")
        sql = "insert into jianshuit (user0, time0, title, view0, comment0, like0, reward) values (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (item['user'], item['time'], item['title'], item['view'], item['comment'], item['like'], item['reward']))
        cursor.connection.commit()
        return item
