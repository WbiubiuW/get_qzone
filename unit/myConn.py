# -*- coding:utf-8 -*-

import pymysql, os
from collections import namedtuple
from configparser import ConfigParser
from unit import get_driPath
import threading

"获取数据库连接对象"


class myConn(get_driPath.get_path):
    
    def __init__(self):
        self.conn = self.get_conn()
        self.coursor = self.conn.cursor()



    def get_conn(self):
        #获取数据库配置文件信息
        dirPath = self.get_driPath("resource", "db.ini")
        cfg = ConfigParser()
        cfg.read(dirPath, encoding="utf-8")

        for i in cfg.sections():
            conn = pymysql.connect(cfg.get('数据库', 'Host'), cfg.get('数据库', 'UserName'),
                                       cfg.get('数据库', 'Password'), cfg.get('数据库','Name'))
            return conn
        raise TypeError("数据库配置文件错误")

    def select(self, sql):
        resultObj = []

        self.coursor.execute(sql)
        # 获取数据库字段名
        keyName = [i[0] for i in self.coursor.description]

        tup = namedtuple("tup", keyName)

        tempData = self.coursor.fetchall()
        for i in tempData:
            tempTup = tup(*i)
            resultObj.append(tempTup)

        return resultObj

    def delete(self, sql):

        try:
            self.coursor.execute(sql)

            self.coursor.commit()

        except Exception as e:
            print(repr(e))
            self.coursor.rollback()

    def update(self, sql):

        try:
            self.coursor.execute(sql)

            self.get_conn().commit()

        except Exception as e:
            print(repr(e))
            self.get_conn().rollback()

    def insert(self, sql,msg):
        try:
            self.coursor.executemany(sql,msg)

            self.conn.commit()

        except Exception as e:
            print("insertError--------->{0}".format(msg))
            print("insertError--------->{0}".format(repr(e)))
            self.conn.rollback()

        finally:
            pass
            # self.coursor.close()
            # self.conn.close()



    def batchUpdate(self, sql,msg):

        try:
            self.coursor.executemany(sql,msg)

            self.conn.commit()

        except Exception as e:
            print("UpdateError--------->{0}".format(msg))
            print("UpdateError--------->{0}".format(repr(e)))
            self.conn.rollback()

    def selectMany(self, sql,msg):
        resultObj = []

        self.coursor.execute(sql,msg)
        # 获取数据库字段名
        keyName = [i[0] for i in self.coursor.description]
        tup = namedtuple("tup", keyName,rename=True)
        tempData = self.coursor.fetchall()
        for i in tempData:
            tempTup = tup(*i)
            resultObj.append(tempTup)

        return resultObj

    def closed(self):
        if self.conn:
            self.conn.close()

        if self.coursor:
            self.coursor.close()

if __name__ == "__main__":
    temp = myConn()
    sql = "show tables"
    updateSql = "update {0} set del_flasg=1.jpg where mes_id=1000060"

    try:
        obj = temp.select(sql)
        # temp.update(updateSql)
        for i in obj:
            temp.update(updateSql.format(i.Tables_in_mes_test))
    except:
        print(i.Tables_in_mes_test)


