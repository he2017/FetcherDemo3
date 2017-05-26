# -*- coding: utf-8 -*-
# 第一行加这个后，就可以加中文注释了
'''
Created on 2017年5月21日

@author: tony
'''
import http.client
import urllib.request
import html.parser

'''
抓取网页
'''
def fetchHtml(url):
    page = urllib.request.urlopen(url) #打开一个链接
    html = page.read() #读取数据
    return html #返回html内容

'''
抓取微博
'''
def fetchWeibo(url, cookie=''):
    ret = html.parser.urlparse(url)    # Parse input URL
    conn = http.client.HTTPConnection(ret.netloc)
    conn.request(method='GET', url=url , headers={'Cookie': cookie})
    return conn.getresponse().read()
