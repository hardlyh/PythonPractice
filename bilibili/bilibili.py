#!/usr/bin/env python
# -*- coding: utf-8 -*-


from selenium import webdriver
import  urllib,queue
from bs4 import BeautifulSoup
import re

class Record:

	def __init__(self):
		self.title="" #标题
		self.url="" #url
		self.name="" #up主名字

	def writeToFile(self,f):
		row='"{0}","{1}","{2}"'.format(self.title,self.name,self.url.replace('"',"'"))+'\n'
		f.write(row)
	def toString(self):
		return '"{0}","{1}","{2}"'.format(self.title,self.url,self.name)




class bilibili:
	urlTemplate="http://search.bilibili.com/all?keyword=%E4%BB%A5%E6%92%92&page={0}&order=totalrank"
	resultQueue=queue.Queue()
	keyWords="bilibili"
	totalNum=0  #数量
	name="";       #up主

	def __init__(self,words,name):
		self.keyWords=words
		self.name=name
		pass

	def __del__(self):

		pass

	def makeUrl(self,pageNum):
		return self.urlTemplate.format(pageNum)

	def init(self):
		r2=Record()
		r2.name="up主名字"
		r2.title="主题"
		r2.url="链接"
		self.resultQueue.put(r2)

		pass


	def writeResult(self):
		f=open(self.keyWords+".csv","w")
		while(self.resultQueue.empty()==False):
			self.resultQueue.get().writeToFile(f)
			print("input success")
		f.close()
		pass



	def getContent(self,url):

		print("即将爬取:",url)

		html=urllib.request.urlopen(url).read()
		soup=BeautifulSoup(html,"html5lib")

		ul=soup.find("ul",class_="ajax-render")

		for li in ul.find_all("li"):
			try:
				span=li.find("span",title="up主")
				up_name=span.find("a").get_text().strip()
				if(up_name==self.name):
					obj=Record()
					a=li.find("div",class_="headline ").find("a")
					obj.url=a['href']
					obj.title=a['title']
					obj.name=self.name
					self.resultQueue.put(obj)
					self.totalNum+=1
				else:
					print("up主为  "+up_name,"  不符合要求")
			except Exception as ex:
				print("出现错误,错误信息为 ",ex)

	def getAll(self,pageNum):

		self.init()
		for i in range(1,pageNum+1):
			try:
				self.getContent(self.makeUrl(i))
			except Exception as ex:
				print("出现错误",ex)

		self.writeResult()
		print("内容为",self.keyWords,"up主为",self.name,"的视频共有",self.totalNum)


if __name__ == '__main__':
	bi=bilibili("以撒","少年Pi")
	bi.getAll(10)