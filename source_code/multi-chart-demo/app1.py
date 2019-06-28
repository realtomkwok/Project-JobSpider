 
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 14:46:54 2019

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 20:07:13 2019

@author: Administrator
"""

from random import randrange
from flask import Flask, render_template,url_for, request, json,jsonify
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Grid,Timeline,Page
import pandas as pd  
from collections import defaultdict

app = Flask(__name__, static_folder="templates")

app.config['JSON_AS_ASCII'] = False


def ZQF1(lang) -> Grid:
    print("第一个表格开始处理")
    language = "data/ZQF/"+lang+".xlsx"
    df = pd.read_excel(language)
    df["industry_first"]= df.industry.str.split(' ').str[0].str.split("/").str[0].str.split(",").str[0].str.split("(").str[0].str.split("|").str[0].str.split("丨").str[0]
    df["wage_avg"] = (df.wage_min + df.wage_max)/2
#加wage_avg和industry_first两列
    count =  df.groupby("industry_first").industry_first.count().sort_values(ascending=False)
    industries = list(count.keys()[0:20])   #前二十个热门行业
    count = list(count[0:20])          #前二十个热门行业的岗位
    salaries = []                      #平均工资
    data = []

    for each in industries:
        data.append({"行业":each,"平均工资":round(df.query("industry_first == '"+ each +"'" ).wage_avg.mean(), 2)})
        salaries.append(round(df.query("industry_first == '"+ each +"'" ).wage_avg.mean(), 2))

    bar = (
        Bar()
        .add_xaxis(industries)
        .add_yaxis(
            "岗位数量",
           count,
            yaxis_index=1,
            color="#d14a61",
        )

        .extend_axis(
            yaxis=opts.AxisOpts(
                name="岗位数量（个）",
                type_="value",
                min_=0,
                max_=2200,
                position="right",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#d14a61")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
            )
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value",
                name="平均工资（千/月）",
                min_=0,
                max_=35,
                position="left",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#675bba")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} "),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            )
        )
        .set_global_opts(
            
            title_opts=opts.TitleOpts(title=lang + "行业工资关系图"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            toolbox_opts = opts.ToolboxOpts(is_show=True)
            
        )
    )

    line = (
        Line()
        .add_xaxis(industries)
        .add_yaxis(
            "平均工资",
            salaries,
            yaxis_index=2,
            color="#675bba",
            label_opts=opts.LabelOpts(is_show=False),
        )
    )

    bar.overlap(line)
    return Grid().add(bar, opts.GridOpts(pos_left="5%", pos_right="20%"), is_control_axis_index=True)


#################################################################################
print("开始处理ZQF第二个表格的数据")
print("请稍等......")
ZQF2_languages = ["C#", "C++","HTML+CSS","Java","JavaScript","PHP","Python","Ruby","Swift","TypeScript","",]
ZQF2_city_salary_dict = {"北京":[],"广州":[],"深圳":[],"上海":[],}

for each_table in ['data/ZQF/C#.xlsx','data/ZQF/C++.xlsx','data/ZQF/HTML+CSS.xlsx','data/ZQF/Java.xlsx','data/ZQF/JavaScript.xlsx','data/ZQF/PHP.xlsx','data/ZQF/Python.xlsx','data/ZQF/Ruby.xlsx','data/ZQF/Swift.xlsx','data/ZQF/TypeScript.xlsx']:
    ZQF2_df = pd.read_excel(each_table)
    ZQF2_cities = list(ZQF2_df.groupby("city").wage_avg.mean().keys())
    ZQF2_cities_avg_wage = list(ZQF2_df.groupby("city").wage_avg.mean().round(2))
    
    for i in [0,1,2,3]:
        ZQF2_city_salary_dict[ZQF2_cities[i]].append(ZQF2_cities_avg_wage[i])

###################################################################

def ZQF2() -> Timeline:
    print("第二个表格开始处理")    
    tl = Timeline()
    for i in ZQF2_cities:
        bar = (
            Bar()
            .add_xaxis(ZQF2_languages)
            .add_yaxis("{}平均工资".format(i), ZQF2_city_salary_dict[i],  yaxis_index=1)
            .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value",
                name="平均工资（千/月）",
                min_=0,
                max_=30,
                position="left",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#675bba")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value} "),
                splitline_opts=opts.SplitLineOpts(
                    is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
                ),
            )
        )
            .set_global_opts(title_opts=opts.TitleOpts("{}各语言平均工资".format(i)),
            )
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值"),
       
                ]
            ),
        )
        )
        tl.add(bar, "{}".format(i))
    return tl


#ZQF############################################################################
print("开始处理ZQF第三个表格的数据")
print("请稍等......")
cities=[]
cities_avg_wage = []
districts = []
districts_avg_wage = []
a = []

for each_table in ['data/ZQF/C#.xlsx','data/ZQF/C++.xlsx','data/ZQF/HTML+CSS.xlsx','data/ZQF/Java.xlsx','data/ZQF/JavaScript.xlsx','data/ZQF/PHP.xlsx','data/ZQF/Python.xlsx','data/ZQF/Ruby.xlsx','data/ZQF/Swift.xlsx','data/ZQF/TypeScript.xlsx']:
    df = pd.read_excel(each_table)
    df["district"] = df.district.str.split('\\xa0').str[0]

    if not cities:
        cities = list(df.groupby("city").wage_avg.mean().keys())
   
    for each in list(df.groupby("district").wage_avg.mean().keys()):
        if each not in districts:
            districts.append(each)           
            districts_avg_wage.append(round(df.query("district== '"+each+"'" ).wage_avg.mean(), 2))
        else:     
            districts_avg_wage[districts.index(each)] = round((districts_avg_wage[districts.index(each)] + df.query("district== '"+each+"'" ).wage_avg.mean())/2, 2)

            #求各区平均薪资
    b = list(df.groupby(["city","district"]).wage_avg.mean().keys())   
    for each in b:
        if each not in a:
            a.append(each) 
        
          #建立一个城市区域的联系表
city_district_dic = defaultdict(list)
for i in range(len(a)):
    city_district_dic[a[i][0]].append(a[i][1])

a = []
city_wage_dict={"上海":[],"北京":[],"广州":[],"深圳":[]}
d = dict(zip(districts,districts_avg_wage))
for each in city_district_dic:
    for i in city_district_dic[each]: 
        city_wage_dict[each].append(d[i])

#print(city_wage_dict)
#print(city_district_dic)   
#城市和工资联系表

#ZQF############################################################################
def ZQF3(city) -> Bar:
    c = (
        Bar()
        .add_xaxis(city_district_dic[city])
        .add_yaxis('平均工资',city_wage_dict[city])
        .set_global_opts(title_opts=opts.TitleOpts(title= city+"各区各编程语言工资", subtitle=""))
        .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markline_opts=opts.MarkLineOpts(
                data=[
                    opts.MarkLineItem(type_="min", name="最小值"),
                    opts.MarkLineItem(type_="max", name="最大值"),
                ]
            ),
        )
    )
    return c

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ZQF1",methods=[ 'POST'])
def get_ZQF1():
    if request.method == "POST":
        lang = request.form.get('lang', '')
    print(lang)
    c = ZQF1(lang)
    return c.dump_options()

@app.route("/ZQF2",methods=[ 'POST'])
def get_ZQF2():
    c = ZQF2()
    return c.dump_options()

@app.route("/ZQF3",methods=[ 'POST'])
def get_ZQF3():
    if request.method == "POST":
        city = request.form.get('city', '')
    print(city)
    c = ZQF3(city)
    return c.dump_options()


if __name__ == "__main__":
    app.run()

