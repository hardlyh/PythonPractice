# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import requests
from bs4 import BeautifulSoup
import sys

class Tool:
    #去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    #删除超链接标签
    removeAddrs = re.compile('<div.*?>|</div>')
    removeAddr = re.compile('<a.*?>|</a>')
    #把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    #将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    #把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    #将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br/>')
    #将其余标签剔除
    removeExtraTag = re.compile('<.*?>')
    def replace(self,x):
        x = re.sub(self.removeAddrs,"",x)
        x = re.sub(self.removeImg,"",x)
        x = re.sub(self.removeAddr,"",x)
        x = re.sub(self.replaceLine,"\n",x)
        x = re.sub(self.replaceTD,"\t",x)
        x = re.sub(self.replacePara,"\n    ",x)
        x = re.sub(self.replaceBR,"\n",x)
        x = re.sub(self.removeExtraTag,"",x)
        #strip()将前后多余内容删除
        return x

class BDTB():
    """docstring for BDTB"""
    def __init__(self, baseURL,seeLZ):
        self.baseURL=baseURL;
        self.seeLZ='?see_lz='+str(seeLZ)
        self.tool=Tool()

    def getpage(self,pageNum):
        try:
            url=self.baseURL+self.seeLZ+'&pn='+str(pageNum)
            request=urllib2.Request(url)
            response=urllib2.urlopen(request)
           # print response.read()
            return response
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print u'百度贴吧连接失败,错误原因',e.reason
                return None

    def gettitle(self):
        page=requests.get(self.baseURL+self.seeLZ).content.decode('utf-8')  
        soup=BeautifulSoup(page,"html5lib")
        #pattern=re.compile('<h3 class="core_title_txt pull-left text-overflown.*?>(.*?)</h3>',re.S)
        #title=soup.find("div",class_="core_title_wrap_bright clearfix")
        #title=soup.find("li",class_="l_reply_num")
        title=soup.find_all("div",class_="d_post_content j_d_post_content ")
        for item in title:
            print self.tool.replace(item.encode("utf-8"))
 



baseURL='http://tieba.baidu.com/p/3138733512'
bdtb=BDTB(baseURL,1)
bdtb.gettitle()


