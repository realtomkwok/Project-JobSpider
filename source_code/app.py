# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 20:07:13 2019

@author: Administrator
"""

from random import randrange

from flask import Flask, render_template,url_for, request, json,jsonify

from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Grid,Page, WordCloud
import pandas as pd
from pyecharts.globals import SymbolType

app = Flask(__name__, static_folder="templates")

app.config['JSON_AS_ASCII'] = False


def bar_base(lang) -> Bar:
    language = "data/LZX/"+lang+".xlsx"
    df = pd.read_excel(language)
    if lang == "C++":
        df_alt = df.query("industry in ['计算机软件', '互联网','网络游戏','通信','电子商务','仪器仪表及工业自动化','移动互联网','教育','计算机硬件','金融','计算机服务','文娱']").groupby(['city','industry']).size().reset_index(name="count")
    elif lang == "C##":
        df_alt = df.query("industry in ['计算机软件', '互联网','IT服务','电子技术','仪器仪表及工业自动化','移动互联网','教育','通信','网络游戏','医疗设备','汽车','媒体','金融']").groupby(['city','industry']).size().reset_index(name="count")
    elif lang == "HTML+CSS":
        df_alt = df.query("industry in ['计算机软件', '互联网','电子技术','仪器仪表及工业自动化','移动互联网','教育','通信','网络游戏','电子商务']").groupby(['city','industry']).size().reset_index(name="count")
    elif lang == "Java":
        df_alt = df.query("industry in ['计算机软件', '互联网','电子技术','移动互联网','教育','通信','网络游戏','电子商务','金融','计算机服务','交通']").groupby(['city','industry']).size().reset_index(name="count")
    elif lang == "JavaScript":
        df_alt = df.query("industry in ['计算机软件', '互联网','电子技术','移动互联网','教育','通信','网络游戏','电子商务','金融','计算机服务','交通','IT服务','房地产','医疗']").groupby(['city','industry']).size().reset_index(name="count")
    elif lang == "PHP":
        df_alt = df.query("industry in ['计算机软件', '互联网','电子技术','移动互联网','教育','通信','网络游戏','电子商务','金融','计算机服务','IT服务','广告']").groupby(['city','industry']).size().reset_index(name="count")
    elif lang == "Python":
        df_alt = df.query("industry in ['计算机软件', '互联网','电子技术','移动互联网','教育','通信','网络游戏','电子商务','金融','计算机服务','IT服务','数据服务','交通','人工智能','仪器仪表及工业自动化']").groupby(['city','industry']).size().reset_index(name="count")
    elif lang == "Ruby":
        df_alt = df.query("industry in ['计算机软件', '互联网','电子技术','移动互联网','教育','通信','网络游戏','金融','计算机服务','IT服务','交通']").groupby(['city','industry']).size().reset_index(name="count")
    elif lang == "Swift":
        df_alt = df.query("industry in ['计算机软件', '互联网','电子技术','移动互联网','教育','通信','网络游戏','金融','计算机服务','IT服务','交通','娱乐','电子商务']").groupby(['city','industry']).size().reset_index(name="count")
    else:
        df_alt = df.query("industry in ['计算机软件', '互联网','移动互联网','教育','通信','网络游戏','金融','计算机服务','IT服务','汽车','数据服务','电子商务']").groupby(['city','industry']).size().reset_index(name="count")
    
    df_SH = df_alt.query("city in ['上海']")
    df_BJ = df_alt.query("city in ['北京']")
    df_SZ = df_alt.query("city in ['深圳']")
    df_GZ = df_alt.query("city in ['广州']")

    SH_whole = df.query("city in ['上海']")['industry'].dropna().shape[0]
    BJ_whole = df.query("city in ['北京']")['industry'].dropna().shape[0]
    SZ_whole = df.query("city in ['深圳']")['industry'].dropna().shape[0]
    GZ_whole = df.query("city in ['广州']")['industry'].dropna().shape[0]

    SH_proportion = list(((df_SH['count']/SH_whole)*100).apply(lambda x: format(x,'.3')))
    BJ_proportion = list(((df_BJ['count']/BJ_whole)*100).apply(lambda x: format(x,'.3')))
    SZ_proportion = list(((df_SZ['count']/SZ_whole)*100).apply(lambda x: format(x,'.3')))
    GZ_proportion = list(((df_GZ['count']/GZ_whole)*100).apply(lambda x: format(x,'.3')))

    industry = list(df_SH["industry"])
    c = (
        Bar()
        .add_xaxis(industry)
        .add_yaxis("上海",SH_proportion, category_gap="20%")
        .add_yaxis("北京",BJ_proportion, category_gap="0%")
        .add_yaxis("深圳",SZ_proportion, category_gap="0%")
        .add_yaxis("广州",GZ_proportion, category_gap="20%")
        .set_global_opts(
            yaxis_opts=opts.AxisOpts(name="单位/百分比"),
            xaxis_opts=opts.AxisOpts(name="行业",axislabel_opts=opts.LabelOpts(rotate=-8)),
            title_opts=opts.TitleOpts(title=lang),
            datazoom_opts=opts.DataZoomOpts(),
    )
    )
    print("*"*50)
    return c

df = pd.read_excel("data/LZX/All.xlsx")

def wordcloud_base() :
    welfares = ['五险一金','绩效奖金','餐饮补贴','周末双休','定期体检','员工旅游','带薪年假','定期团建','项目奖金','大牛带队','补充医疗保险','加班补助','年终奖','通讯补贴','交通补贴','零食下午茶','节日福利','免费住宿','不加班','弹性工作','包吃','免费班车','高温补贴','健身俱乐部','全勤奖','年底双薪','住房补贴','专业培训']
    counts=[]

    def sort_welfare():
        for welfare in welfares:
            count = df[df.welfare.str.contains(welfare)].shape[0]
            welfare_count=(welfare,count)
            counts.append(welfare_count)
            return counts
    words = sort_welfare()    
    c = (
        WordCloud()
        .add("", words, word_size_range=[20, 100])
        .set_global_opts(title_opts=opts.TitleOpts(title="WordCloud-基本示例"))
    )
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

@app.route("/wordCloud",methods=[ 'GET'])
def get_wordCloud_chart():
    d = wordcloud_base()
    return d.dump_options()


if __name__ == "__main__":
    app.run()
