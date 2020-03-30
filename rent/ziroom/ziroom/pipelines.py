# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
# 使用scrapy 底层的Twisted 创建异步存储
from twisted.enterprise import adbapi
from pymysql import cursors 

# 同步插入，慢
class ZiroomPipeline(object):
    def __init__(self):
        # mysql 参数
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '1234',
            'database': 'ziroom',
            'charset': 'utf8', # mysql中所有的都是utf8没有utf-8
            }
        # 创建连接对象,**dbparams 关键字传参，键值对形式，如 'host' = '127.0.0.1'
        self.conn = pymysql.connect(**dbparams)
        # 创建游标
        self.cursor = self.conn.cursor()
        # 保存 sql 语句
        self._sql = None

    def process_item(self, item, spider):
        # 执行sql语句
        self.cursor.execute(self.sql,(item['title'],item['desc'],item['location'],item['city'],item['region'],item['price'],
        item['room_url'],item['prices_url']))
        # 提交到数据库
        self.conn.commit()  
        return item  

    # 将 item 中的数据插入数据库,所以先定义好 sql 语句
    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into city(Id, title, area, location, city, region, price,room_url,
            price_url) 
            values(null,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql    

# 异步插入，快
class TwistedPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '1234',
            'database': 'ziroom',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor # 需要指定游标的类
            }
        # 设置连接池
        self.dbpool = adbapi.ConnectionPool('pymysql',**dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into city(Id, title, area, location, city, region, price,room_url,
            price_url) 
            values(null,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        # 将insert_item 给 runInteraction 执行就可以实现异步
        defer = self.dbpool.runInteraction(self.insert_item, item)
        # 添加错误处理，想知道是哪个 item 出错，所以传入 item 参数，同理传入 spider 
        defer.addErrback(self.handle_error,item, spider)

    # item 是 process_item
    def insert_item(self, cursor, item):
        cursor.execute(self.sql,(item['title'],item['desc'],item['location'],item['city'],item['region'],item['price'],
        item['room_url'],item['prices_url']))
        
    # 添加错误处理
    def handle_error(self,errors,item,spider):
        print("="*10)
        print(errors)
        print("="*10)
