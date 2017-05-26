# -*- coding: utf-8 -*-
# 第一行加这个后，就可以加中文注释了
'''
Created on 2017年5月21日

@author: tony
'''
from util import FetcherUtil, MysqlUtil

'''
1. 从数据库中获取newsmeta信息
2. 根据newsmeta信息的url抓取对应的网页快照
3. 将对应的网页快照信息存储到mysql中
'''    
if __name__ == '__main__':
    #1. 从数据库中获取newsMeta
    newsMeta = MysqlUtil.getNewsMeta()
    htmls = {}
    for meta in newsMeta:
        print (meta['id'], meta['url'], meta['urlSum'], meta['title'])
        html = FetcherUtil.fetchHtml(meta['url'])
        MysqlUtil.saveHtml(meta['urlSum'], meta['url'], html)
        