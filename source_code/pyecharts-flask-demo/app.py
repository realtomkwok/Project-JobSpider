# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 20:07:13 2019

@author: Administrator
"""

from random import randrange

from flask import Flask, render_template

from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Grid
import pandas as pd


app = Flask(__name__, static_folder="templates")


def bar_base() -> Bar:
    language = "data/ZQF/C#.xlsx"
    df = pd.read_excel(language)
    df["industry_first"]= df.industry.str.split(' ').str[0].str.split("/").str[0].str.split(",").str[0].str.split("(").str[0].str.split("|").str[0].str.split("丨").str[0]
    df["wage_avg"] = (df.wage_min + df.wage_max)/2
    df.to_excel(language)
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

    print(language)
    print(industries)
    print(count )
    print(salaries)
    print(avg_wage)
    print('*'*50)
    c = (
        Bar()
        .add_xaxis(industries)
        .add_yaxis('工资', salaries)
        .set_global_opts(title_opts={"text": "C#", "subtext": "工资与行业关系图"})
)
    return c

def pie_base(lang) -> Bar:
    language = "data/ZQF/"+ lang+".xlsx"
    df = pd.read_excel(language)
    df["industry_first"]= df.industry.str.split(' ').str[0].str.split("/").str[0].str.split(",").str[0].str.split("(").str[0].str.split("|").str[0].str.split("丨").str[0]
    df["wage_avg"] = (df.wage_min + df.wage_max)/2
    df.to_excel(language)
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

    print(language)
    print(industries)
    print(count )
    print(salaries)
    print(avg_wage)
    print('*'*50)
    c = (
        Bar()
        .add_xaxis(industries)
        .add_yaxis('工资', salaries)
        .set_global_opts(title_opts={"text": "C#", "subtext": "工资与行业关系图"})
)
    return c

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/barChart/<name>", methods=['GET'])
def get_bar_chart(name):
    print("aaaa")
    c = bar_base(name)
    return c.dump_options()

@app.route("/pieChart")
def get_pie_chart():
    d = pie_base()
    return d.dump_options()


if __name__ == "__main__":
    app.run()
