# -*- coding: utf-8 -*-
# 第一行加这个后，就可以加中文注释了
'''
Created on 2017年5月21日

@author: tony
''' 
from html.parser import HTMLParser
from util import CommonUtil
import re

'''    
提取链接，返回一个链接数组
'''
def extractLink(html):
    html = CommonUtil.toUtf8(html)
    reg = r'<a(.*?)href="(.*?)"(.*?)>(.*?)</a>'
    groups = re.findall(reg, html, re.S|re.M)
    links = []
    for group in groups:
        link = group[1] #找到匹配的链接group
        if(link.strip() != ''): #链接不为空的时候再返回
            links.append(link)
    return links

'''
提取豆瓣首页里面的新闻链接地址和标题
'''
def extractDoubanNews(html):
    html = CommonUtil.toUtf8(html)
    reg = r'class="notes">(.*?)</ul>'
    news = re.findall(reg, html, re.S|re.M)
    if(len(news) == 1):
        return extractItems(news[0])
    return None

'''
提取豆瓣首页里面的新闻链接地址和标题
'''
def extractItems(content):
    reg = r'<li>(.*?)</li>'
    linkReg = re.compile(reg)
    linkList = re.findall(linkReg, content)
    news = []
    for link in linkList:
        itemReg = re.compile('<a href="(.*?)">(.*?)</a>')
        match = itemReg.match(link)
        if match:
            item = []
            item.append(match.group(1))
            item.append(match.group(2))
            news.append(item)
    return news 

'''
提取新闻里面的内容
'''
def extractMeta(html):
    meta = {}
    meta['title'] = ''
    meta['author'] = ''
    meta['pubTime'] = ''
    meta['content'] = ''
    
    #1. 提取标题
    titleReg = r'<h1>(.*?)</h1>'
    titles = re.findall(titleReg, html, re.S|re.M)
    if titles:
        meta['title'] = titles[0]
    
    #2. 提取作者
    authorReg = r'class="note-author">(.*?)</a>'
    authors = re.findall(authorReg, html, re.S|re.M)
    if authors:
        meta['author'] = authors[0]
    
    #3. 提取时间
    timeReg = r'class="pub-date">(.*?)</span>'
    times = re.findall(timeReg, html, re.S|re.M)
    if authors:
        meta['pubTime'] = times[0]
        
    #4. 提取内容
    contentReg = r'id="link-report">(.*?)<div class="copyright-claim original">'
    contents = re.findall(contentReg, html, re.S|re.M)
    if contents:
        meta['content'] = strip_tags(contents[0])
    return meta

'''
提取文本
'''
def strip_tags(html): 
    html = html.replace("\\/", "/")
    result = ['']  
    parser = HTMLParser()  
    parser.handle_data = result.append  
    parser.feed(html)  
    parser.close()  
    return ''.join(result).strip() 


'''
提取微博内容
'''
def extractWeiboContent(html):
    weibos = []
    #1. 提取每个微博内容区域正则表达式
    reg = r'<div class=\\"content clearfix\\" node-type=\\"like\\">(.*?)<div node-type=\\"feed_list_repeat\\"'
    itemList = re.findall(reg, html, re.S|re.M|re.U) # 匹配多行
    for item in itemList: #遍历提取到的每个微博区域
        weibo = {}
        #2. 提取微博作者和微博内容
        textReg = r'<p class=\\"comment_txt\\" (.*?) nick-name=\\"(.*?)\\">(.*?)<\\/p>'
        texts = re.findall(textReg, item, re.S|re.M|re.U)
        if texts and len(texts) > 0:
            weibo['author'] = CommonUtil.unicode2chinese(texts[0][1]) #第二个下标是微博作者
            weibo['text'] = CommonUtil.unicode2chinese(strip_tags(texts[0][2])) #第三个下标是微博内容
        #3. 提取微博发布时间
        dateReg = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}'
        dates = re.findall(dateReg, item, re.S|re.M|re.U)
        if dates and len(dates) > 0:
            weibo['pubTime'] = dates[0]
        weibos.append(weibo)
    return weibos
