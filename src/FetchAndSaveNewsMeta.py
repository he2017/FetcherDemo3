# -*- coding: utf-8 -*-
# 第一行加这个后，就可以加中文注释了
'''
Created on 2017年5月21日

@author: tony
'''
from util import FetcherUtil, CommonUtil, HtmlExtract, MysqlUtil
    
if __name__ == '__main__':
    #1. 第一步一个url变量
    url = 'https://www.douban.com/'
    #2. 第二步抓取网页内容
    html = FetcherUtil.fetchHtml(url) 
    #3. 第三步提取链接
    news = HtmlExtract.extractDoubanNews(html)
    #4. 第四步输出提取到的链接和标题，并保存到数据库中
    for item in news:
        print ('链接:', item[0], '标题:', item[1])
        urlSum = CommonUtil.getUrlSum(item[0])#将url转成固定长度的md5字符串
        MysqlUtil.saveNewsMeta(item[0], urlSum, item[1])
        