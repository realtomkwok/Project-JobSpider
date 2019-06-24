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


def bar_base(lang) -> Bar:
    language = "data/ZQF/"+lang+".xlsx"
    df = pd.read_excel(language)
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
    
    c = (
        Bar()
        .add_xaxis(industries)
        .add_yaxis('工资', salaries)
        .set_global_opts(title_opts={"text": lang, "subtext": "工资与行业关系图"})
)
    print("*"*50)
    return c


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
