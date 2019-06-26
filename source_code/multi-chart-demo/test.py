# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 20:07:13 2019

@author: Administrator
"""

from random import randrange

from flask import Flask, render_template,url_for, request, json,jsonify

from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Grid
import pandas as pd


from example.commons import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar, Grid, Line, Page, Pie


from example.commons import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar, Page, Pie, Timeline
from collections import defaultdict

app = Flask(__name__, static_folder="templates")

app.config['JSON_AS_ASCII'] = False

#不分语言看地域分布与工资的关系
from pyecharts.charts import Bar, Line
import pandas as pd
import glob
#ZQF############################################################################
#cities=[]
#cities_avg_wage = []
#districts = []
#districts_avg_wage = []
#a = []
#
#df = pd.read_excel('data/ZQF/C#.xlsx')
#df["district"] = df.district.str.split('\\xa0').str[0]
#
#if not cities:
#    cities = list(df.groupby("city").wage_avg.mean().keys())
#    cities_avg_wage = list(df.groupby("city").wage_avg.mean().round(2))
#else:
#    new_cities_avg_wage = list(df.groupby("city").wage_avg.mean().round(2))
#    for i in [0,1,2,3]:
#        cities_avg_wage[i] = round((cities_avg_wage[i] + new_cities_avg_wage[i])/2,2)
#    #城市和城市工资图表数据done
#
#   
#for each in list(df.groupby("district").wage_avg.mean().keys()):
#    if each not in districts:
#        districts.append(each)           
#        districts_avg_wage.append(round(df.query("district== '"+each+"'" ).wage_avg.mean(), 2))
#    else:     
#        districts_avg_wage[districts.index(each)] = round((districts_avg_wage[districts.index(each)] + df.query("district== '"+each+"'" ).wage_avg.mean())/2, 2)
#
#        #求各区平均薪资
#b = list(df.groupby(["city","district"]).wage_avg.mean().keys())   
#for each in b:
#    if each not in a:
#        a.append(each) 
#        
#          #建立一个地区和城市的联系表
#city_district_dic = defaultdict(list)
#for i in range(len(a)):
#    city_district_dic[a[i][0]].append(a[i][1])
#print(city_district_dic)
#print(len(city_district_dic))
#
#city_wage_dict={"上海":[],"北京":[],"广州":[],"深圳":[]}
#d = dict(zip(districts,districts_avg_wage))
#for each in city_district_dic:
#    for i in city_district_dic[each]: 
#        city_wage_dict[each].append(d[i])
#print(city_wage_dict)
##城市和工资联系表
#
#print(cities)
#print(cities_avg_wage)
#print(districts)
#print(districts_avg_wage)
#        
##ZQF############################################################################
#
#def bar_base(lang) -> Timeline:  
#   
#    tl = Timeline()
#
#    bar = (
#        Bar()
#        .add_xaxis(city_district_dic["北京"])
#        .add_yaxis("各区工资", city_wage_dict["北京"])
#        .set_global_opts(title_opts=opts.TitleOpts("{}{}各区工资".format(lang,i)))
#    )
#  
#    
#    bar2 = (
#    Bar()
#    .add_xaxis(cities)
#    .add_yaxis('人均工资', cities_avg_wage)
#
#    .set_global_opts(title_opts={"text": "C#", "subtext": "工资与城市分布关系图"})
#    )
#        
#    bar2.render_notebook()
#    tl.add(bar2, "bar2")
#    tl.add(bar, "{}".format(i))
#
#    return tl

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/barChart",methods=[ 'POST'])
def get_bar_chart():
    if request.method == "POST":
        lang = request.form.get('lang', '')
    print(lang)
    c = bar_base(lang)
    return c.dump_options()


if __name__ == "__main__":
    app.run()
    
   