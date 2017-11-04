# -*- coding:utf-8 -*-

import requests
import urllib2
import re
import urllib
import cookielib
from bs4 import BeautifulSoup
import sys
import socket 
import time



def getVIEW(Page):          # Get viewststes for login page
	view = r'name="__VIEWSTATE" value="(.+)" '
	view = re.compile(view)
	return view.findall(Page)[0]

CaptchaUrl = "http://211.64.32.90/CheckCode.aspx"
PostUrl = "http://211.64.32.90/default2.aspx"
cookie=cookielib.CookieJar()
handler=urllib2.HTTPCookieProcessor(cookie)
opener=urllib2.build_opener(handler)

username="201401009053"
pwd="19960215"
picture=opener.open(CaptchaUrl).read()
local=open("e:/image.jpg",'wb')
local.write(picture)
local.close()

code=raw_input("input ：")
Data={
	'__VIEWSTATE':'dDwtMTg3MTM5OTI5MTs7Pv2bFHphUolg1EYGNu2ag/mHYBwg',
	'TextBox1':username,	
	'TextBox2':pwd,
	'TextBox3':code,
	'RadioButtonList1':'',
	'Button1':'',
	'lbLanguage':''
}

headers={
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36',
	'Referer':'http://211.64.32.90/default2.aspx',
	'Connection':'keep-alive',
	'Content-Type':'application/x-www-form-urlencoded'

}

data=urllib.urlencode(Data)
req=urllib2.Request(PostUrl,data,headers)
response=opener.open(req)


head={
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, sdch',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'Connection':'keep-alive',
	'Host':'211.64.32.90',
	'Referer':'http://211.64.32.90/xs_main.aspx?xh=201401009053',
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'

}

getdata=urllib.urlencode({
	'xh':'201401009053',
	'xm':'李昱慧',
	'gnmkdm':'N121619'
	})


Request=urllib2.Request('http://211.64.32.90/xscjcx_dq.aspx?'+getdata,None,head)
response=opener.open(Request)



getdata2=urllib.urlencode({
	'__EVENTTARGET':'ddlxn',
	'__EVENTARGUMENT':'',
	'__VIEWSTATE':getVIEW(response.read()),
	'ddlxn':'2015-2016',
	'ddlxq':'1',

	})

head={
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'Cache-Control':'max-age=0',
	'Connection':'keep-alive',
	'Content-Length':'1489',
	'Content-Type':'application/x-www-form-urlencoded',
	'Host':'211.64.32.90',
	'Origin':'http://211.64.32.90',
	'Referer':'http://211.64.32.90/xscjcx_dq.aspx?'+getdata,
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36',
	}

request=urllib2.Request('http://211.64.32.90/xscjcx_dq.aspx?'+getdata,getdata2,head)
response=opener.open(request)
print response.read()




