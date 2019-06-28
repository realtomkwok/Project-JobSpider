# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 20:03:18 2019

@author: Administrator
"""

from flask import Flask
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig

# 关于 CurrentConfig，可参考 [基本使用-全局变量]
CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates"))

from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Grid
import pandas as pd


for each_table in ['data/C#.xlsx','data/C++.xlsx','data/HTML+CSS.xlsx','data/Java.xlsx','data/JavaScript.xlsx','data/PHP.xlsx','data/Python.xlsx','data/Ruby.xlsx','data/Swift.xlsx','data/TypeScript.xlsx']:
    df = pd.read_excel(each_table)
    df["industry_first"]= df.industry.str.split(' ').str[0].str.split("/").str[0].str.split(",").str[0].str.split("(").str[0].str.split("|").str[0].str.split("丨").str[0]
    df["wage_avg"] = (df.wage_min + df.wage_max)/2
    df.to_excel(each_table)
#加wage_avg和industry_first两列

    avg_wage = round(df.wage_avg.mean(),2)
    count =  df.groupby("industry_first").industry_first.count().sort_values(ascending=False)
    industries = list(count.keys()[0:20])
    count = list(count[0:20])
    salaries = []
    data = []

    for each in industries:
        data.append({"行业":each,"平均工资":round(df.query("industry_first == '"+ each +"'" ).wage_avg.mean(), 2)})
        salaries.append(round(df.query("industry_first == '"+ each +"'" ).wage_avg.mean(), 2))

    print(each_table)
    print(industries)
    print(count )
    print(salaries)
    print(avg_wage)
    print('*'*50)

app = Flask(__name__, static_folder="templates")


def bar_base() -> Bar:
    c = (
        Bar()
        .add_xaxis(industries)
        .add_yaxis('工资', salaries)
        .set_global_opts(title_opts={"text": "C#", "subtext": "工资与行业关系图"})
)
    return c


@app.route("/")
def index():
    c = bar_base()
    return Markup(c.render_embed())


if __name__ == "__main__":
    app.run()