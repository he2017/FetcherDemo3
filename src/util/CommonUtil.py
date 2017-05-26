# -*- coding: utf-8 -*-
# 第一行加这个后，就可以加中文注释了
'''
Created on 2017年5月21日

@author: tony
'''
import hashlib

UTF_8 = "UTF-8"
GB18030 = "GB18030"
GBK = "GBK"
UNICODE_ESCAPE = "unicode_escape"

'''
将url链接转换成md5加密的32位唯一字符串
'''
def getUrlSum(url):
    urlSum = None
    if url:
        url_md5 = hashlib.md5()
        url_md5.update(url.encode(UTF_8))   
        urlSum = url_md5.hexdigest()   
    return urlSum

def toGBK(html):
    if(html):
        return html.encode(GBK, "ignore").decode(GBK)
    else:
        return html

def toUtf8(html):
    if(html):
        return html.decode(UTF_8)
    else:
        return html

def unicode2chinese(html):
    if(html):
        return html.encode(UTF_8).decode(UNICODE_ESCAPE)
    else:
        return html
