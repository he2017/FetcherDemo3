# -*- coding: UTF-8 -*-
# 第一行加这个后，就可以加中文注释了
'''
Created on 2017年5月21日

@author: tony
'''
from util import CommonUtil, MysqlUtil, FetcherUtil

if __name__ == '__main__':
    #1. 第一步一个url变量
    url = 'https://www.douban.com/'
    urlSum = CommonUtil.getUrlSum(url)#将url转成固定长度的md5字符串
    #2. 第二步从数据库中获取快照
    html = MysqlUtil.getHtml(urlSum)
    if not html:
        #3. 第三步数据库中不存在则从网上实时抓取
        html = FetcherUtil.fetchHtml(url) 
        #4. 将网页内容存储到DB
        result = MysqlUtil.saveHtml(urlSum, url, html)
        if result:
            print ('保存网页成功')
        else:
            print ('保存网页失败')
    if(html):
        print(CommonUtil.toGBK(html))
    