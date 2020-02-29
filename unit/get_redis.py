#!/usr/bin/python
# -*- coding: UTF-8 -*-

import redis
import pymysql

mysqlHost='192.168.100.41'
mysqlPort=3306
mysqlUser='root'
mysqlPassword='Qianxin123'
mysqlDb='mes_test'
mysqlCharset='utf8'

redisHost='172.16.0.31'
redisPort=6379
redisPassword='HW@armtest2020'
redisDb=0


def init():
    mysql_con = pymysql.connect(
        host=mysqlHost,
        port=mysqlPort,
        user=mysqlUser,
        password=mysqlPassword,
        db=mysqlDb,
        charset=mysqlCharset
    )
    cursor = mysql_con.cursor()
    cursor.execute(
        'SELECT collector_id, device_id, mes_id FROM `mes_collector` where device_id is not null and device_id!="" and mes_id is not null')
    data = cursor.fetchall()

    redis_pool = redis.ConnectionPool(
        host=redisHost,
        port=redisPort,
        password=redisPassword,
        db=redisDb
    ) if redisPassword != "" else redis.ConnectionPool(
        host=redisHost,
        port=redisPort,
        db=redisDb
    )
    redis_con = redis.Redis(connection_pool=redis_pool)

    for i in redis_con.keys():
        print(str(i,encoding='utf-8'))

    redis_con.close()
    redis_pool.disconnect()
    mysql_con.close()


init()