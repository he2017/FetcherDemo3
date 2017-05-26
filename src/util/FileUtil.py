# -*- coding: utf-8 -*-
# 第一行加这个后，就可以加中文注释了
'''
Created on 2017年5月21日

@author: tony
'''
from util import CommonUtil

'''
将文本保存到指定的文件中
'''
def writeLine(fileName, html):
        try:
            fObj = open(fileName, 'w+', encoding=CommonUtil.UTF_8)  
            fObj.write(html)
            fObj.write('\n')
            fObj.close()
            print ('write successfully')
        except IOError as e:
            print ('file write error:', e, 'fileName', fileName, 'html:', html)