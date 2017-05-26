# -*- coding: GB18030 -*-
# 第一行加这个后，就可以加中文注释了
'''
Created on 2017年5月21日

@author: tony
'''
from util import CommonUtil, FileUtil, FetcherUtil, MysqlUtil, HtmlExtract

'''
简单的通过cookie抓取微博搜索结果
'''
if __name__ == '__main__':
    #1. 初始化变量
    url = 'http://s.weibo.com/weibo/%25E4%25BA%25AC%25E4%25B8%259C&b=1&page=1'
    cookie_str = '这里填写自己的微博账号cookie'
    #2. 首先从Mysql中获取快照
    urlSum = CommonUtil.getUrlSum(url)
    html = MysqlUtil.getHtml(urlSum)
    #3. 如果Mysql没有快照，则实时的从网上抓取快照
    if not html:
        html = FetcherUtil.fetchWeibo(url, cookie_str)
        result = MysqlUtil.saveHtml(urlSum, url, html) #抓取王快照后存储本地Mysql中
        if result:
            print ('保存微博快照成功')
        else:
            print ('保存微博快照失败')
    
    FileUtil.writeLine("weibo.html", html) #保存快照到临时文件中
    #4. 从html快照中提取结构化的微博内容
    weiboDatas = HtmlExtract.extractWeiboContent(html) 
    #5. 输入提取到的微博结构化内容
    for weiboData in weiboDatas:
        print ('作者:', weiboData['author'])
        print ('发布时间:', weiboData['pubTime'])
        print ('内容:', weiboData['text'])
        print ('')
    print ('找到', len(weiboDatas), '条微博')
    #6. 存储到Mysql中