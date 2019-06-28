 
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
from pyecharts.charts import Bar, Line, Grid
import pandas as pd  

app = Flask(__name__, static_folder="templates")

app.config['JSON_AS_ASCII'] = False


def ZQF1(lang) -> Grid:
    print("第一个表格开始处理")
    language = "data/ZQF/"+lang+".xlsx"
    df = pd.read_excel(language)
    df["industry_first"]= df.industry.str.split(' ').str[0].str.split("/").str[0].str.split(",").str[0].str.split("(").str[0].str.split("|").str[0].str.split("丨").str[0]
    df["wage_avg"] = (df.wage_min + df.wage_max)/2
#加wage_avg和industry_first两列

    avg_wage = round(df.wage_avg.mean(),2)
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


from example.commons import Faker
from pyecharts import options as opts
from pyecharts.charts import Bar, Page, Pie, Timeline
from collections import defaultdict

#################################################################################
print("开始处理ZQF第二个表格的数据")
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

################################################################################################
print("开始处理ZQF第三个表格的数据")
for each_table in ['data/ZQF/C#.xlsx','data/ZQF/C++.xlsx','data/ZQF/HTML+CSS.xlsx','data/ZQF/Java.xlsx','data/ZQF/JavaScript.xlsx','data/ZQF/PHP.xlsx','data/ZQF/Python.xlsx','data/ZQF/Ruby.xlsx','data/ZQF/Swift.xlsx','data/ZQF/TypeScript.xlsx']:
    ZQF3_df = pd.read_excel(each_table)
    ZQF3_cities = list(ZQF3_df.groupby("city").wage_avg.mean().keys())
    ZQF3_cities_avg_wage = list(ZQF3_df.groupby("city").wage_avg.mean().round(2))
 
    if not ZQF3_cities:
        ZQF3_cities = list(ZQF3_df.groupby("city").wage_avg.mean().keys())
        ZQF3_cities_avg_wage = list(ZQF3_df.groupby("city").wage_avg.mean().round(2))
    else:
        new_cities_avg_wage = list(ZQF3_df.groupby("city").wage_avg.mean().round(2))
        for i in [0,1,2,3]:
            ZQF3_cities_avg_wage[i] = round((ZQF3_cities_avg_wage[i] + new_cities_avg_wage[i])/2,2)

    
###################################################################################################

def ZQF3():
    print("第三个表格开始处理")
    bar = (
        Bar()
        .add_xaxis(ZQF3_cities)
        .add_yaxis('人均工资', ZQF3_cities_avg_wage, category_gap="60%")
        .set_global_opts(title_opts={"text": "C#", "subtext": "工资与城市分布关系图"})
       .set_series_opts(label_opts=opts.LabelOpts(is_show=False),
                        markline_opts=opts.MarkLineOpts(
                                data=[opts.MarkLineItem(y=max(ZQF3_cities_avg_wage), name="yAxis=50")]
                                ),
                        )
                        )
        
    bar.render_notebook()
    return bar


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
    c = ZQF3()
    return c.dump_options()


if __name__ == "__main__":
    app.run()

