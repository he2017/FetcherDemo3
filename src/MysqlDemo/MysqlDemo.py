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
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
    finally:
        return conn

'''
测试从Mysql查询数据
1. 首先需要安装Mysql
2. 创建数据库和表接口，参考fetcher_data.sql文件
'''
def testSelectData():
    data = [] #返回数组形式结果集
    try:
        conn = getConn()
        if conn == None:
            return data
        cur = conn.cursor()
        cur.execute('select * from mysql_demo') #测试一个最简单的Sql查询语句
        results = cur.fetchmany(10) #每次最多查询10条记录
        for r in results:
            record = {} #每个record存储为一个map结构形式
            record['id'] = r[0] #获取ID
            record['url'] = r[1] #获取连接
            record['title'] = r[2] #获取标题
            data.append(record)
        cur.close() #关闭游标
        conn.close() #关闭链接
    except pymysql.Error as e: #将数据库处理异常信息打印到控制台方便调试
        print ("Mysql Error %d: %s" % (e.args[0], e.args[1]))
    finally:
        return data  #最后返回一个record数组
    
'''
测试插入数据
'''
def testInsertData(data):
    try:
        conn = getConn() #获取数据库连接
        cur = conn.cursor() #打开游标
        for item in data: #循环插入数据
            sql = "insert into mysql_demo (url, title) values('%s', '%s')"%(item[0],item[1])
            cur.execute(sql)
        conn.commit() #提交事务，注意少了这一步插入数据将会失败
        cur.close() #关闭游标
        conn.close() #关闭连接
    except pymysql.Error as e:
        conn.rollback()
        print ("Mysql Error %d: %s" % (e.args[0], e.args[1]))
    
'''
输出打印数据库record信息
'''
def displayData(data):
    for record in data:
        print ('ID:', record['id'], '链接:', record['url'], '标题:', record['title'])
    print ('查询到%s条记录'%(len(data)))

def getInitData():
    data = []
    record = []
    record.append('http://www.baidu.com')
    record.append('百度首页')
    data.append(record)
    return data


'''
入口函数
'''
if __name__ == '__main__':
    data = getInitData()
    testInsertData(data)
    data = testSelectData()
    displayData(data)