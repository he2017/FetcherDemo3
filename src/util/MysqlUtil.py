# -*- coding: utf-8 -*-
# 第一行加这个后，就可以加中文注释了
'''
Created on 2017年5月21日

@author: tony
'''

import pymysql

'''
创建数据库链接
'''
def getConn():
    conn = None
    try:
        conn = pymysql.connect(host='localhost', #数据库地址 
                               user='root', #数据库账户名称
                               passwd='123456', #账户密码
                               db='fetcher_data',  #数据库名称
                               port=3306, #端口
                               charset="utf8") #编码方式
    except pymysql.Error as e: #将数据库处理异常信息打印到控制台方便调试
        print ("Mysql getConn Error %d: %s" % (e.args[0], e.args[1]))
    finally:
        return conn


'''
关闭链接资源
'''
def closeConn(conn, cur):
    try:
        if cur:
            cur.close()
        if conn:
            conn.close()
    except pymysql.Error as e: #将数据库处理异常信息打印到控制台方便调试
        print ("Close mysql conn or cur Error %d: %s" % (e.args[0], e.args[1]))


'''
测试插入数据
'''
def saveHtml(urlSum, url, html):
    html=html.decode('utf-8')#
    try:
        conn = getConn() #获取数据库连接
        cur = conn.cursor() #打开游标
        cur.execute('SET NAMES utf8mb4')#设置编码
        cur.execute("SET CHARACTER SET utf8mb4")#设置编码
        sql = "insert into html_data (url_sum, url, html) values('%s', '%s', '%s')"%(urlSum, url, pymysql.escape_string(html))
        cur.execute(sql)
        conn.commit() #提交事务，注意少了这一步插入数据将会失败
        closeConn(conn, cur) #关闭资源
        return True
    except pymysql.Error as e:
        print ("Mysql saveHtml Error %d: %s" % (e.args[0], e.args[1]))
    return False

'''
获取网页快照
'''
def getHtml(urlSum):
    html = None
    try:
        conn = getConn()
        if conn == None:
            return ""
        cur = conn.cursor()
        cur.execute("select html from html_data where url_sum='%s'"%urlSum) 
        results = cur.fetchmany(1)
        closeConn(conn, cur) #关闭资源
        if(results and len(results) == 1):
            html = results[0][0]
    except pymysql.Error as e:
        print ("Mysql getHtml Error %d: %s" % (e.args[0], e.args[1]))
    return html

'''
将新闻的meta数据插入到数据库中
'''
def saveNewsMeta(url, urlSum, title):
    try:
        conn = getConn() #获取数据库连接
        cur = conn.cursor() #打开游标
        sql = "insert into news_meta (url, url_sum, title) values('%s', '%s', '%s')"%(url, urlSum, title)
        cur.execute(sql)
        conn.commit() #提交事务，注意少了这一步插入数据将会失败
        closeConn(conn, cur) #关闭资源
        return True
    except pymysql.Error as e:
        print ("Mysql saveNewsMeta error %d: %s" % (e.args[0], e.args[1]))
    return False

'''
将新闻的meta数据插入到数据库中
'''
def saveNewsContent(url, urlSum, title, author, pubTime, content):
    try:
        conn = getConn() #获取数据库连接
        cur = conn.cursor() #打开游标
        sql = "insert into news_content (url, url_sum, title, author, pub_time, content) values('%s', '%s', '%s', '%s', '%s', '%s')"%(url, urlSum, title, author, pubTime, pymysql.escape_string(content))
        cur.execute(sql)
        conn.commit() #提交事务，注意少了这一步插入数据将会失败
        closeConn(conn, cur) #关闭资源
        return True
    except pymysql.Error as e:
        print ("Mysql saveNewsContent error %d: %s" % (e.args[0], e.args[1]))
    return False

'''
将新闻的meta数据插入到数据库中
'''
def updateNewsMetaFetchedStatus(urlSum):
    try:
        conn = getConn() #获取数据库连接
        cur = conn.cursor() #打开游标
        sql = "update news_meta set is_fetched=1 where url_sum='%s'"%(urlSum)
        cur.execute(sql)
        conn.commit() #提交事务，注意少了这一步插入数据将会失败
        closeConn(conn, cur) #关闭资源
        return True
    except pymysql.Error as e:
        print ("Mysql saveNewsMeta error %d: %s" % (e.args[0], e.args[1]))
    return False

'''
将新闻的meta数据插入到数据库中
'''
def getNewsMeta():
    newsMeta = []
    try:
        conn = getConn()
        if conn == None:
            return ""
        cur = conn.cursor()
        cur.execute("select * from news_meta where is_fetched=0") 
        results = cur.fetchmany(10)
        closeConn(conn, cur) #关闭资源
        for result in results:
            meta = {}
            meta['id'] = result[0]
            meta['url'] = result[1]
            meta['urlSum'] = result[2]
            meta['title'] = result[3]
            newsMeta.append(meta)
    except pymysql.Error as e:
        print ("Mysql getHtml Error %d: %s" % (e.args[0], e.args[1]))
    return newsMeta