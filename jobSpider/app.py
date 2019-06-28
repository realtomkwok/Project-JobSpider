# -*- coding: utf-8 -*-
from random import randrange

from flask import Flask, render_template,url_for, request, json,jsonify
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Grid, Funnel, WordCloud
from pyecharts.globals import SymbolType
import pandas as pd  

app = Flask(__name__, static_url_path='')

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
                              toolbox_opts=opts.ToolboxOpts(),
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
#####################################################################
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
        .set_global_opts(title_opts=opts.TitleOpts(title= city+"各区各编程语言工资", subtitle=""), toolbox_opts=opts.ToolboxOpts(),)
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


def LSQ1(lang) -> Bar:
    language = "data/ZQF/"+lang+".xlsx"
    df = pd.read_excel(language)
    data = df.groupby(['city', 'experience']).avgWage.mean().round(2).reset_index(name='salary')

    shanghai = list(data.query("city=='上海'").salary)
    beijing = list(data.query("city=='北京'").salary)
    guangzhou = list(data.query("city=='广州'").salary)
    shenzhen = list(data.query("city=='深圳'").salary)

    bar = (
        Bar()
        .add_xaxis(['1-5年', '10年以上', '5-10年', '不限'])
        .add_yaxis('上海', shanghai)
        .add_yaxis('北京', beijing)
        .add_yaxis('广州', guangzhou)
        .add_yaxis('深圳', shenzhen)
        .set_global_opts(title_opts={"text": lang, "subtext": "工资与经验关系图"}, toolbox_opts=opts.ToolboxOpts(),)
    )
    return bar


def LSQ2(lang) -> Bar:
    language = "data/ZQF/"+lang+".xlsx"
    df = pd.read_excel(language)
    data = df.groupby(['city', 'experience']).avgWage.mean().round(2).reset_index(name='salary')

    shanghai = list(data.query("city=='上海'").salary)
    beijing = list(data.query("city=='北京'").salary)
    guangzhou = list(data.query("city=='广州'").salary)
    shenzhen = list(data.query("city=='深圳'").salary)

    bar = (
        Bar()
        .add_xaxis(['不限','中专','中技','博士','大专','本科','硕士','高中'])
        .add_yaxis('上海', shanghai)
        .add_yaxis('北京', beijing)
        .add_yaxis('广州', guangzhou)
        .add_yaxis('深圳', shenzhen)
        .set_global_opts(title_opts={"text": lang, "subtext": "工资与经验关系图"},
                          toolbox_opts=opts.ToolboxOpts(),)
    )
    return bar   

def funnel_base(lang) -> Funnel:
    df1 = pd.read_excel("data/ZLQ/position.xlsx",sheet_name=lang)

    df_C = df1.groupby('position').size().reset_index(name="count").sort_values(by="count",ascending= False).iloc[:10]#sort_values(by="count")  
    proportion = ((df_C['count']/df1.shape[0])*100).apply(lambda x: format(x, '.2')) 
    df_C['proportion'] = proportion
    
    proportions = list(df_C['proportion'])
    positions = list(df_C['position'])
    df_C.reset_index(drop = True)
    
    data = [[positions[i],proportions[i]] for i in range(len(positions))]    
    funnel = (
       Funnel()
        .add(
            series_name=lang,
            data_pair=data,
            gap=2,
            tooltip_opts=opts.TooltipOpts(trigger="item", formatter="{a} <br/>{b} : {c}%"),
            itemstyle_opts=opts.ItemStyleOpts(border_color="#fff", border_width=1),
            )
        .set_global_opts(title_opts=opts.TitleOpts(title="{}岗位热门关键词Top10".format(lang)),
                         toolbox_opts=opts.ToolboxOpts(),
                         legend_opts=opts.LegendOpts(is_show=False), 
                        )
        )
    return funnel

def wordcloud_base(lang) -> WordCloud:
    DF = pd.read_excel("data/ZLQ/Lagou.xlsx",sheet_name=lang)
    
    DF_= DF.groupby('split').size().reset_index(name="count").sort_values(by="count",ascending= False).iloc[:10].reset_index(drop = True)
    proportion = ((DF_['count']/DF.shape[0])*100).apply(lambda x: format(x, '.3'))
    DF_['proportion'] = proportion
    
    splits = list(DF_['split'])
    nums = list(DF_['proportion'])
    C_cloud = []
    for i in range(10):
        C_cloud.append((splits[i],nums[i]))
       
    wordcloud = (
        WordCloud()
        .add(lang, C_cloud,
             word_size_range=[20, 150],
             shape="circle",
             )
        .set_global_opts(title_opts=opts.TitleOpts(title="{}热门应用领域".format(lang)),
                         toolbox_opts=opts.ToolboxOpts()
                         )
    )
    return wordcloud

def mjx_base(lang) -> WordCloud:
    df = pd.read_excel("data/MJX/tech.xlsx",sheet_name=lang)
    words = []
    i=0
    for i in range(len(df["标签词"])):
        word = (str(df["标签词"][i]),int(df["词频"][i]))
        words.append(word)
    words = words    
    mjx = (
            WordCloud()
            .add("", words, word_size_range=[20, 100],shape="pentagon",word_gap = 40,rotate_step= 25)
            .set_global_opts(title_opts=opts.TitleOpts(title="WordCloud-shape-diamond"),
                             toolbox_opts=opts.ToolboxOpts())
        )
    return mjx

def LZX1(lang) -> Bar:
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
             toolbox_opts=opts.ToolboxOpts(),
            datazoom_opts=opts.DataZoomOpts(),
    )
    )
    print("*"*50)
    return c


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/salary")
def salary():
    return render_template("salary.html")

@app.route("/district")
def district():
    return render_template("district.html")

@app.route("/district")
def district():
    return render_template("district.html")

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


@app.route("/LSQ1", methods=[ 'POST'])
def get_LSQ1():    
    if request.method == "POST":
        lang = request.form.get('lang', '')
    print(lang)
    c = LSQ1(lang)
    return c.dump_options()

@app.route("/LSQ2", methods=[ 'POST'])
def get_LSQ2():    
    if request.method == "POST":
        lang = request.form.get('lang', '')
    print(lang)
    c = LSQ2(lang)
    return c.dump_options()

@app.route("/funnelChart",methods=[ 'POST'])
def get_funnel_chart():
    if request.method == "POST":
        lang = request.form.get('lang', '')   
    c = funnel_base(lang)
    return c.dump_options()

@app.route("/wordcloudChart",methods=[ 'POST'])
def get_wordcloud_chart():
    if request.method == "POST":
        lang = request.form.get('lang', '')
    d = wordcloud_base(lang)  
    return d.dump_options()

@app.route("/mjxChart",methods=[ 'POST'])
def get_mjx_chart():
    if request.method == "POST":
        lang = request.form.get('lang', '')   
    e = mjx_base(lang)  
    return e.dump_options()

@app.route("/LZX1",methods=[ 'POST'])
def get_bar_chart():
    if request.method == "POST":
        lang = request.form.get('lang', '')
    print(lang)
    c = LZX1(lang)
    return c.dump_options()

if __name__ == "__main__":
    app.run()

