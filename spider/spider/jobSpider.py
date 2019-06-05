# -*- coding: utf-8 -*-
"""
Created on Sat May 25 07:35:04 2019
@author: 张芹妃
"""

from spider import Spider, MultiThreadedSpider,time,ChromeSpider, Response
import pandas as pd

class jobSpider(MultiThreadedSpider):
    
     def on_start(self):
         self.data = []

     def process(self, response):
         for a in response.doc("#resultList > div > p > span > a").items():
                self.crawl(a.attr("href"), self.detail)  
         for a in response.doc("#resultList > div.dw_page > div > div > div > ul > li > a").items():    
             self.crawl(a.attr("href"), self.process)
             
     def detail(self, response):
        position = response.doc(" body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > h1").text()
        salary = response.doc("body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > strong").text()
        company = response.doc("body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > p.cname > a.catn").text()
        company_type = response.doc("body > div.tCompanyPage > div.tCompany_center.clearfix > div.tCompany_sidebar > div:nth-child(1) > div.com_tag > p:nth-child(1)").text()
        welfare = response.doc("body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > div > div ").text()
        category = response.doc("body > div.tCompanyPage > div.tCompany_center.clearfix > div.tCompany_main > div:nth-child(1) > div > div.mt10 > p:nth-child(1) > a").text()
        position_details = response.doc("body > div.tCompanyPage > div.tCompany_center.clearfix > div.tCompany_main > div:nth-child(1) > div > p").text()
        size = response.doc("body > div.tCompanyPage > div.tCompany_center.clearfix > div.tCompany_sidebar > div:nth-child(1) > div.com_tag > p:nth-child(2)").text()
        industry = response.doc("body > div.tCompanyPage > div.tCompany_center.clearfix > div.tCompany_sidebar > div:nth-child(1) > div.com_tag > p:nth-child(3)").text()
        other_info = response.doc("body > div.tCompanyPage > div.tCompany_center.clearfix > div.tHeader.tHjob > div > div.cn > p.msg.ltype").text()
        other_info = other_info.split("|")
        for i in range(0,3):
            other_info.append("无")
        if other_info[0][0:2] in ["北京","上海","广州","深圳"]:
            if position and salary and company:
                self.data.append({"position":position, "company": company,  "location":other_info[0],"diploma_requirement":other_info[2], "wage": salary, "experience":other_info[1], "industry":industry,"welfare": welfare, "description":position_details,"size": size, "company_type": company_type, "category": category,})   #保存数据
 
     def on_end(self, sheetname, result):
         df = pd.DataFrame.from_dict(self.data)
         df.to_excel(result, sheet_name = sheetname, index = False)    
       
 
start_urls = ['https://search.51job.com/list/030200%252C020000%252C010000%252C040000,000000,0000,00,9,99,Python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=', 
              'https://search.51job.com/list/030200%252C020000%252C010000%252C040000,000000,0000,00,9,99,JavaScript,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=', 
              'https://search.51job.com/list/030200%252C020000%252C010000%252C040000,000000,0000,00,9,99,Java,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=', 
              'https://search.51job.com/list/030200%252C020000%252C010000%252C040000,000000,0000,00,9,99,PHP,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=', 
              'https://search.51job.com/list/030200%252C020000%252C010000%252C040000,000000,0000,00,9,99,Swift,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
              'https://search.51job.com/list/030200%252C020000%252C010000%252C040000,000000,0000,00,9,99,Ruby,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=', 
              'https://search.51job.com/list/030200%252C020000%252C010000%252C040000,000000,0000,00,9,99,TypeScript,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=', 
              'https://search.51job.com/list/030200%252C020000%252C010000%252C040000,000000,0000,00,9,99,C++,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=', 
              'https://search.51job.com/list/030200%252C020000%252C010000%252C040000,000000,0000,00,9,99,C%2523,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=', 
              'https://search.51job.com/list/030200%252C020000%252C010000%252C040000,000000,0000,00,9,99,HTML+CSS,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=', 
             ]
     
sheetname = ["Python","JavaScript","Java","PHP","Swift","Ruby","TypeScript","C++","C#","HTML+CSS"]

result= pd.ExcelWriter("51job.xlsx")
 
for i in range(0, 10):
    print(start_urls[i], sheetname[i])
    jobSpider().start(start_urls[i], sheetname[i],result)
 
result.save()
         
 