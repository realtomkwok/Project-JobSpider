from spider.spider import Spider, MultiThreadedSpider,time,ChromeSpider, Response
import pandas as pd
import re


class jobSpider(MultiThreadedSpider):
     start_urls = ["https://www.liepin.com/zhaopin/?init=-1&headckid=04237a5e368b395d&flushckid=1&fromSearchBtn=2&dqs=010&sfrom=click-pc_homepage-centre_searchbox-search_new&ckid=04237a5e368b395d&key=python&siTag=I-7rQ0e90mv8a37po7dV3Q~fA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_fp&d_ckId=e58253142065531476b3a39fc2dea5e5&d_curPage=0&d_pageSize=40&d_headId=e58253142065531476b3a39fc2dea5e5"]
     def on_start(self):
         self.data = []

     def process(self, response):
         for a in response.doc("#sojob > div:nth-child(7) > div > div.job-content > div > ul > li > div > div.job-info > h3 > a").items():
             print(a.text(), a.attr("href"))
            #  self.crawl(a.attr("href"), self.detail)   #先爬首页里的每个链接
        #  for a in response.doc("#sojob > div:nth-child(7) > div > div.job-content > div:nth-child(1) > div > div > a").items():    #再爬每个页面里的每个链接
        #      self.crawl(a.attr("href"), self.process)
             
     def detail(self,response):
         position = response.doc("#job-view-enterprise > div.wrap.clearfix > div.clearfix > div.main > div.about-position > div.title-info > h1").text()
         salary = response.doc("#job-view-enterprise > div.wrap.clearfix > div.clearfix > div.main > div.about-position > div:nth-child(2) > div.clearfix > div.job-title-left > p.job-item-title").text()
         company = response.doc("#job-view-enterprise > div.wrap.clearfix > div.clearfix > div.main > div.about-position > div.title-info > h3 > a").text()
         location = response.doc("#job-view-enterprise > div.wrap.clearfix > div.clearfix > div.main > div.about-position > div:nth-child(2) > div.clearfix > div.job-title-left > p.basic-infor > span > a").text()
         area = response.doc("#job-view-enterprise > div.wrap.clearfix > div.clearfix > div.side > div:nth-child(2) > div.right-post-top > div.company-infor > div > ul.new-compintro > li:nth-child(1) > a").text()
         level = response.doc("#job-view-enterprise > div.wrap.clearfix > div.clearfix > div.main > div.about-position > div:nth-child(2) > div.clearfix > div.job-title-left > div > span:nth-child(1)").text()
         experience = response.doc("#job-view-enterprise > div.wrap.clearfix > div.clearfix > div.main > div.about-position > div:nth-child(2) > div.clearfix > div.job-title-left > div > span:nth-child(2)").text()
         language = response.doc("#job-view-enterprise > div.wrap.clearfix > div.clearfix > div.main > div.about-position > div:nth-child(2) > div.clearfix > div.job-title-left > div > span:nth-child(3)").text()
         age = response.doc("#job-view-enterprise > div.wrap.clearfix > div.clearfix > div.main > div.about-position > div:nth-child(2) > div.clearfix > div.job-title-left > div > span:nth-child(4)").text()
         self.data.append({"职位":position,"薪酬":salary,"公司":company,"地点":location,"公司领域":area,"学历":level,"工作经验":experience,"语言要求":language,"年龄":age})
     def on_end(self):
        print(self.data)
        df = pd.DataFrame.from_dict(self.data)
        df.to_excel("data.xlsx")
         
    
         
#         position = response.doc("body > div.view > div.job-detail > section.base-info > div.flexbox.baseinfo-top > span").text()
#         salary = response.doc("body > div.view > div.job-detail > section.base-info > div.flexbox.baseinfo-top > p").text()
#         company = response.doc("body > div.view > div.job-detail > section.company-info > div.job-parent.clearfix > div > h2").text()
#         location = response.doc("body > div.view > div.job-detail > section.base-info > div.job-conditon > p:nth-child(1) > a").text()
#         area = response.doc("body > div.view > div.job-detail > section.company-info > div.job-parent.clearfix > div > p > a").text()
#         self.data.append({"职位":position,"薪酬":salary,"公司":company,"地点":location,"公司领域":area})
    
        
        
jobSpider().start()
