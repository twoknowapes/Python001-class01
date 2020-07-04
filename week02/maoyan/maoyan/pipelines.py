# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql


class MysqlPipeline(object):
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            port=crawler.settings.get('MYSQL_PORT'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            database=crawler.settings.get('MYSQL_DATABASE'),
        )

    def open_spider(self, spider):
        self.conn = pymysql.connect(self.host,
                                    self.user,
                                    self.password,
                                    self.database,
                                    charset='utf8',
                                    port=self.port)
        self.cursor = self.conn.cursor()

        create_aql = '''
            CREATE TABLE movies(
                id int NOT NULL AUTO_INCREMENT,
                名称 val(200) NOT NULL,
                类型 val(50) NOT NULL,
                上映时间 val(100) NOT NULL,
                PRIMARY KET (id))
                ENGINE = MyIASM AUTO_INCREMENT = 1 DEFAULT  CHARSET = utf8mb4
        '''
        self.cursor.execute(create_aql)

    def process_item(self, item, spider):
        data = dict(item)
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        insert_sql = '''
        INSERT INTO TABLE movies(名称，类型，上映时间) VALUES (%s, %s, %s, %s)
        '''
        try:
            self.cursor.executemany(insert_sql, data)
            # self.cursor.execute(sql, tuple(data.values()))
        except:
            self.conn.rollback()
        finally:
            self.cursor.close()
            self.conn.close()
        return item
