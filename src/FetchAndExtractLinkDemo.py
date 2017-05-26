# -*- coding: utf-8 -*-
# 第一行加这个后，就可以加中文注释了
'''
Created on 2017年5月21日

@author: tony
'''
from util import FetcherUtil, HtmlExtract
    
if __name__ == '__main__':
    #1. 第一步一个url变量
    url = 'https://www.douban.com/'
    #2. 第二步抓取网页内容
    html = FetcherUtil.fetchHtml(url) 
    #3. 第三步提取链接
    links = HtmlExtract.extractLink(html)
    #4. 第四不输出提取到的链接到控制台
    if links:
        for link in links:
            print (link)
