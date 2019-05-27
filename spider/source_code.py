# -*- coding: utf-8 -*-
"""
Created on Sat May 25 07:35:04 2019

@author: Administrator
"""

from spider.spider import Spider, MultiThreadedSpider,time,ChromeSpider, Response
import pandas as pd
import re


class jobSpider(MultiThreadedSpider):
     start_urls = ["https://search.51job.com/list/030200,000000,0000,00,9,99,专八,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=", 
             "https://search.51job.com/list/030200,000000,0000,00,9,99,Python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=",
        "https://search.51job.com/list/030200,000000,0000,00,9,99,安卓,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=",
          "https://search.51job.com/list/030200,000000,0000,00,9,99,VB,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare="]
     def on_start(self):
         self.data = []

     def process(self, response):
         for a in response.doc("#resultList > div > p > span > a").items():
             self.crawl(a.attr("href"), self.detail)   #先爬首页里的每个链接
         for a in response.doc("#resultList > div.dw_page > div > div > div > ul > li > a").items():    #再爬每个页面里的每个链接
             self.crawl(a.attr("href"), self.process)
             
     def detail(self, response):
        position = response.doc(" body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > h1").text()
        salary = response.doc("body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > strong").text()
        company = response.doc("body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > p.cname > a.catn").text()
        company_type = response.doc("body > div.tCompanyPage > div.tCompany_center.clearfix > div.tCompany_sidebar > div:nth-child(1) > div.com_tag > p:nth-child(1)").text()
        welfare = response.doc("body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > div > div ").text()
        category = response.doc("body > div.tCompanyPage > div.tCompany_center.clearfix > div.tCompany_main > div:nth-child(1) > div > div.mt10 > p:nth-child(1) > a").text()
        other_info = response.doc("body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > p.msg.ltype").text()
        other_info = other_info.split("|")
        info_len = len(other_info)
        add_info_len = 6 - info_len  
        for i in (0, add_info_len):
            other_info.append("无")          
        self.data.append({"福利": welfare, "职能类别": category,"职位":position, "工资": salary, "公司": company, "公司类型": company_type, "地区":other_info[0],"工龄要求":other_info[1],"学历要求":other_info[2],"招聘人数":other_info[3],"发布日期": other_info[4], "语言要求":other_info[5]})   #保存数据
 
     def on_end(self):
         df = pd.DataFrame.from_dict(self.data)
         df.to_excel("51job.xlsx")          #处理并输出数据
        
jobSpider().start()
