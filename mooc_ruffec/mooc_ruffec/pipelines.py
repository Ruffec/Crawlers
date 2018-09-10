# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymysql.cursors
import pymysql.err as err
from pymysql import Error
from scrapy.utils.project import get_project_settings

class MoocRuffecPipeline(object):
    def process_item(self, item, spider):
        try:
            self.creatdatabase()
            self.createTable()
        # except (err.ProgrammingError, err.InternalError):
        except (Error):
            print("数据库或表 已存在！跳过")
            pass
        # 添加数据到数据库中
        self.storeDB(item)
        print("保存item".center(50, '*'))

    def __init__(self):
        self.settings = get_project_settings()
        self.host = self.settings["MYSQL_HOST"]
        self.user = self.settings['MYSQL_USER']
        self.passwd = self.settings['MYSQL_PASSWD']
        self.db = self.settings['MYSQL_DBNAME']

    # 连接到mysql，不是连接到具体的数据库
    def connectMysql(self):
        conn = pymysql.connect(host=self.host,
                               user=self.user,
                               passwd=self.passwd,
                               # db=self.db,不指定数据库名
                               charset='utf8')  # 要指定编码，否则中文可能乱码
        return conn
    #  # 连接到具体的数据库（settings中设置的MYSQL_DBNAME）
    def connectDatabase(self):

        conn = pymysql.connect(host=self.host,
                               user=self.user,
                               passwd=self.passwd,
                               db=self.db,
                               charset='utf8')  # 要指定编码，否则中文可能乱码
        return conn
    # 创建数据库
    def creatdatabase(self):
        con = self.connectMysql()#连接数据库
        '''因为创建数据库直接修改settings中的配置MYSQL_DBNAME即可，所以就不要传sql语句了'''
        sql = "create database if not exists "+self.db
        cur = con.cursor()
        # 执行语句
        cur.execute(sql)
        cur.close()
        con.close()

    # 创建表
    def createTable(self):
        conn = self.connectDatabase()
        sql = "create table mooc( title varchar(50) PRIMARY KEY ,url varchar(200)," \
              " image_url varchar(200), introduction varchar(200), student varchar(200))"
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.close()
        self.table = True


    # 添加数据到数据库
    def storeDB(self, item):
        conn = self.connectDatabase()
        to = len(item.get("title", ''))
        for i in range(to):
            sql = "insert into mooc(title, url, image_url, introduction, student) " \
                  "values(\"%s\", \"%s\", \"%s\", \"%s\",\"%s\")" \
                  % (item.get("title", "")[i],
                     item.get("url", ""),
                     item.get("image_url", "")[i],
                     item.get("introduction", "")[i],
                     item.get("student", ""))

            conn.cursor().execute(sql)
            conn.commit()
        print('----------------------')
        print('数据成功保存到数据库中！')
        print('----------------------')
        return item
    # 关闭数据库
    def closeDB(self):
        con = self.connectDatabase()
        con.close()
    def __del__(self):
        self.closeDB()

