# -*- coding: utf-8 -*-
"""
Created on Fri May 31 12:10:31 2019

@author: Nicole
"""

import requests
import time
import json,xlwt
from xlrd import open_workbook
from xlutils.copy import copy


def get_json(url,page):
    url_start = "https://www.lagou.com/jobs/list_swift?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput="
    url_parse = "https://www.lagou.com/jobs/positionAjax.json?city=深圳&needAddtionalResult=false"
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?city=%E6%88%90%E9%83%BD&cl=false&fromSearch=true&labelWords=&suginput=',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
    }
    #for x in range(1, 30):
    data = {
            'first': 'true',
            'pn': page,#str(x),
            'kd': 'swift'
                }
    s = requests.Session()
    info_list = []
    s.get(url_start, headers=headers, timeout=3)  # 请求首页获取cookies
    cookie = s.cookies  # 为此次获取的cookies
    response = s.post(url_parse, data=data, headers=headers, cookies=cookie, timeout=3)  # 获取此次文本
    time.sleep(5)
    response.encoding = response.apparent_encoding
    text = json.loads(response.text)
    info = text["content"]["positionResult"]["result"]
    for i in info:
            job_info = [] 
            job_info.append(i["companyFullName"])
            job_info.append(i["city"])
            job_info.append(i["district"])
            job_info.append(i["positionName"])
            job_info.append(i["salary"])
            job_info.append(i["companySize"])
            job_info.append(i["createTime"])
            job_info.append(i["positionAdvantage"])
            info_list.append(job_info) 
    return info_list

            
def main():    
   url="https://www.lagou.com/jobs/positionAjax.json?city=深圳&needAddtionalResult=false"
   page=1    
   info_result=[]    
   title = ['公司全名',"城市","区域", '职位名称', '薪资水平', '公司规模',  "发布时间",  "福利" ]    
   info_result.append(title)    
   while page < 31:        
      job_info=get_json(url,page)        
      info_result=info_result+job_info        
      page+=1
      r_xls = open_workbook("LaGou_Jobs.xls") # 读取excel文件
      row = r_xls.sheets()[0].nrows # 获取已有的行
      excel = copy(r_xls) #将xlrd的对象转化为xlwt的对象
      table = excel.get_sheet(0) # 获取要操作的sheet
      #对excel表追加一行内容
      workbook = xlwt.Workbook(encoding="utf-8")  
      table = workbook.add_sheet('JavaScript', cell_overwrite_ok=True)
      for i, row in enumerate(info_result):                           
          for j, col in enumerate(row):                
             table.write(i, j, col)
      workbook.save('swiftSZ.xls')   

if __name__ == '__main__':
	main()
 

 


        
